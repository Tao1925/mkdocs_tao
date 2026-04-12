# 桌面运维工程师

## 总览（初级）

### 脚本语言

- [Shell](Shell)
- [Python](#Python)
### 运维工具

- [流程、运维、监控、配置平台](#流程、运维、监控、配置平台)
### 中间件

- [Nginx](#Nginx)
- [Redis](#Redis)
- [Tomcat](#Tomcat)
- [Tongweb](#Tongweb)
### 数据库

- [数据库基础](#数据库基础)
- [Oracle](#Oracle)
- [Mysql](#Mysql)
- [国产改造](#国产改造)
### 虚拟化

- [VMWare/FC](#VMWare/FC)
- [Docker/K8s](#Docker/K8s)
### 终端安全

- [主机安全](#主机安全)
- [终端管理](#终端管理)
### 操作系统

- [Linux/Kylin](#Linux/Kylin)
- [Windows](#Windows)
### 服务器

- [服务器基础](#服务器基础)
### 网络

- [网络基础](#网络基础)


<h2 id="Shell">Shell</h2>
1、脚本声明与注释


```bash
#!/bin/bash  # 最常见，使用 Bash 解释器
#!/bin/sh    # 使用系统默认的 Shell（可能是 Bash 的兼容模式，也可能是更简单的如 dash）
# 这是一个单行注释
echo "Hello"  # 这也是一个注释（在命令之后）
```
2、变量
```bash
MY_NAME="Alice" # 变量名通常为大写，非必须
COUNT=10 # 等号两侧不带空格
FILE_PATH="/home/user/docs/file.txt" # 值可以是数字、字符串（引号非必须，但推荐处理空格或特殊字符时使用）
```
3、引号
```bash
# 单引号 ('): 强引用。引号内所有字符都按字面意义解释，变量和命令替换不会发生。
echo '$HOME is your home' # 输出 $HOME is your home
 #双引号 ("): 弱引用。引号内允许变量扩展 ($var)、命令替换 (`command` 或 $(command)) 和转义字符 (\)。是最常用的引号。
bash echo "Your home is $HOME" # 输出 Your home is /home/username
echo "Date: $(date)"     # 输出 Date: Fri Jun 20 12:34:56 UTC 2025
# 反引号 (`): 用于命令替换（将命令的输出作为字符串）。推荐使用更清晰且支持嵌套的 $(command) 形式。
bash
OLD_STYLE=`date`      # 旧方式
NEW_STYLE=$(date)     # 推荐方式
```
4、输入输出
```bash
# 输出 (echo): 最常用的输出命令。
bash
echo "Hello World"
echo -e "Line1\nLine2"  # -e 启用反斜杠转义（如 \n 换行）
# 输出 (printf): 提供更精确的格式化输出（类似 C 语言的 printf）。
bash
printf "Name: %-10s Age: %d\n" "Alice" 30 # 格式化输出
# 输入 (read): 从标准输入（通常是键盘）或文件读取数据到变量。
bash
read -p "Enter your name: " USER_NAME # -p 显示提示符
echo "Hello, $USER_NAME!"
```
5、条件判断
```bash
if [ condition ]; then # 注意 [ 后和 ] 前必须有空格
    # commands if true
elif [ another_condition ]; then
    # commands if elif true
else
    # commands if false
fi
```
6、循环
```bash
# for循环-列表
for fruit in apple banana orange; do
    echo "I like $fruit"
done
# for循环-命令输出
for file in $(ls *.txt); do # 遍历当前目录下所有 .txt 文件
    echo "Processing $file"
done
# while循环
count=1
while [ $count -le 5 ]; do # 使用 [ ]
# while [[ $count -le 5 ]]; do # 使用 [[ ]]
    echo "Count: $count"
    count=$((count + 1))    # 算术运算
done
# until循环
count=1
until [ $count -gt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```
7、函数
```bash
function say_hello() {  # 'function' 关键字可选
    local name="$1"     # 'local' 使变量只在函数内可见。$1 是函数的第一个参数
    echo "Hello, $name!"
}
say_hello "Bob"
```
8、重定向与管道
```bash
>: 覆盖输出重定向 (command > file 将 command 的 stdout 覆盖到 file)。
>>: 追加输出重定向 (command >> file 将 command 的 stdout 追加到 file)。
<: 输入重定向 (command < file 从 file 读取输入给 command)。
2>: 错误输出重定向 (command 2> error.log 将 stderr 重定向到 error.log)。
&> 或 > file 2>&1: 将 stdout 和 stderr 都重定向到 file。
|: 管道 (command1 | command2 将 command1 的 stdout 作为 command2 的 stdin)。
```
9、系统监控
```bash
top
free
iostat
```
10、磁盘与网络
```bash
df
du
lsblk
fdisk
mount

ifconfig
ping
netstat
iptables
```
11、用户与权限
```bash
useradd\mod\del
passwd
groupadd
id
su
sudo
chmod
chown
umask
```
<h2 id="Python">Python</h2>

<h2 id="流程、运维、监控、配置平台">流程、运维、监控、配置平台</h2> 

Prometheus+Granfa

<h2 id="Nginx">Nginx</h2> 
1、基础介绍

```
定位：高性能的开源 Web 服务器 + 反向代理 + 负载均衡器 + HTTP 缓存。
核心优势：
高并发：事件驱动架构（Epoll/Kqueue），轻松应对万级并发连接。
低资源消耗：内存占用远低于传统服务器（如 Apache）。
模块化设计：通过模块扩展功能（如 SSL、压缩、流媒体）。
典型用途：
托管静态资源（HTML/CSS/JS/图片）
反向代理转发请求到后端应用（Tomcat/Python/Node.js）
负载均衡分发流量到多台服务器
终结 SSL/TLS 加密（HTTPS）
实现 URL 重写、访问控制、缓存加速
```
2、常用命令
```bash
nginx -t	# 检查配置文件语法	
nginx -s reload	# 平滑重载配
nginx -s stop	# 立即停止服务	
systemctl status nginx	# 查看服务状态	
tail -f /var/log/nginx/access.log	# 实时监控访问日志	
ss -tulnp | grep nginx	# 查看 Nginx 监听端口	
```
3、nginx.conf
```nginx
user nginx;                     # 运行进程的用户/组
worker_processes auto;           # 工作进程数（通常设为 CPU 核心数）
error_log /var/log/nginx/error.log warn; # 错误日志路径与级别
pid /run/nginx.pid;              # 主进程 PID 文件位置
events {
    worker_connections 1024;     # 单个工作进程最大连接数
    use epoll;                   # 事件驱动模型（Linux 建议 epoll）
}
http {
    include /etc/nginx/mime.types;  # 文件扩展名与 MIME 类型映射
    default_type application/octet-stream; # 默认 MIME 类型

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main; # 访问日志路径

    sendfile on;                  # 零拷贝传输文件（提升性能）
    tcp_nopush on;                # 优化数据包发送
    keepalive_timeout 65;         # 客户端长连接超时时间（秒）

    gzip on;                      # 开启 Gzip 压缩
    gzip_types text/plain text/css application/json; # 压缩类型

    # 包含子配置（如 server 块）
    include /etc/nginx/conf.d/*.conf;
}
server {
    listen 80;                   # 监听端口（HTTP）
    server_name example.com www.example.com; # 域名（支持通配符）

    root /var/www/html;          # 网站根目录
    index index.html index.htm;   # 默认首页文件

    # 访问控制（按需使用）
    location /admin/ {
        allow 192.168.1.0/24;    # 允许内网访问
        deny all;                 # 拒绝其他所有 IP
        auth_basic "Restricted";  # 启用基础认证
        auth_basic_user_file /etc/nginx/.htpasswd; # 认证文件
    }

    # 反向代理配置（转发到后端应用）
    location /api/ {
        proxy_pass http://backend_server; # 后端服务器地址（需提前定义 upstream）
        proxy_set_header Host $host;      # 传递原始域名
        proxy_set_header X-Real-IP $remote_addr; # 传递客户端真实 IP
    }

    # 静态文件缓存（提升性能）
    location ~* \.(jpg|png|css|js)$ {
        expires 30d;             # 客户端缓存 30 天
        add_header Cache-Control "public";
    }

    # 错误页面自定义
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
upstream backend_server {
    server 10.0.0.1:8080 weight=3;  # 权重 3，处理更多请求
    server 10.0.0.2:8080;           # 默认权重 1
    server 10.0.0.3:8080 backup;    # 备份服务器（仅当主节点宕机时启用）

    # 负载均衡算法（默认轮询）
    # least_conn;   # 最少连接数
    # ip_hash;      # 基于客户端 IP 哈希（会话保持）
}
server {
    listen 443 ssl http2;         # 启用 HTTP/2 优化
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;     # 证书路径
    ssl_certificate_key /etc/nginx/ssl/example.com.key; # 私钥路径

    ssl_protocols TLSv1.2 TLSv1.3; # 禁用不安全协议
    ssl_ciphers HIGH:!aNULL:!MD5;  # 强加密套件
    ssl_prefer_server_ciphers on;  # 优先使用服务端加密套件
    ssl_session_cache shared:SSL:10m; # SSL 会话缓存
    ssl_session_timeout 10m;       # 会话超时时间

    # 强制 HTTP 跳转 HTTPS
    if ($scheme = http) {
        return 301 https://$server_name$request_uri;
    }
}
```
<h2 id="Redis">Redis</h2> 
1、非关系型数据库

```
定义：非关系型数据库，不依赖传统的关系模型（无固定表结构、无SQL语法）。
诞生背景：解决高并发、海量数据、灵活数据结构的需求（如社交网络、物联网）。

```
| 类型     | 代表数据库   | 数据结构            | 典型场景       |
| ---------- | ----------------- | ----------------------- | ------------------ |
| 键值存储 | Redis, DynamoDB   | Key-Value               | 缓存、会话存储 |
| 文档数据库 | MongoDB, CouchDB  | JSON/BSON 文档        | 内容管理、用户配置 |
| 列族数据库 | Cassandra, HBase  | 列簇（Column Families） | 时序数据、日志分析 |
| 图数据库 | Neo4j, JanusGraph | 节点+关系           | 社交网络、推荐系统 |

2、redis概念

```
定位：开源 内存型键值数据库（也可持久化），支持多种数据结构。
核心标签：
单线程模型（6.0+ 支持多线程 I/O）
响应时间 < 1ms
支持主从复制、哨兵、集群模式
官方定义：“REmote DIctionary Server”（远程字典服务）
```
3、redis

4、redis常用命令
```bash
sudo apt install redis-server # 安装
# 关键配置文件（/etc/redis/redis.conf）：
bind 0.0.0.0            # 允许远程访问（生产环境需配合防火墙）
requirepass yourpassword # 设置访问密码
maxmemory 4gb           # 最大内存限制
appendonly yes          # 开启 AOF 持久化
# 常用运维命令
redis-cli ping	#检查服务状态	→ 返回 PONG 表示正常
redis-cli info	#查看全部运行信息	info memory（只看内存）
redis-cli --stat	#实时监控操作统计	
redis-benchmark -c 100	#压力测试（100并发连接）	
KEYS *	#列出所有Key（生产禁用！）	SCAN 0 MATCH user:*（安全遍历）
BGSAVE	#后台触发 RDB 持久化
```

<h2 id="Tomcat">Tomcat</h2>
<h2 id="Tongweb">Tongweb</h2> 

| 对比维度     | TongWeb                                    | Tomcat                               |
| ------------ | ------------------------------------------ | ------------------------------------ |
| 架构定位     | 全功能企业级应用服务器（支持 EJB、JMS 等） | 轻量级 Web 服务器/Servlet 容器       |
| 规范支持     | 完整 Java EE/Jakarta EE 全栈规范           | 仅支持 Servlet/JSP（部分 J2EE 标准） |
| 性能与扩展性 | 高并发集群、Failover 容灾、动态伸缩        | 单节点受限，无原生集群管理           |
| 安全能力     | 内置可信计算、国密算法、等保四级合规       | 依赖外部安全方案，无主动防御机制     |
| 运维管理     | 提供 APM 性能诊断、热部署、集中管控台      | 需第三方工具扩展，无统一监控平台     |
| 技术服务     | 企业级售后支持（金融/政务专属团队）        | 社区支持为主，无官方保障             |




| 维度     | Tomcat                                 | Nginx                                     |
| ---------- | -------------------------------------- | ----------------------------------------- |
| 本质     | Java应用服务器（Servlet/JSP容器） | 高性能HTTP服务器/反向代理       |
| 动态处理 | ✅ 原生支持Java动态内容（Servlet/JSP） | ❌ 需通过FastCGI、uWSGI等代理后端动态语言 |
| 静态资源 | ⚠️ 可处理但效率较低        | ✅ 极高性能（事件驱动模型+零拷贝技术） |
| 企业级能力 | ✅ 支持EJB、JMS等Java EE规范    | ❌ 无内置企业级中间件支持     |








<h2 id="数据库基础">数据库基础</h2> 

SQL

| JOIN类型 | 是否保留未匹配数据 | 常见场景               |
| ---------- | ------------------ | -------------------------- |
| INNER JOIN | 否                | 精确匹配关联         |
| LEFT JOIN  | 保留左表       | 主表附带可选信息   |
| RIGHT JOIN | 保留右表       | 较少使用（可被左连接替代） |
| FULL JOIN  | 保留双表       | 数据完整性检查      |
| CROSS JOIN | 无关联条件    | 生成组合/测试数据  |

DXL

| 类型 | 典型命令         | 作用对象 | 是否自动提交 |
| ---- | -------------------- | ---------- | ------------- |
| DDL  | CREATE/ALTER/DROP    | 数据库结构 | ✅ 自动提交 |
| DML  | INSERT/UPDATE/DELETE | 数据记录 | ❌ 需显式提交 |
| DQL  | SELECT               | 数据查询 | 不涉及事务 |
| DCL  | GRANT/REVOKE         | 访问权限 | ✅ 自动生效 |
| TCL  | COMMIT/ROLLBACK      | 事务状态 | 控制DML执行 |


sql优化

```sql
-- 为高频查询列建索引
-- 优化前：全表扫描（耗时2s+）
SELECT * FROM orders WHERE user_id = 1005;
-- 优化后：创建索引（耗时0.01s）
CREATE INDEX idx_user_id ON orders(user_id);

-- 复合索引最左匹配原则
-- 索引：idx_city_age(city, age)
SELECT * FROM users WHERE city='北京' AND age>30; -- ✅ 命中索引
SELECT * FROM users WHERE age>30;                -- ❌ 无法命中

-- 覆盖索引减少回表
-- 优化前：需回表查name
SELECT name FROM products WHERE category='电子产品';
-- 优化后：建立覆盖索引
CREATE INDEX idx_category_name ON products(category, name);

-- 避免SELECT *
-- 坏实践：读取无用字段
SELECT * FROM employees WHERE dept='IT';
-- 好实践：仅取所需
SELECT id, name FROM employees WHERE dept='IT';

-- 用EXISTS替代IN（大数据集）
-- 低效：IN导致全表扫描
SELECT * FROM orders 
WHERE product_id IN (SELECT id FROM products WHERE price>1000);
-- 高效：EXISTS短路查询
SELECT * FROM orders o 
WHERE EXISTS (SELECT 1 FROM products p 
             WHERE p.id=o.product_id AND p.price>1000);

-- 分页优化：避免OFFSET大偏移
-- 低效：偏移10万条（扫描10万+20行）
SELECT * FROM logs ORDER BY id LIMIT 20 OFFSET 100000;
-- 高效：记住上一页末尾ID
SELECT * FROM logs WHERE id > 100000 ORDER BY id LIMIT 20;

-- 小表驱动大表（JOIN优化）
-- 低效：大表orders驱动小表users
SELECT * FROM orders o JOIN users u ON o.user_id=u.id;
-- 高效：小表驱动大表（尤其LEFT JOIN）
SELECT * FROM users u LEFT JOIN orders o ON u.id=o.user_id;

-- 数据类型优化
-- 用INT而非VARCHAR存储ID（减少比较开销）
-- 日期字段用DATETIME而非字符串

-- 分区表应对海量数据
-- 按月分区（OceanBase/GoldenDB均支持）
CREATE TABLE logs (
  id BIGINT,
  log_time DATETIME
) PARTITION BY RANGE (YEAR(log_time)*100 + MONTH(log_time)) (
  PARTITION p202401 VALUES LESS THAN (202402),
  PARTITION p202402 VALUES LESS THAN (202403)
);

-- 禁止在WHERE中对字段做运算
-- 索引失效：无法使用create_time索引
SELECT * FROM orders WHERE YEAR(create_time)=2024;
-- 优化后：范围查询
SELECT * FROM orders 
WHERE create_time BETWEEN '2024-01-01' AND '2024-12-31';
```

索引

数据库中的索引是加速数据检索的核心数据结构，相当于书籍的目录。它通过牺牲少量存储空间和写入性能，换取查询效率的指数级提升。

```sql
-- 创建索引
CREATE INDEX idx_email ON users(email);

-- 删除索引
DROP INDEX idx_email ON users;

-- 查看索引
SHOW INDEX FROM users;

-- 重建索引（解决碎片化）
ALTER TABLE users REBUILD INDEX idx_name;
```

事务ACID

| 特性                                 | 核心目标                                                | 实现机制 | 违反后果 |
| -------------------------------------- | ----------------------------------------------------------- | -------- | -------- |
| Atomicity  | 事务“要么全做，要么全不做” | - Undo Log（回滚日志）- 事务中任何一步失败自动回滚所有操作|部分更新导致数据逻辑矛盾                   |
| Consistency |事务前后数据满足业务规则 | - 数据库约束（主键/唯一键/外键/CHECK）- 业务逻辑在事务中封装 |脏数据破坏业务完整性       |
| Isolation  | 并发事务互不干扰   | - 锁机制（行锁/表锁）| 脏读/幻读/不可重复读    - MVCC（多版本并发控制）   |
| Durability | 提交后数据永久保存 | - Redo Log（重做日志）- 事务提交后日志刷盘，即使宕机也能恢复|数据丢失造成业务中断          |

| 问题                          | 现象                                                           | 示例                                                                  |
| ------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 脏读(Dirty Read)              | 读到其他事务未提交的数据                             | 事务A读到事务B修改后未提交的余额，B回滚导致A读到“幽灵数据” |
| 不可重复读(Non-Repeatable Read) | 同一事务内两次读取同一条数据，结果不一致（数据被其他事务修改） | 事务A第一次查余额1000，事务B扣减后提交，A再查变成900 |
| 幻读(Phantom Read)            | 同一事务内两次查询同一条件，返回的行数不同（数据被其他事务增删） | 事务A查询年龄>30有10人，事务B插入1人后提交，A再查询变成11人 |
| 丢失更新(Lost Update)       | 两个事务同时修改同一数据，后提交者覆盖前者的修改 | 事务A和B同时读余额1000，A存入100（1100），B取出200（800），最终余额错误 |

| 隔离级别                 | 脏读 | 不可重复读 | 幻读 | 实现方式                 | 典型数据库默认级别 |
| ---------------------------- | ---- | ---------- | ---- | ---------------------------- | ------------------ |
| READ UNCOMMITTED（读未提交） | ❌  | ❌        | ❌  | 无锁，直接读内存最新数据 | 极少使用       |
| READ COMMITTED               | ✅  | ❌        | ❌  | MVCC：每次读生成快照 | Oracle、SQL Server |
| REPEATABLE READ（可重复读） | ✅  | ✅        | ❌  | MVCC：事务开始时生成全局快照 | MySQL（InnoDB）  |
| SERIALIZABLE（串行化）  | ✅  | ✅        | ✅  | 读写均加锁（性能最低） |                    |


缓存




锁

| 锁类型               | 冲突对象   | 适用场景           | SQL示例                     |
| ----------------------- | -------------- | ---------------------- | ----------------------------- |
| 共享锁 (S Lock)      | 独占锁(X)   | 读取数据（不修改） | SELECT ... LOCK IN SHARE MODE |
| 独占锁 (X Lock)      | 共享锁/独占锁 | 修改数据（增删改） | SELECT ... FOR UPDATE         |
| 意向锁 (Intention Lock) | 表级锁冲突检测 | 快速判断表中是否有行锁 | 自动管理                  |

```mermaid
graph TB
    A[数据库] --> B[表级锁]
    A --> C[页级锁]
    A --> D[行级锁]
    D --> E[记录锁 Record Lock]
    D --> F[间隙锁 Gap Lock]
    D --> G[临键锁 Next-Key Lock]
```

```sql
-- 记录锁 (Record Lock)
-- 锁定id=100的记录（索引项）
SELECT * FROM users WHERE id=100 FOR UPDATE;

-- 间隙锁 (Gap Lock)
-- 锁定(20,30)区间，防止插入
SELECT * FROM users WHERE age BETWEEN 20 AND 30 FOR UPDATE;

-- 临键锁 (Next-Key Lock) = 记录锁 + 间隙锁
```

| 当前锁 → 请求锁 | X  | S  | IX | IS |
| --------------- | -- | -- | -- | -- |
| X (独占锁)   | ❌ | ❌ | ❌ | ❌ |
| S (共享锁)   | ❌ | ✅ | ❌ | ✅ |
| IX (意向独占锁) | ❌ | ❌ | ✅ | ✅ |
| IS (意向共享锁) | ❌ | ✅ | ✅ | ✅ |

```mermaid
sequenceDiagram
    事务A->>表1: 持有行1的X锁
    事务B->>表2: 持有行2的X锁
    事务A->>表2: 申请行2的X锁（阻塞）
    事务B->>表1: 申请行1的X锁（死锁！）
```
```bash
死锁处理策略
# 死锁检测（默认）
InnoDB：innodb_deadlock_detect=ON
发现死锁后回滚代价最小的事务

# 超时等待
SET innodb_lock_wait_timeout=50; -- 等待50秒超时

# 预防策略
按固定顺序访问资源
小事务尽快提交
```

```sql
-- 锁监控命令
-- MySQL
SHOW ENGINE INNODB STATUS;  -- 查看LATEST DETECTED DEADLOCK
SELECT * FROM information_schema.INNODB_TRX; -- 查看运行中事务

-- Oracle
SELECT * FROM v$locked_object;
```

| 问题现象   | 原因               | 解决方案                          |
| -------------- | -------------------- | ------------------------------------- |
| 锁等待超时 | 长事务阻塞      | 拆解事务，SET max_execution_time=5000 |
| 死锁频发   | 跨表更新顺序不一致 | 统一按主键顺序更新           |
| 行锁升级为表锁 | 无索引更新导致全表锁 | 为WHERE条件字段添加索引      |
| 分布式锁冲突 | 跨节点事务竞争 | GoldenDB：避免热点分片   OceanBase：使用LOCAL索引      |

表结构设计

| 范式              | 核心要求           | 示例（反例→正解）                              | 优缺点                    |
| ------------------- | ---------------------- | -------------------------------------------------------- | ---------------------------- |
| 1NF（原子性）  | 字段不可再分     | 地址: "北京市海淀区#中关村" → 拆分为省、市、详细地址 | 避免数据冗余，但增加JOIN成本 |
| 2NF（消除部分依赖） | 非主键字段完全依赖主键 | 订单表(订单ID,产品ID,产品价格) → 拆分为订单表+订单明细表 | 解决更新异常，但查询变复杂 |
| 3NF（消除传递依赖） | 非主键字段无传递依赖 | 员工表(工号,部门,部门电话) → 拆分为员工表+部门表 | 减少数据冗余，需维护外键 |


数据库审计

| 审计项 | 记录内容示例                                | 风险场景     |
| -------- | ------------------------------------------------- | ---------------- |
| 登录尝试 | 用户: admin, IP: 192.168.1.100, 结果: 失败  | 暴力破解攻击 |
| 数据查询 | SELECT * FROM users WHERE id=1;                   | 越权查看敏感信息 |
| 数据变更 | UPDATE salary SET amount=99999 WHERE emp_id=1001; | 恶意篡改薪资 |
| 结构变更 | DROP TABLE financial_data;                        | 破坏性操作  |

| 系统级审计类型       | 记录内容                     |
| ------------ | -------------------------------- |
| 权限变更 | GRANT DBA TO user_x;             |
| 配置修改 | ALTER SYSTEM SET audit_trail=DB; |
| 备份恢复操作 | RMAN RESTORE DATABASE;           |



数据库监控

| 维度   | 监控指标示例           | 业务影响         |
| -------- | ---------------------------- | -------------------- |
| 可用性 | 服务状态、连接成功率 | 宕机导致业务中断 |
| 性能   | QPS、TPS、平均响应延迟 | 用户体验下降   |
| 资源   | CPU、内存、磁盘I/O、网络流量 | 硬件瓶颈引发性能劣化 |
| 数据安全 | 备份状态、日志归档延迟 | 数据丢失风险   |



<h2 id="Oracle">Oracle</h2>

oracle安装

实例

```text
实例 = 内存结构（SGA） + 后台进程（Background Processes）
作用：数据库运行时的临时环境，用于管理数据文件、处理用户请求。
关键特性：
一个实例同一时间只能挂载一个数据库（非CDB架构）。
实例本身不存储数据，数据持久化在磁盘文件中（如 .dbf）。
```
| 组件                    | 功能说明                                                               |
| ------------------------- | -------------------------------------------------------------------------- |
| SGA (System Global Area)  | 共享内存区，含缓冲池（Buffer Cache）、共享池（Shared Pool）等 |
| PGA (Program Global Area) | 私有内存区，每个会话独立（排序、哈希操作）            |
| 后台进程              | DBWn（写数据文件）、LGWR（写Redo Log）、PMON（进程监控）、SMON（实例恢复） |

```sql
1、启动实例：
SQL> STARTUP NOMOUNT;  -- 启动实例（未挂载数据库）  
此时分配SGA，启动后台进程，但未关联任何数据文件。
2、挂载数据库：
SQL> ALTER DATABASE MOUNT;  -- 关联控制文件  
SQL> ALTER DATABASE OPEN;   -- 打开数据文件  
3、查看实例状态：
SQL> SELECT instance_name, status FROM v$instance;  
4、输出：
INSTANCE_NAME    STATUS  
---------------- ------------  
orcl             OPEN  
```

租户

```text
多租户架构（Multitenant） 从 Oracle 12c 引入，将传统数据库拆分为：
CDB（Container Database）：容器数据库，承载多个租户。
PDB（Pluggable Database）：可插拔数据库，每个PDB是一个独立租户。
```

| 概念   | 说明                                                               |
| -------- | -------------------------------------------------------------------- |
| CDB      | 根容器（CDB$ROOT） + 多个PDB，管理公共资源（如Undo表空间、Redo日志） |
| PDB      | 业务数据库，拥有独立的数据文件、用户、表空间（如 sales_pdb） |
| 应用容器 | 可选层，将多个PDB分组（如 hr_app 容器包含 hr_pdb1、hr_pdb2） |

```sql
1、创建CDB：
CREATE DATABASE cdb01  
  ENABLE PLUGGABLE DATABASE  
  ADMIN USER cdb_admin IDENTIFIED BY password;  
2、创建PDB租户：
-- 创建订单库PDB  
CREATE PLUGGABLE DATABASE orders_pdb  
  ADMIN USER orders_admin IDENTIFIED BY password  
  FILE_NAME_CONVERT = ('/pdbseed/', '/orders_pdb/');  
  
-- 创建用户库PDB  
CREATE PLUGGABLE DATABASE users_pdb  
  ADMIN USER users_admin IDENTIFIED BY password  
  FILE_NAME_CONVERT = ('/pdbseed/', '/users_pdb/');  
3、切换租户：
-- 连接到CDB根容器  
SQL> ALTER SESSION SET CONTAINER = cdb$root;  
  
-- 切换到orders_pdb租户  
SQL> ALTER SESSION SET CONTAINER = orders_pdb;  
4、查看租户信息：
SELECT name, open_mode FROM v$pdbs;  
5、输出：
NAME       OPEN_MODE  
---------- ----------  
ORDERS_PDB READ WRITE  
USERS_PDB  MOUNTED    -- 未打开  
```

会话

| 场景         | 会话概念     | 电话客服类比 |
| -------------- | ---------------- | ------------------ |
| 用户连接数据库 | 新建会话     | 客户拨通电话 |
| 执行SQL查询 | 会话活跃中  | 客服处理业务 |
| 半小时不操作 | 会话闲置（IDLE） | 客户沉默，客服等待 |
| 管理员踢人 | 终止会话     | 主管强制挂断电话 |
| 用户退出   | 会话正常结束 | 客户说“谢谢”后挂机 |

```sql
-- 查看所有会话（像客服中心监控大屏）
SELECT sid, serial#, username, status FROM v$session;

-- 踢掉卡住的会话（像主管强制挂断电话）
ALTER SYSTEM KILL SESSION '123,456';  -- 123是会话ID,456是序列号

-- 限制通话时长（设置自动挂断）
ALTER PROFILE default LIMIT IDLE_TIME 30;  -- 30分钟无操作自动断线
```


表空间

| 衣柜结构 | 对应表空间概念 | 作用说明                   |
| ------------ | --------------------- | ------------------------------ |
| 整个衣柜 | 数据库（Database） | 容纳所有物品的大家具 |
| 分层抽屉 | 表空间（Tablespace） | 核心！ 分类存储不同物品 |
| 抽屉里的格子 | 数据文件（Data File） | 实际存放衣服的空间（硬盘文件） |
| 衣服/裤子 | 表（Table）        | 具体数据                   |

```text
🔧 为什么需要表空间？（衣柜的妙用）

分类管理
👔 上衣抽屉：存放 用户表（比如 USER_DATA 表空间）
👖 裤子抽屉：存放 系统表（比如 SYSTEM 表空间）
🧦 内衣抽屉：存放 临时数据（比如 TEMP 表空间）
—— 避免袜子混进西装堆！
性能优化
把常穿的 当季衣服 放在容易拿的抽屉（表空间放 高速SSD）
过季衣服塞到顶层抽屉（表空间放 普通HDD）
安全隔离
贵重手表锁进 带锁抽屉（加密表空间 ENCRYPTION=ON）
孩子不能打开父母抽屉（不同用户访问不同表空间）
```

```sql
1. 创建表空间（加个新抽屉）
-- 创建一个叫「照片抽屉」的表空间（自动扩展+存放照片）
CREATE TABLESPACE photo_drawer 
  DATAFILE '/u01/oradata/photo01.dbf' SIZE 100M 
  AUTOEXTEND ON NEXT 50M;
2. 把表放进表空间（衣服入抽屉）
-- 创建「家庭相册」表，存到 photo_drawer 表空间
CREATE TABLE family_photos (
  id    NUMBER,
  photo BLOB
) TABLESPACE photo_drawer;  -- 指定抽屉！
3. 爆仓预警（抽屉满了怎么办？）
-- 查看表空间使用率（像检查抽屉剩余空间）
SELECT tablespace_name, 
       used_percent "已用%"
FROM dba_tablespace_usage_metrics;

-- 扩容抽屉：给 photo_drawer 增加一个格子（数据文件）
ALTER TABLESPACE photo_drawer 
  ADD DATAFILE '/u02/oradata/photo02.dbf' SIZE 200M;
```


权限分配

UNDO/REDO

| 功能   | REDO 日志                  | UNDO 日志                  |
| -------- | ---------------------------- | ---------------------------- |
| 本质   | 操作流水账              | 数据旧照备份           |
| 目的   | 防数据丢失（持久性） | 回滚+读一致性（隔离性） |
| 内容   | 物理操作（如“XX位置写YY值”） | 逻辑旧值（如“余额原为1000”） |
| 是否可删 | 归档后可清理           | 事务提交后延迟清理  |


ASM


归档

```bash
Oracle中的归档（Archiving） 是指将写满的重做日志文件（Redo Log）备份保存的过程，是数据库实现完整恢复和连续运行的核心机制。以下是关键要点：

归档的核心作用

# 数据恢复保障
允许数据库恢复到任意时间点（包括日志切换后的历史操作）
# 持续运行支持
避免重做日志写满后数据库挂起（归档释放日志文件可重用）
# 备份基础
所有物理备份（RMAN）依赖归档日志实现完全恢复
```

| 特性   | 归档模式 (ARCHIVELOG)  | 非归档模式 (NOARCHIVELOG) |
| -------- | -------------------------- | ------------------------- |
| 日志处理 | 写满的日志备份后标记可重用 | 日志写满后直接覆盖 |
| 恢复能力 | 支持时间点恢复（PITR） | 仅能恢复到上次备份时刻 |
| 可用性 | 日志写满不阻塞数据库 | 日志循环写满后数据库挂起 |
| 适用场景 | 生产环境（7x24小时运行） | 测试/开发环境       |

视图

在Oracle数据库中，视图（View） 是基于一个或多个表的查询结果集生成的虚拟表，不存储实际数据，而是通过SQL查询动态生成数据。

| 特性   | 视图                         | 表          |
| -------- | ------------------------------ | ------------ |
| 存储数据 | ❌ 虚拟                     | ✅ 物理存储 |
| 更新限制 | 部分可更新                | 完全可更新 |
| 性能   | 依赖基表查询性能       | 直接访问更快 |
| 索引   | 不可直接建索引（物化视图除外） | 支持索引 |


位图

段与区管理机制

```mermaid
graph TD
    A[表空间 Tablespace] --> B[段 Segment]
    B --> C[区 Extent]
    C --> D[数据块 Block]
```

```text
表空间（Tablespace）：逻辑存储容器（如USERS表空间）
段（Segment）：存储特定对象的所有数据（如表、索引段）
区（Extent）：由连续数据块组成的物理存储单元
数据块（Block）：最小I/O单元（通常8KB）
```

RMAN

```sql
1、完全恢复（介质故障）
-- 步骤1：挂载数据库
STARTUP MOUNT;
-- 步骤2：恢复数据文件
RESTORE DATABASE;
-- 步骤3：应用归档日志
RECOVER DATABASE;
-- 步骤4：打开数据库
ALTER DATABASE OPEN;

2. 时间点恢复（PITR - 误删表）
RUN {
  SET UNTIL TIME "to_date('2024-06-26 14:00:00','yyyy-mm-dd hh24:mi:ss')";
  RESTORE DATABASE;
  RECOVER DATABASE;
}
ALTER DATABASE OPEN RESETLOGS;  -- 必须重置日志

3. 单表恢复（12c+）
-- 将表恢复到指定时间点（无需全库恢复）
RECOVER TABLE scott.employees 
  UNTIL TIME '2024-06-26 14:00:00'
  AUXILIARY DESTINATION '/tmp';
```
| 能力   | RMAN                   | expdp/impdp      | OS拷贝 |
| -------- | ---------------------- | ---------------- | -------- |
| 备份类型 | 物理备份（块级） | 逻辑备份（行级） | 物理备份 |
| 增量备份 | ✅ 块级增量       | ❌              | ❌      |
| 恢复粒度 | 数据库/表空间/数据文件 | 全库/表       | 仅全库 |
| 断点续传 | ✅                    | ❌              | ❌      |
| 压缩加密 | ✅                    | ✅ (部分)     | ❌      |

导入导出工具

AWR/ASH报告分析

Listener配置与管理

TNS服务名解析配置

动态/静态注册机制

多监听与端口绑定

RAC

节点与集群服务管理

共享存储与集群文件系统配置

心跳机制与故障转移策略

DG备库同步机制

<h2 id="Mysql">Mysql</h2> 

innoDB
```mermaid
graph LR
    A[客户端SQL] --> B[SQL接口]
    B --> C[查询优化器]
    C --> D[存储引擎层]
    D -->|读写| E[缓冲池 Buffer Pool]
    E -->|刷脏| F[磁盘数据文件 .ibd]
    D -->|日志| G[Redo Log]
    D -->|回滚| H[Undo Log]
```

<h2 id="国产改造">国产改造</h2> 

各数据库特点/架构

| 维度     | Oracle                | MySQL                    | OceanBase                      | GoldenDB                       |
| ---------- | --------------------- | ------------------------ | ------------------------------ | ------------------------------ |
| 架构模型 | 集中式/共享存储 | 单机/主从复制      | 原生分布式（LSM-Tree）  | 原生分布式（分片集群） |
| 扩展性  | 垂直扩展（Scale-Up） | 有限水平扩展（分库分表） | 在线水平扩展（1:0.9线性比） | 动态分片扩容（哈希/范围分片）9|
| 高可用  | RAC（多实例共享存储） | 主从复制（半同步） | Paxos多副本（RPO=0, RTO<30s） | gSync多活（异地容灾） |
| 存储引擎 | 行存储（B-Tree） | InnoDB（B+Tree）       | LSM-Tree（高压缩）    | 行列混合（HTAP优化） |
| 事务一致性 | 强一致（ACID）   | 强一致（ACID）      | 分布式强一致（全局事务） | 分布式强一致（透明二阶段提交） |

数据导入/导出

| 特性       | Oracle                           | MySQL                    | OceanBase                        | GoldenDB                       |
| ------------ | -------------------------------- | ------------------------ | -------------------------------- | ------------------------------ |
| 核心工具 | Data Pump (expdp/impdp)、EXP/IMP | mysqldump、mysql 命令 | ODC (OceanBase Developer Center) | dbtool、batchload.py          |
| 支持格式 | DMP、SQL、CSV、PDE            | SQL、CSV                | SQL、CSV、ZIP                  | CSV、SQL                      |
| 是否支持并行 | ✅ (Data Pump)                  | ❌ (需手动分片)    | ✅ (ODC 全局快照)           | ✅ (分片并行导入)       |
| 大文件处理 | ✅ (表空间导出)            | ✅ (压缩导出)       | ✅ (文件自动切分)         | ✅ (分片存储)             |
| 跨平台兼容性 | ✅ (DMP 二进制通用)        | ✅ (SQL 文本通用)   | ✅ (CSV/SQL 格式)             | ✅ (CSV 中介)               |
| 典型场景 | 全库迁移、表空间迁移   | 中小规模备份、跨版本迁移 | 分布式环境数据同步、HTAP 负载 | 金融核心系统迁移、分片数据管理 |

备份/恢复

| 特性       | Oracle                        | MySQL                     | OceanBase                   | GoldenDB                     |
| ------------ | ----------------------------- | ------------------------- | --------------------------- | ---------------------------- |
| 核心备份工具 | Data Pump (expdp/impdp)、RMAN | mysqldump、xtrabackup    | ODC（图形化）、物理备份命令 | dbtool、restore.py          |
| 备份类型 | 逻辑备份（DMP）、物理备份 | 逻辑备份（SQL）、物理备份 | 物理备份、逻辑备份 | 全量/增量备份、Binlog 日志 |
| 恢复粒度 | 全库、表空间、表      | 全库、单库、单表  | 租户、库、表级别    | 分片（DN）、单库、单表 |
| 关键特性 | 并行导出、加密、压缩 | 基于时间点恢复（Binlog） | 分布式一致性、异地备份 | 分片感知、活跃事务一致性处理 |

高可用

| 维度       | Oracle                         | MySQL                   | OceanBase            | GoldenDB                 |
| ------------ | ------------------------------ | ----------------------- | -------------------- | ------------------------ |
| 核心架构 | 共享存储 (RAC) + 逻辑复制 (DG) | 主从复制 + Paxos (MGR) | Paxos 多副本 + 仲裁 | 分片分组 (gTank) + gSync |
| 数据一致性 | 强一致 (DG 最大可用模式) | 最终一致 → 强一致 (MGR) | 强一致 (多数派确认) | 强一致 (分片内)    |
| 故障恢复速度 | RTO < 30秒 (RAC)              | RTO < 10秒 (MGR)       | RTO < 8秒           | RTO < 10秒 (分片切换) |
| 容灾能力 | 跨机房 (DG)                 | 跨集群异步 (ClusterSet) | 三地五中心部署 | 本地/同城/异地三级架构 |
| 适用场景 | 传统金融核心             | 互联网中型应用   | 分布式金融/HTAP 场景 | 银行核心系统迁移 |

分布式

| 维度     | Oracle                        | MySQL                      | OceanBase                   | GoldenDB               |
| ---------- | ----------------------------- | -------------------------- | --------------------------- | ---------------------- |
| 是否分布式 | ❌ 集中式（扩展方案伪分布式） | ❌ 单机（需分库分表） | ✅ 原生分布式         | ✅ 原生分布式    |
| 实现方式 | RAC+Data Guard（共享存储） | 中间件（如ShardingSphere） | 多副本Paxos+LSM-Tree     | 分片集群+GTM事务管理器 |
| 数据分片 | 表分区（非分布式）   | 手动分库分表         | 自动分区（HASH/RANGE） | 分片键路由（业务感知） |
| 事务一致性 | 强一致（单机）         | 弱一致（主从延迟） | 强一致（Multi-Paxos）  | 强一致（2PC+GTM） |
| 扩展性  | 垂直扩展（Scale-Up）    | 水平扩展（复杂）   | 在线水平扩展（1:0.9线性比） | 动态分片扩容     |
| 典型场景 | 传统金融核心            | 中小Web应用            | 金融HTAP/高并发        | 银行核心系统迁移 |

集群部署

| 特性     | Oracle RAC         | MySQL PXC        | OceanBase             | GoldenDB            |
| ---------- | ------------------ | ---------------- | --------------------- | ------------------- |
| 架构本质 | 共享存储       | 多主同步复制 | 原生分布式多副本 | 分片集群 + 容器化 |
| 数据一致性 | 强一致（单集群） | 强一致（多主） | 分布式强一致（Paxos） | 分片内强一致（GTM） |
| 扩展性  | 垂直扩展       | 水平扩展（受限） | 在线水平扩展    | 动态分片裂变  |
| 容灾粒度 | 节点级          | 节点级        | 机房/城市级      | 分片级           |
| 部署复杂度 | 高（依赖共享存储） | 中（脚本化） | 中（ODC 工具辅助） | 低（云管平台集成） |


<h2 id="VMWare/FC">VMWare/FC</h2> 

1、虚拟网络

```bash
# 桥接模式（Bridged Mode）

核心原理：虚拟机通过虚拟交换机（VMnet0）直接桥接到主机的物理网卡，获得与宿主机同一网段的独立IP地址，成为局域网中的“平等成员”。

IP分配：由物理网络的DHCP服务器分配，或手动配置静态IP（需与宿主机同网段）。

网络可见性：
✅ 虚拟机可访问局域网内所有设备及互联网；
✅ 局域网内其他设备可直接访问虚拟机（如通过SSH、Web服务）。

安全性：较低，虚拟机完全暴露在局域网中。

适用场景：
虚拟机需作为独立服务器对外提供服务（如Web服务器、数据库）；
局域网IP资源充足且允许新设备接入。

配置要点：
需确保主机物理网卡启用“VMware Bridge Protocol”3；
若主机切换网络（如从有线转无线），可勾选“复制物理网络连接状态”保持IP稳定3。

# NAT模式（Network Address Translation Mode）

核心原理：虚拟机通过虚拟网卡VMnet8连接到虚拟NAT设备，共享宿主机的公网IP访问外部网络。外部请求需经端口映射才能访问虚拟机。
特点与行为：

IP分配：由VMware内置DHCP服务分配私有IP（如192.168.xxx.xxx）
。
网络可见性：
✅ 虚拟机可单向访问互联网及局域网其他设备；
❌ 外部设备默认无法访问虚拟机（除非配置端口转发）。

安全性：中等，虚拟机隐藏于宿主机之后。

适用场景：
多虚拟机需同时上网且IP资源紧张（如开发测试环境）；
无需对外提供服务，仅需基础网络访问。

配置要点：
无需手动设置IP（默认DHCP自动分配）；

端口映射步骤：VMware虚拟网络编辑器 → NAT设置 → 添加端口转发规则。

# 仅主机模式（Host-Only Mode）

核心原理：虚拟机通过虚拟网卡VMnet1与宿主机组成封闭私有网络，完全隔离外部网络。

特点与行为：
IP分配：由VMware内置DHCP分配私有IP（或手动设置），范围与VMnet1子网一致（如192.168.137.xxx）。

网络可见性：
✅ 虚拟机可与宿主机及同一Host-Only网络的其他虚拟机通信；
❌ 无法访问互联网或外部设备（除非宿主机开启网络共享或代理）。

安全性：最高，完全隔离外部网络。

适用场景：
安全测试、漏洞实验等需严格隔离的环境；
内部网络通信测试（如集群软件调试）。

配置要点：
若需联网：在宿主机网络设置中启用“Internet连接共享”，将物理网卡共享至VMnet。
```
| 特性         | 桥接模式          | NAT模式             | 仅主机模式       |
| -------------- | --------------------- | --------------------- | --------------------- |
| IP地址来源 | 物理网络DHCP/手动配置 | VMware DHCP（私有IP） | VMware DHCP（私有IP） |
| 访问互联网 | ✅ 直接访问      | ✅ 通过宿主机NAT转换 | ❌ 默认不可（需共享） |
| 外部访问虚拟机 | ✅ 直接访问      | ❌ 需端口映射   | ❌ 不可访问      |
| 虚拟机间通信 | ✅（同网段）    | ✅（同NAT网络） | ✅（同Host-Only网络） |
| 安全性      | 低（暴露于局域网） | 中（隐藏于NAT后） | 高（完全隔离） |
| 典型场景   | 对外服务的服务器 | 开发/测试环境上网 | 安全测试/内部网络实验 |




<h2 id="Docker/K8s">Docker/K8s</h2> 
<h2 id="主机安全">主机安全</h2> 
<h2 id="终端管理">终端管理</h2> 

1、域控

```bash
# 核心概念

定义与作用:
Active Directory (AD)：微软开发的目录服务，用于集中管理网络资源（用户、计算机、策略）。
域（Domain）：AD 的基本管理单元，是安全边界和策略应用边界的集合。

核心价值：
统一身份认证：单点登录（SSO）访问所有授权资源。
集中策略管理：通过组策略（GPO）批量配置安全/软件设置。
资源组织与发现：全局编录（GC）快速搜索跨域对象。
```

| 术语        | 说明                                                              |
| ------------- | ------------------------------------------------------------------- |
| 域控制器 (DC) | 运行 AD DS 服务的服务器，存储域数据库（ntds.dit），处理认证请求。 |
| 林 (Forest)  | 由一个或多个域组成的最大安全边界，共享架构（Schema）和全局编录。 |
| 树 (Tree)    | 具有连续 DNS 命名空间的域集合（如 parent.com → child.parent.com）。 |
| 信任 (Trust) | 域间关系，允许跨域认证（如：单向信任、双向信任、林信任）。 |
| OU (组织单元) | 容器对象，用于分层管理用户/计算机/组，是组策略的最小应用单位。 |
| 组策略 (GPO) | 批量配置用户/计算机的规则集合（如密码策略、软件部署）。 |

```mermaid
graph TD
    A[林 Forest] --> B[域树 Tree 1]
    A --> C[域树 Tree 2]
    B --> D[域 Domain A]
    B --> E[域 Domain B]
    D --> F[OU 部门]
    F --> G[子OU 技术组]
    G --> H[用户]
    G --> I[计算机]
```
身份认证

```mermaid
sequenceDiagram
    用户->>DC: 发送用户名/密码
    DC-->>用户: 返回 TGT（票据授予票据）
    用户->>DC: 用 TGT 请求服务票据（如访问文件服务器）
    DC-->>用户: 返回服务票据
    用户->>文件服务器: 提交服务票据
    文件服务器-->>用户: 授权访问
```

组策略

| 策略       | 作用                      | 示例配置项                        |
| ------------ | --------------------------- | -------------------------------------- |
| 密码策略 | 强制密码复杂度       | 最小长度8，90天更换            |
| 软件部署 | 自动安装/卸载应用   | 推送Chrome到市场部OU             |
| 文件夹重定向 | 将桌面/文档同步到文件服务器 | \\FS01\UserProfiles\%username%         |
| 登录脚本 | 用户登录时自动执行 | 映射网络驱动器 net use Z: \\FS01\Share |
| 策略       | 作用                      | 示例配置项                        |


2、准入

```bash
准入控制（Network Access Control, NAC）是网络安全的核心边界防御机制，其核心原理可概括为：“未知设备不入网，非标终端不通行”。它通过预连接策略验证设备安全状态，实现网络访问的动态授权。

三大核心原理：
认证（Authentication）
授权（Authorization）
合规检查（Posture Assessment）
```

### 认证（Authentication）

802.1x协议
```mermaid
sequenceDiagram
    终端->>交换机: EAPOL-Start
    交换机->>RADIUS服务器: RADIUS Access-Request
    RADIUS服务器-->>终端: EAP Challenge
    终端-->>RADIUS服务器: EAP Response (证书/账号密码)
    RADIUS服务器-->>交换机: Access-Accept + VLAN策略
    交换机->>终端: 授权网络访问
```
非802.1X方案：

Web认证门户：访客设备浏览器重定向至认证页

MAC旁路认证：打印机/IoT设备白名单

### 授权（Authorization）

目的：动态分配访问权限

| 策略类型 | 控制粒度         | 应用场景                                            |
| -------- | -------------------- | ------------------------------------------------------- |
| VLAN划分 | 隔离不同安全等级终端 | 员工VLAN（10.1.0.0/16） vs 访客VLAN（192.168.100.0/24） |
| ACL过滤 | 限制IP/端口访问 | 研发部禁止访问外网存储服务                 |
| 带宽限制 | QoS保障关键业务 | 视频会议流量优先于P2P下载                    |


3、桌管

4、虚拟桌面

```bash
虚拟桌面（Virtual Desktop）是一种将传统PC的桌面环境（操作系统、应用程序、用户数据）从本地设备迁移到集中式服务器或云端，通过网络交付给终端用户的计算模型。其核心思想是“集中计算，分布显示”，用户通过瘦客户端、PC或移动设备远程访问完整的桌面体验。
虚拟桌面通过服务器虚拟化技术在数据中心创建多个虚拟机（VM），每个VM运行独立的桌面操作系统（如Windows/Linux）。用户通过远程桌面协议（如RDP、PCoIP、SPICE）访问这些虚拟机，实现与传统PC无差别的操作体验。
```

| 维度   | 传统PC               | 虚拟桌面               |
| -------- | ---------------------- | -------------------------- |
| 数据安全 | 数据分散在终端，易泄露 | 数据集中存储，加密隔离 |
| 运维成本 | 逐台维护，成本高昂 | 集中管理，批量部署与更新 |
| 移动性 | 依赖特定设备     | 多终端接入（PC/平板/手机） |
| 资源弹性 | 硬件固定，升级困难 | 动态分配CPU/内存/存储 |

```mermaid
graph TB
    A[用户终端] -->|连接协议| B[管理服务器]
    B --> C[虚拟桌面池]
    C --> D[存储系统]
    D --> E[网络基础设施]
    B --> F[身份认证平台]
```

| 架构 | 计算位置 | 存储位置 | 优势                 | 典型场景        |
| ---- | ---------- | ------------ | ---------------------- | ------------------- |
| VDI  | 集中服务器 | 集中存储 | 数据安全高，移动性强 | 金融/远程办公 |
| IDV  | 本地终端 | 集中+本地 | 外设兼容性好，断网可用 | 制造业/实验室 |
| TCI  | 本地终端 | 本地虚拟磁盘 | 极致外设兼容性  | 3D设计/高性能工作站 |
| RDS  | 集中服务器 | 集中存储 | 成本低，部署简单 | 呼叫中心/图书馆终端 |

```mermaid
sequenceDiagram
    用户->>管理服务器: 登录认证（AD/LDAP）
    管理服务器->>虚拟桌面池: 请求可用桌面
    虚拟桌面池-->>管理服务器:  分配虚拟机VM01
    管理服务器->>用户:  返回VM01连接信息
    用户->>VM01: 通过RDP连接
    VM01->>存储系统: 加载用户配置文件
    VM01-->>用户: 交付桌面界面
```

<h2 id="Linux/Kylin">Linux/Kylin</h2> 
1、linux文件目录

| 目录 | 用途                         | 关键内容示例            |
| ------ | ------------------------------ | ----------------------------- |
| /      | 根目录，所有目录的起点 |                               |
| /bin   | 基础命令（所有用户可用） | ls, cp, cat                   |
| /sbin  | 系统管理命令（仅 root 可用） | fdisk, ifconfig, iptables     |
| /etc   | 系统配置文件             | passwd, fstab, nginx.conf     |
| /var   | 动态变化数据             | log/, lib/, www/              |
| /tmp   | 临时文件（自动清理） |                               |
| /home  | 普通用户家目录          | user1/, user2/                |
| /root  | root 用户家目录           |                               |
| /usr   | 用户程序与资源（只读） | bin/, lib/, include/          |
| /opt   | 第三方软件安装目录    | google/chrome/                |
| /dev   | 设备文件                   | sda, ttyS0, null              |
| /proc  | 内核和进程信息（虚拟文件系统） | cpuinfo, meminfo, 1/（PID 1） |
| /sys   | 系统硬件信息（虚拟文件系统） | class/, devices/              |
| /boot  | 启动文件                   | vmlinuz, initramfs, grub/     |
| /mnt   | 临时挂载点                |                               |
| /media | 可移动设备挂载点       | cdrom/, usb/                  |
2、重要配置文件
```bash
/etc/passwd       # 用户账户信息
/etc/shadow       # 加密密码（仅root可读）
/etc/group        # 用户组信息
/etc/hosts        # 本地域名解析
/etc/fstab        # 文件系统挂载配置
/etc/resolv.conf  # DNS服务器配置
```
3、软件包管理
```bash
Debian/Ubuntu	
apt install nginx	# 安装软件
apt remove nginx	# 卸载软件
apt update	# 更新软件源列表
apt upgrade	# 升级所有软件
RHEL/CentOS	
yum install httpd	# 安装软件
yum remove httpd	# 卸载软件
yum update	# 升级所有软件
通用	
dpkg -i pkg.deb	# 手动安装Deb包
rpm -ivh pkg.rpm	# 手动安装RPM包
```
4、服务管理
```bash
# 服务操作
systemctl start nginx    # 启动服务
systemctl stop nginx     # 停止服务
systemctl restart nginx  # 重启服务
systemctl reload nginx   # 重载配置（不中断）
systemctl enable nginx   # 设置开机自启
systemctl disable nginx  # 禁用开机自启

# 服务状态查看
systemctl status nginx   # 详细状态
systemctl is-active nginx # 是否运行中
journalctl -u nginx -f   # 实时查看日志
```
5、日志系统
```mermaid
graph LR
A[应用程序] -->|syslog API| B(rsyslog)
B --> C["/var/log/messages"]
B --> D["/var/log/secure"]
B --> E["/var/log/cron"]
F[内核] -->|printk| G(klogd)
G --> B
H(auditd) --> I["/var/log/audit/audit.log"]
```
| 日志文件             | 记录内容                  |
| ------------------------ | ----------------------------- |
| /var/log/messages        | 常规系统消息（CentOS/RHEL） |
| /var/log/syslog          | 常规系统消息（Debian/Ubuntu） |
| /var/log/auth.log        | 认证日志（登录、sudo） |
| /var/log/secure          | 安全日志（RHEL系）     |
| /var/log/kern.log        | 内核日志                  |
| /var/log/audit/audit.log | 审计日志（需auditd服务） |
6、性能调优

| 参数                       | 默认值 | 优化值 | 作用             |
| ---------------------------- | ------ | ------- | ------------------ |
| net.core.somaxconn           | 128    | 4096    | TCP连接队列长度 |
| net.ipv4.tcp_tw_reuse        | 0      | 1       | 重用TIME_WAIT连接 |
| vm.swappiness                | 60     | 10      | 减少Swap使用   |
| fs.file-max                  | 79322  | 2097152 | 最大文件句柄数 |
| net.ipv4.tcp_max_syn_backlog | 128    | 8192    | SYN队列长度    |
| vm.dirty_ratio               | 20     | 10      | 减少写缓冲脏页比例 |
<h2 id="Windows">Windows</h2> 
1、用户与组

| 操作类型 | 图形界面路径               | 命令行工具 | 关键命令示例                      |
| ---------- | -------------------------------- | -------------- | --------------------------------------- |
| 创建用户 | 计算机管理 → 本地用户和组 → 用户 | net user       | net user John P@ssw0rd /add             |
| 删除用户 | 同上                           | 同上         | net user John /del                      |
| 修改密码 | 同上 → 右键用户 → 设置密码 | 同上         | net user John * (交互式修改)       |
| 加入用户组 | 用户属性 → 隶属于 → 添加 | net localgroup | net localgroup Administrators John /add |

2、组策略管理（GPO）

应用场景：统一配置域内计算机（如密码策略、软件部署）

操作路径：
```bash
gpedit.msc  # 本地组策略编辑器
计算机配置/用户配置 → 策略模板
```
3、服务与进程管理

| 操作       | 图形界面            | 命令行（sc）               | PowerShell                                       |
| ------------ | ----------------------- | ------------------------------- | ------------------------------------------------ |
| 启动服务 | services.msc → 右键启动 | sc start "Spooler"              | Start-Service -Name Spooler                      |
| 停止服务 | 同上 → 停止       | sc stop "Spooler"               | Stop-Service -Name Spooler                       |
| 设置启动类型 | 属性 → 启动类型 | sc config "Spooler" start= auto | Set-Service -Name Spooler -StartupType Automatic |
```cmd

进程监控与终止
任务管理器：Ctrl+Shift+Esc → 查看CPU/内存占用
命令行终结进程：
tasklist | findstr "malware.exe"  # 查找进程ID
taskkill /F /PID 1234             # 强制终止进程
资源监视器：resmon.exe（分析进程的文件/网络活动）
```

4、事件日志

| 日志类型 | 路径                          | 主要用途          |
| ------------ | ------------------------------- | --------------------- |
| 系统日志 | 事件查看器 → Windows日志 → 系统 | 服务启动失败/硬件错误 |
| 应用程序日志 | 同上 → 应用程序         | 软件崩溃/兼容性问题 |
| 安全日志 | 同上 → 安全               | 登录审计/权限变更记录 |
| Setup日志  | 同上 → Setup                | 系统更新/补丁安装问题 |

5、本地安全策略

本地安全策略（secpol.msc）
| 配置项    | 路径                  | 企业应用                             |
| ------------ | ----------------------- | ---------------------------------------- |
| 账户策略 | 账户策略 → 密码策略 | 强制密码复杂度+最长使用期限 |
| 用户权限分配 | 本地策略 → 用户权限分配 | 禁止普通用户关机（Shut down the system） |
| 安全审计 | 高级审计策略 → 审计策略 | 启用文件删除审计           

| 维度     | 组策略（GPO）              | 本地安全策略           |
| ---------- | ------------------------------- | ---------------------------- |
| 作用范围 | 支持域/OU/本地             | 仅本地计算机           |
| 配置颗粒度 | 可配置软件部署/IE设置等非安全项 | 专注账户/审计/权限等安全设置 |
| 优先级  | 域策略 > OU策略 > 本地策略 | 属于本地策略的一部分 |

<h2 id="服务器基础">服务器基础</h2> 

1、部署流程

```mermaid
graph LR
A[规划] --> B[硬件上架]
B --> C[固件/驱动更新]
C --> D[操作系统安装]
D --> E[网络配置]
E --> F[安全加固]
F --> G[应用部署]
G --> H[监控接入]
```

2、CPU

| 术语   | 说明                                | 计算公式                    |
| -------- | ------------------------------------- | ------------------------------- |
| 物理CPU | 插在主板上的实体处理器     |                                 |
| 物理核心 | 单个CPU内的独立计算单元     |                                 |
| 逻辑CPU | 通过超线程（Hyper-Threading）虚拟的核 | 逻辑CPU数 = 物理核心数 × 线程数 |

3、存储

| 类型   | 原理          | 接口   | 适用场景      | 寿命/性能          |
| -------- | --------------- | -------- | ----------------- | ---------------------- |
| HDD      | 机械磁头读写 | SATA/SAS | 冷数据存储   | 寿命长，IOPS低（<200） |
| SATA SSD | 闪存芯片    | SATA     | 普通应用服务器 | DWPD 0.3-1，IOPS 50K  |
| NVMe SSD | PCIe通道直连CPU | M.2/U.2  | 数据库/高性能计算 | DWPD 1-3，IOPS 500K+  |
| SAS SSD  | 企业级闪存 | SAS 12Gb | 企业级存储阵列 | DWPD 3-10，IOPS 200K  |

4、内存

| 参数  | 说明                  | 示例值   | 影响               |
| ------- | ----------------------- | ----------- | -------------------- |
| 容量  | 单条内存大小      | 32GB        | 决定并发处理能力 |
| 频率  | 数据传输速度      | DDR4-3200   | 高频提升CPU-内存带宽 |
| 时序  | 延迟参数（CL-tRCD-tRP） | CL16-18-18  | 低时序减少延迟 |
| ECC支持 | 错误校验纠正      | ECC/Non-ECC | 关键业务必需   |

5、带外管理

| 技术 | 厂商   | 访问方式   | 核心功能                 |
| ----- | -------- | -------------- | ---------------------------- |
| iDRAC | Dell     | Web/https://IP | 硬件监控、远程控制、日志导出 |
| iLO   | HPE      | Java/iLO App   | 虚拟KVM、电源管理、固件更新 |
| BMC   | 通用标准 | IPMI工具     | 基础硬件监控           |

6、排障流程

```mermaid
graph TD
A[故障现象] --> B[指示灯状态]
B --> C{"硬件/软件？"}
C -->|硬件| D[查看BMC/iLO日志]
C -->|软件| E[分析系统日志]
D --> F[定位故障部件]
E --> G[检查服务状态]
F --> H[更换硬件]
G --> I[修复配置]
```


<h2 id="网络基础">网络基础</h2> 

1、TCP/IP四层模型

| 层级     | 功能                 | 核心协议              | 传输单元  | 设备示例       |
| ---------- | ---------------------- | ------------------------- | ------------- | ------------------ |
| 应用层  | 提供用户接口和服务 | HTTP, FTP, DNS, SMTP, SSH | 数据流     | 浏览器、邮件客户端 |
| 传输层  | 端到端连接、可靠性保障 | TCP, UDP                  | 段（Segment） | 防火墙、负载均衡器 |
| 网络层  | 寻址和路由选择  | IP, ICMP, ARP, OSPF       | 包（Packet） | 路由器          |
| 网络接口层 | 物理传输、帧封装 | Ethernet, Wi-Fi, PPP      | 帧（Frame） | 交换机、网卡 |

```bash
# 应用层（Application Layer）
作用：直接面向应用程序，提供网络服务接口

协议示例：
HTTP：网页传输（GET /index.html）
DNS：域名解析（将 www.baidu.com → 180.101.49.12）
SSH：加密远程登录（ssh user@192.168.1.1）

数据单元：原始数据流（如 JSON 文本、图片二进制流）

# 传输层（Transport Layer）
作用：建立端到端连接，保障数据传输可靠性

核心协议对比：
特性	TCP	UDP
连接方式	面向连接（三次握手）	无连接
可靠性	丢包重传、数据排序	不保证可靠传输
速度	慢（需确认机制）	快
头部大小	20字节	8字节
适用场景	网页、邮件、文件传输	视频流、DNS查询、游戏数据

端口号：标识应用程序（如 80→HTTP，443→HTTPS）

# 网络层（Internet Layer）
作用：逻辑寻址（IP地址）和路由选择

核心协议：
IP：无连接的数据包传输（IPv4/IPv6）
ICMP：网络诊断（ping、traceroute）
ARP：IP地址 → MAC地址解析（局域网通信基础）

IP 地址示例：
IPv4：192.168.1.100（32位，点分十进制）
IPv6：2001:0db8:85a3::8a2e:0370:7334（128位，十六进制）

# 网络接口层（Network Interface Layer）
作用：物理介质访问、帧封装/解封装

核心技术：
MAC 地址：硬件唯一标识（如 00:1A:C2:7B:00:47）

以太网帧结构：
| 目标MAC (6B) | 源MAC (6B) | 类型 (2B) | 数据 (46-1500B) | CRC (4B) |
MTU：最大传输单元（以太网默认1500字节）

```

2、常见协议

网络服务协议

| 协议 | 端口 | 传输层 | 用途                 | 安全建议             |
| ------ | ---- | ------- | ---------------------- | ------------------------ |
| HTTP   | 80   | TCP     | 网页传输（明文） | 必须升级HTTPS        |
| HTTPS  | 443  | TCP     | 加密网页传输     | 定期更新TLS证书    |
| DNS    | 53   | UDP/TCP | 域名解析           | 启用DNSSEC防劫持    |
| SSH    | 22   | TCP     | 加密远程管理     | 禁用密码登录，用密钥认证 |
| Telnet | 23   | TCP     | 明文远程登录（危险！） | 生产环境禁用       |
| Ping   | -    | ICMP    | 网络连通测试     | 限制ICMP速率防洪水攻击 |

文件传输协议

| 协议 | 端口   | 传输层 | 用途                | 安全加固方法      |
| ---- | ----- | ------- | --------------------- | ----------------------- |
| FTP  |   21(控制)      20(数据)| TCP     | 文件传输（明文） | 改用SFTP/FTPS         |
| SFTP | 22       | TCP     | 基于SSH的加密文件传输 | 限制用户目录（Chroot） |
| FTPS | 989/990  | TCP     | FTP over TLS          | 强制使用TLS 1.2+    |
| NFS  | 2049     | TCP/UDP | 网络文件共享    | 用Kerberos认证（NFSv4） |
| SMB  | 445      | TCP     | Windows文件共享   | 启用SMB加密         |

邮件协议

| 协议   | 端口 | 加密端口 | 用途               | 部署建议        |
| -------- | ---- | -------- | -------------------- | ------------------- |
| SMTP     | 25   | 465/587  | 邮件发送         | 端口587启用STARTTLS |
| POP3     | 110  | 995      | 收邮件（下载到本地） | 强制使用SSL     |
| IMAP     | 143  | 993      | 收邮件（服务器存储） | 默认禁用明文端口 |
| Exchange | 443  | -        | MAPI over HTTPS      | 仅开放HTTPS端口 |

数据库协议

| 数据库  | 默认端口 | 传输层 | 暴露风险                | 防护措施             |
| ---------- | -------- | ------ | --------------------------- | ------------------------ |
| MySQL      | 3306     | TCP    | SQL注入/未授权访问   | 限制IP白名单 + SSL加密 |
| PostgreSQL | 5432     | TCP    | 漏洞利用（如CVE-2019-9193） | 启用SCRAM认证        |
| Redis      | 6379     | TCP    | 未授权访问导致勒索 | 绑定127.0.0.1 + 设置密码 |
| Oracle     | 1521     | TCP    | TNS劫持攻击             | 配置sqlnet.ora加密   |

3、TCP连接过程

| 字段 | 首次握手（SYN） | 第二次握手（SYN+ACK） | 第三次握手（ACK） |
| ---- | --------------- | --------------------- | ----------------- |
| SYN  | 1               | 1                     | 0                 |
| ACK  | 0               | 1                     | 1                 |
| Seq  | x（随机初始化） | y（随机初始化） | x+1               |
| Ack  | 0               | x+1                   | y+1          
|Win	|客户端窗口大小|	服务端窗口大小|	客户端窗口大小|

| 报文     | 标志位   | 序列号 | 确认号 | 状态变化            |
| ---------- | ----------- | ------- | ------- | ----------------------- |
| 第一次挥手 | FIN=1       | Seq=u   | Ack=v   | A: ESTAB→FIN_WAIT_1   |
| 第二次挥手 | ACK=1       | Seq=v   | Ack=u+1 | B: ESTAB→CLOSE_WAIT   |
| 第三次挥手 | FIN=1,ACK=1 | Seq=w   | Ack=u+1 | B: CLOSE_WAIT→LAST_ACK |
| 第四次挥手 | ACK=1       | Seq=u+1 | Ack=w+1 | A: FIN_WAIT_2→TIME_WAIT |

```bash
# 为什么是三次握手
防止历史连接初始化：若客户端发出的旧SYN报文因网络延迟晚到，服务端响应后，客户端可根据上下文判断并发送RST终止旧连接（两次握手无法实现此机制）。

# 为什么是四次挥手

TCP 是全双工协议，每个方向需独立关闭：
主动方发 FIN → 关闭发送通道（仍可接收数据）
被动方先 ACK → 确认收到关闭请求
被动方发 FIN → 关闭自身发送通道
主动方 ACK → 确认最终关闭
```

4、拥塞与流量控制

```bash
# 流量控制：滑动窗口

接收方通过 TCP 头部的 Window Size 字段通告剩余缓冲区大小（单位：字节）
发送方根据窗口值动态调整发送速率（发送窗口 ≤ 接收窗口）

零窗口问题与解决
现象：接收方缓冲区满 → 通告 Win=0
探活机制：发送方启动 持续定时器（Persist Timer），定时发送 ZWP（Zero Window Probe） 报文（1字节数据），检测窗口恢复情况。
```
拥塞控制 

| 算法   | 触发条件    | 行为                                | 适用场景     |
| -------- | --------------- | ------------------------------------- | ---------------- |
| 慢启动 | 连接初始化 | 窗口呈指数增长（cwnd *= 2）  | 新连接建立  |
| 拥塞避免 | cwnd ≥ ssthresh | 窗口线性增长（cwnd += 1）     | 稳定传输阶段 |
| 快速重传 | 收到3个重复ACK | 立即重传丢失包，不等待超时 | 轻微丢包     |
| 快速恢复 | 快速重传后 | cwnd = ssthresh + 3，进入拥塞避免阶段 | 配合快速重传使用 |

5、OSI协议

| 层级        | 功能描述                | 代表协议/技术                            | 数据传输单元 | 设备示例       |
| ------------- | --------------------------- | ---------------------------------------------- | ------------- | ------------------ |
| 1. 物理层  | 比特流传输（电信号/光信号） | RS-232, RJ45, 光纤, IEEE 802.3（以太网物理层） | 比特（Bit） | 集线器、中继器 |
| 2. 数据链路层 | 帧封装、MAC寻址、差错控制 | 以太网（Ethernet II）, PPP, MAC地址, VLAN | 帧（Frame） | 交换机、网桥 |
| 3. 网络层  | 逻辑寻址（IP）、路由选择 | IP, ICMP, ARP, OSPF, BGP                       | 包（Packet） | 路由器          |
| 4. 传输层  | 端到端连接、可靠性保障 | TCP, UDP, TLS/SSL                              | 段（Segment） | 防火墙、负载均衡器 |
| 5. 会话层  | 建立/管理/终止会话  | NetBIOS, RPC, SSH隧道管理                  | 数据（Data） | （通常由软件实现） |
| 6. 表示层  | 数据格式转换、加密/压缩 | SSL/TLS（加密）, JPEG, MPEG, ASCII         | 数据（Data） | （软件库实现） |
| 7. 应用层  | 用户接口、网络服务 | HTTP, FTP, DNS, SMTP, SSH                      | 数据（Data） | 应用程序       |

| 层级     | 对应OSI层             | 核心协议            |
| ---------- | ------------------------ | ----------------------- |
| 网络接口层 | 物理层 + 数据链路层 | Ethernet, Wi-Fi, ARP    |
| 网络层  | 网络层                | IP, ICMP, BGP           |
| 传输层  | 传输层                | TCP, UDP, QUIC          |
| 应用层  | 会话层 + 表示层 + 应用层 | HTTP, DNS, TLS/SSL, RTP |

| 维度      | OSI模型                    | TCP/IP模型                  |
| ----------- | ---------------------------- | ----------------------------- |
| 设计目标 | 理论通用框架（理想化） | 解决实际问题（源于ARPANET） |
| 层级结构 | 严格七层，边界清晰  | 四层，灵活实用         |
| 协议绑定 | 未指定具体协议        | 与IP/TCP/UDP等协议强绑定 |
| 实际影响力 | 学术标准，用于教学和理论分析 | 互联网运行基础         |
| 会话/表示层 | 独立定义会话管理和数据格式 | 合并到应用层（如TLS处理加密） |

