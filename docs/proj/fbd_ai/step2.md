# 防病毒检测能力增强方案（第二步）

## 一、第二步的目标

你现在已经完成了一个最小闭环。

1. 本机已经安装并运行了 Ollama。
2. Python 脚本可以把一条告警交给本地模型进行初步分析。
3. 当前脚本已经有基础规则层，可以结合签名、路径、父进程、行为标记给出保守判断。

第二步不建议直接跳到“训练一个更大的模型”。

更务实的方向是先把 `detection_name`、`file_path` 周边能拿到的信号补齐，再让规则层、历史案例和本地模型一起做判断。这样投入更小，也更容易在当前进展上看到效果。

如果把第二步压缩成一句话，它的目标可以定义为。

**把“只看一条告警文本”升级为“看结构化特征、历史案例和可信度信号的文件级智能研判”。**

---

## 二、为什么只靠 detection_name 和 file_path 不够

这两个字段当然有价值，但单独使用时有明显局限。

- `detection_name` 往往带有厂商命名习惯，噪声很大。像 `Trojan.Generic`、`Heur.Malware`、`PUA` 这类名字，本身并不能稳定代表真实风险。
- `file_path` 能反映信任边界，但不能直接证明文件良恶。合法升级程序和恶意落地文件，都可能出现在相似目录。
- 真实研判时，分析员其实不会只看这两个字段，而是会同时看签名、文件类型、出现频次、父进程、落地位置、是否来自软件发布、是否命中历史误报等信息。

所以第二步的关键不是把提示词写得更花，而是把输入先做成更接近人工研判习惯的结构化告警画像。

---

## 三、建议的增强路线

建议按下面这条顺序推进，而不是一上来就微调。

1. 先把 `detection_name` 和 `file_path` 做标准化与标签化。
2. 再增加文件可信度、路径可信度和出现频次等低成本特征。
3. 再把你们自己的历史误报和真实案例做成一个本地案例库。
4. 最后再考虑 LoRA 微调或蒸馏，而不是把模型当成唯一能力来源。

这个顺序的优点很明确。

- 不依赖大规模标注数据。
- 对 CPU 更友好。
- 更容易解释为什么这样判断。
- 后续即使换模型，前面的特征和案例库也不会浪费。

---

## 四、第一类增强：把 detection_name 做成可计算特征

### 1. 先做检测名归一化

很多杀软检测名里混有大量厂商前缀、变体编号和噪声片段，建议先做标准化处理，例如。

- 转小写
- 去掉空格、重复分隔符
- 拆分出家族词、风险词、泛化词
- 区分 `generic`、`heur`、`pua`、`hacktool`、`trojan`、`worm`、`backdoor` 这类关键词

建议至少抽取下面这些标签。

- `family_tag`：例如 `trojan`、`worm`、`backdoor`
- `generic_tag`：是否为泛化检测，如 `generic`、`heur`
- `grayware_tag`：是否更偏灰产或工具类，如 `pua`、`hacktool`
- `specific_family`：是否识别出较稳定的家族名

这样做的价值是，模型以后不必每次都直接看原始检测名，而是可以先参考这些标签。

### 2. 给 detection_name 做一个初始打分表

你可以先不训练模型，先维护一份简单的检测名词典，例如。

| 关键词 | 倾向 | 说明 |
| --- | --- | --- |
| `generic` / `heur` | 中性偏保守 | 代表泛化或启发式检测，不能单独定性 |
| `pua` / `riskware` | 偏误报或灰区 | 常需要结合业务场景判断 |
| `hacktool` | 高依赖场景 | 在运维机上可能合理，在办公终端上更可疑 |
| `trojan` / `backdoor` / `worm` | 偏高风险 | 仍需结合路径、签名、行为和历史案例 |

这个词典不要求一开始就很完整，但要能持续积累。

---

## 五、第二类增强：把 file_path 做成路径风险画像

路径是当前阶段最容易补强、成本最低、收益最高的信号之一。

### 1. Windows 下建议重点区分的路径类型

可以把路径先映射为 `path_class`。

| 路径类型 | 示例 | 倾向 |
| --- | --- | --- |
| 系统目录 | `C:\\Windows\\System32\\` | 中性，需结合签名与父进程 |
| 软件安装目录 | `C:\\Program Files\\` | 更偏可信，但不能单独放行 |
| 用户目录 | `C:\\Users\\<user>\\` | 风险抬高 |
| 临时目录 | `C:\\Users\\<user>\\AppData\\Local\\Temp\\` | 风险抬高 |
| 启动相关目录 | `Startup`、注册表自启动关联路径 | 高风险 |
| 下载与桌面目录 | `Downloads`、`Desktop` | 中高风险 |

还可以继续提取下面这些信号。

- 是否位于 `AppData`、`Temp`、`ProgramData`
- 是否扩展名和目录不匹配，例如 `jpg.exe`、`pdf.scr`
- 是否文件名伪装系统组件，例如 `svch0st.exe`、`expl0rer.exe`
- 是否位于启动项、计划任务、服务二进制路径关联位置

### 2. Linux 下建议重点区分的路径类型

Linux 下同样可以先按目录语义分类。

| 路径类型 | 示例 | 倾向 |
| --- | --- | --- |
| 系统程序目录 | `/usr/bin/`、`/usr/sbin/` | 中性，先看包归属和签名来源 |
| 第三方安装目录 | `/opt/`、`/usr/local/` | 中性偏可信 |
| 用户目录 | `/home/<user>/` | 风险抬高 |
| 临时目录 | `/tmp/`、`/var/tmp/`、`/dev/shm/` | 高风险 |
| 自动启动位置 | `~/.config/autostart/`、`/etc/cron.*` | 高风险 |
| 隐蔽目录 | `/tmp/.x11/`、名称以 `.` 开头的异常目录 | 高风险 |

Linux 侧额外要注意下面几类情况。

- ELF 文件伪装成图片、文档或脚本资源
- 可执行文件落在 `/tmp`、`/dev/shm`、用户下载目录
- 与 `systemd service`、`cron`、`rc.local`、`bashrc` 等持久化位置有关联
- 被 shell、python、perl、curl、wget 等解释器或下载器拉起

### 3. 路径不只看“在哪”，还要看“像不像正常文件”

建议把下面几个字段一并补上。

- `path_class`
- `file_ext`
- `path_depth`
- `is_hidden_file`
- `is_temp_path`
- `is_startup_related`
- `name_masquerading_score`

只要这一步做好，哪怕暂时还没做检索和微调，判断质量也会比单纯把原始路径交给 LLM 稳定很多。

---

## 六、第三类增强：补齐文件可信度特征

如果你希望模型更好判断“这个文件是不是病毒”，那就不要只把路径和检测名扔进去。

至少还应该增加下面几类特征。

### 1. 文件基本特征

- 文件大小
- SHA256
- 文件类型
- 编译时间或修改时间
- 是否可执行文件
- 是否带壳或高熵

### 2. 可信度特征

- 是否有数字签名
- 签名发布者是否可信
- 是否属于操作系统或已安装软件包
- 是否来自统一软件发布
- 同一哈希是否在多台机器上同时出现

### 3. 上下文特征

- 父进程
- 命令行参数
- 当前主机角色
- 是否命中计划任务、自启动、服务、注册表或 systemd 持久化
- 是否伴随外联、提权、凭据访问等行为标记

你现在的脚本已经支持 `signed`、`signer`、`parent_process`、`prevalence`、`distribution`、`behavior_flags`，这很好。第二步最直接的收益点，就是把这些字段补得更完整、更稳定。

---

## 七、第四类增强：把历史样本做成案例库，而不是只问模型

这是最值得投入的一步。

即使模型不变，只要你做出一个小型本地案例库，效果就会明显提升。

### 1. 最小案例库字段建议

建议先用 CSV 或 JSONL 维护，不必一开始就上数据库。

每条案例至少包含。

- `case_id`
- `detection_name_raw`
- `detection_tags`
- `file_path_raw`
- `path_class`
- `file_hash`
- `signer`
- `parent_process`
- `behavior_flags`
- `final_label`
- `analyst_reason`
- `recommended_action`

### 2. 检索时优先匹配什么

建议优先按下面的顺序做相似性召回。

1. 同一哈希
2. 同一路径模式
3. 同一检测名归一化结果
4. 同一签名发布者
5. 同一父进程和行为组合

### 3. 案例库为什么现在就该做

因为它比微调门槛低，而且和现有方案天然兼容。

- 规则命不中时，可以先检索历史案例。
- 模型解释时，可以把 1 到 3 条相似案例一起输入。
- 后续做微调时，这些案例又能直接变成训练样本。

---

## 八、第五类增强：提示词与输出格式要改成“证据驱动”

当前脚本已经要求模型输出 JSON，这是对的。第二步建议继续加强下面几点。

### 1. 输入模板改成结构化摘要

不要让模型直接读一大段原始日志，建议固定成下面这种输入结构。

```json
{
	"detection_name": "Trojan.GenericKD",
	"detection_tags": ["trojan", "generic"],
	"file_path": "C:\\Users\\alice\\AppData\\Local\\Temp\\run.exe",
	"path_class": "windows_temp",
	"signed": false,
	"signer": "",
	"file_type": "pe32 executable",
	"parent_process": "powershell.exe",
	"prevalence": "low",
	"distribution": "unknown",
	"behavior_flags": ["scheduled_task", "network_beacon"],
	"matched_history": [
		"过去90天无相同哈希误报记录"
	],
	"rule_summary": {
		"false_positive_signals": [],
		"suspicious_signals": [
			"位于临时目录",
			"无签名",
			"父进程为 powershell.exe"
		]
	}
}
```

### 2. 输出里必须保留“不确定”

不要逼模型只输出“病毒”或“不是病毒”。

建议至少保留下面三类。

- `likely_false_positive`
- `likely_true_positive`
- `needs_review`

在安全场景里，让模型承认“不确定”，通常比强行给结论更可靠。

### 3. 让模型明确说明“为何推翻规则层”

这是为了后续调优。

如果模型和规则层结论不一致，就让它必须说明理由。这样你后面才能判断问题到底出在规则、数据、提示词还是样本本身。

---

## 九、Windows 下的可落地做法

下面这些做法不要求你立刻重写整套系统，可以先人工执行，再逐步脚本化。

### 1. 采集文件基础信息

```powershell
$path = 'C:\Users\alice\AppData\Local\Temp\run.exe'
Get-Item $path | Select-Object FullName, Length, CreationTime, LastWriteTime
Get-FileHash $path -Algorithm SHA256
Get-AuthenticodeSignature $path | Select-Object Status, StatusMessage, SignerCertificate
```

### 2. 判断是否位于高风险目录

```powershell
$path = 'C:\Users\alice\AppData\Local\Temp\run.exe'
$highRisk = @('\\AppData\\', '\\Temp\\', '\\Downloads\\', '\\Desktop\\')
$highRisk | ForEach-Object {
	if ($path -like "*$_*") { "HIGH_RISK_PATH: $_" }
}
```

### 3. 看是否与持久化相关

```powershell
Get-ScheduledTask | Where-Object {
	$_.Actions.Execute -like '*run.exe*'
}

reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
```

### 4. 看是否命中业务软件或更新场景

可以先维护一份简单白名单。

- 合法软件安装目录
- 合法签名发布者
- 合法升级程序文件名
- 已确认误报的哈希

第一阶段不必复杂，CSV 就够用。

---

## 十、Linux 下的可落地做法

Linux 侧的判断逻辑类似，但要多看包归属、文件类型和持久化位置。

### 1. 采集文件基础信息

```bash
path='/tmp/run.sh'
stat "$path"
file "$path"
sha256sum "$path"
strings -n 6 "$path" | head -n 30
```

### 2. 判断文件是否属于已安装软件包

Debian / Ubuntu 系列。

```bash
dpkg -S "$path"
```

RHEL / CentOS / Rocky / openEuler 系列。

```bash
rpm -qf "$path"
```

如果一个可执行文件位于系统目录，但不属于任何已安装包，就应该明显抬高风险。

### 3. 判断是否位于高风险目录

```bash
path='/tmp/run.sh'
case "$path" in
	/tmp/*|/var/tmp/*|/dev/shm/*|/home/*/Downloads/*|/home/*/.config/autostart/*)
		echo HIGH_RISK_PATH
		;;
	esac
```

### 4. 检查是否涉及持久化

```bash
crontab -l
grep -R --line-number 'run.sh' /etc/cron* /etc/systemd/system ~/.config/autostart 2>/dev/null
systemctl list-unit-files --type=service | grep -i run
```

### 5. 检查是否由高风险解释器或下载器拉起

建议把下面这些父进程优先标为高风险。

- `bash`
- `sh`
- `python`
- `perl`
- `curl`
- `wget`
- `nc`

如果可执行文件位于 `/tmp`、无包归属、由这些解释器或下载器拉起，那么即使检测名是 `Generic`，也不应轻易判成误报。

---

## 十一、建议你下一步实际补哪些字段

如果只允许你在当前 JSON 输入上多加一些字段，我建议优先补下面这些。

| 字段 | 作用 | 优先级 |
| --- | --- | --- |
| `file_type` | 判断是否为可执行文件、脚本或文档 | 高 |
| `file_hash` | 关联历史案例和白名单 | 高 |
| `path_class` | 把路径从文本转成类别 | 高 |
| `signer_trusted` | 比原始签名字符串更适合规则判断 | 高 |
| `package_owner` | Linux 下判断是否属于合法软件包 | 高 |
| `parent_process` | 判断启动链路 | 高 |
| `command_line` | 判断是否为下载执行、解压执行 | 中 |
| `first_seen` / `prevalence` | 判断是否大范围出现 | 中 |
| `persistence_flags` | 判断是否命中持久化 | 中 |
| `matched_case_ids` | 让模型引用历史案例 | 中 |

只要你把这些字段逐步补进来，模型对同一条告警的判断质量通常会明显好于现在只看 `detection_name` 和 `file_path`。

---

## 十二、建议的最小实施顺序

为了避免第二步做得太散，建议按下面三轮推进。

### 第 1 轮：先把输入字段补齐

目标是最快看到质量提升。

建议动作。

1. 给 `detection_name` 做归一化和标签提取。
2. 给 `file_path` 做 `path_class` 分类。
3. 增加 `file_type`、`file_hash`、`signer_trusted`、`package_owner`。
4. 把 Windows 和 Linux 的高风险目录、可信目录写成规则表。

### 第 2 轮：做规则增强和案例库

目标是让系统先学会你们自己的常见场景。

建议动作。

1. 维护一份误报白名单和可疑规则表。
2. 整理最近 50 到 200 条历史案例。
3. 让模型先看规则摘要，再看最相似的 1 到 3 条案例。

### 第 3 轮：再考虑微调

只有在前两轮做完后，微调才更有价值。

建议动作。

1. 把高质量案例转成指令数据。
2. 只微调结构化研判和解释能力，不急着让模型记所有安全知识。
3. 用保留测试集检查漏报率、待复核召回率和输出稳定性。

---

## 十三、第二步的验收标准

第二步是否做成，不要只看模型回答是不是更像专家，而要看下面这些指标有没有改善。

1. 同类高频误报是否更容易被识别出来。
2. 位于高风险目录、无签名、低频出现的样本是否更容易被升级为可疑。
3. 模型输出里是否能清楚说出关键证据，而不是只复述告警。
4. 对证据不足的样本，是否更稳定地输出 `needs_review`。

如果这四点都有改善，就说明你的第二步是有效的。

---

## 十四、我对你当前阶段的建议

基于你已经完成的进度，我最建议你现在就做下面三件事。

1. 先别急着换更大的模型，先把路径分类、文件类型、签名和历史案例补上。
2. 先把 Windows 和 Linux 的高风险目录、可信目录、持久化位置整理成规则表。
3. 先积累一批你们自己确认过的误报和真实案例，再决定是否做 LoRA 微调。

对你这个项目来说，第二步真正提升效果的关键，通常不是“模型参数更多了”，而是“输入更像人工分析员真正会看的证据了”。
