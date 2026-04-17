# MkDocs Docker 部署到 Linux 虚拟机全流程

本文档用于把当前仓库部署到云服务器厂商提供的 Linux 虚拟机上，并通过 Docker 运行，使站点可以通过以下地址访问：

- http://VM_IP:8493

同时，这套方案会在宿主机上通过定时任务定期拉取 GitHub 仓库最新内容，并自动重建容器，从而完成网页更新。

## 1. 部署方案说明

本方案采用如下结构：

```text
浏览器
   |
   | HTTP 8493
   v
Linux VM
   |
   | Docker 端口映射 8493 -> 80
   v
Nginx 容器
   |
   | 提供 MkDocs 生成后的静态页面
   v
MkDocs 构建产物

宿主机 Cron
   |
   | 定时执行
   v
git pull + docker build + docker rm/run
```

说明如下：

- 容器内部不运行 mkdocs serve，而是先构建静态页面，再由 Nginx 提供服务。
- 宿主机负责定时拉取 GitHub 更新，并重新构建和启动容器。
- 访问地址固定为宿主机 IP 的 8493 端口。

## 2. 本目录中的文件说明

- [DEPLOY.md](DEPLOY.md)：本部署文档。
- [Dockerfile](Dockerfile)：用于构建 MkDocs 站点镜像。
- [deploy.sh](deploy.sh)：首次部署脚本。
- [update.sh](update.sh)：手动更新或定时更新脚本。
- [install_cron.sh](install_cron.sh)：安装定时任务脚本。
- [deploy.env.example](deploy.env.example)：可选配置样例文件。

## 3. 前置条件

在 Linux 虚拟机上需要满足以下条件：

1. 已安装 Docker。
2. 已安装 Git。
3. 当前账号可以执行 Docker 命令。
4. 云服务器安全组或防火墙已放行 8493 端口。
5. 可以从虚拟机访问 GitHub。

如果当前用户不能直接执行 Docker，请把命令前加 sudo，或把当前用户加入 docker 用户组。

## 4. 第一步：在虚拟机上克隆项目

先登录虚拟机，然后选择一个部署目录，例如：

```bash
mkdir -p /opt
cd /opt
git clone <你的GitHub仓库地址> mkdocs_tao
cd /opt/mkdocs_tao
```

如果你的 GitHub 仓库是私有仓库，建议使用 SSH Key 或者 Personal Access Token 方式完成克隆。

## 5. 第二步：准备配置文件

先复制一份配置样例：

```bash
cd /opt/mkdocs_tao
cp docker_deploy/deploy.env.example docker_deploy/deploy.env
```

然后根据实际情况修改：

```bash
vi docker_deploy/deploy.env
```

常见需要修改的项有：

- DEPLOY_BRANCH：部署分支，例如 main 或 master。
- HOST_PORT：宿主机端口，当前默认是 8493。
- IMAGE_NAME：Docker 镜像名。
- CONTAINER_NAME：Docker 容器名。
- CRON_EXPR：定时拉取频率。

如果你不修改，默认值也可以直接使用。

## 6. 第三步：给脚本加执行权限

```bash
cd /opt/mkdocs_tao
chmod +x docker_deploy/*.sh
```

## 7. 第四步：执行首次部署

```bash
cd /opt/mkdocs_tao
./docker_deploy/deploy.sh
```

该脚本会完成以下动作：

1. 检查 Docker 和 Git 是否存在。
2. 读取配置文件。
3. 从 GitHub 拉取目标分支最新代码。
4. 使用 [Dockerfile](Dockerfile) 构建镜像。
5. 删除旧容器并重新启动新容器。
6. 将宿主机 8493 端口映射到容器内部 80 端口。

部署成功后，可通过以下地址访问：

- http://VM_IP:8493

## 8. 第五步：验证部署结果

### 检查容器状态

```bash
docker ps
```

你应该能看到配置文件中指定名称的容器正在运行。

### 在虚拟机本机测试

```bash
curl http://127.0.0.1:8493
```

如果返回 HTML 内容，说明容器服务正常。

### 在浏览器测试

在本地浏览器中访问：

- http://VM_IP:8493

如果无法访问，请检查：

1. Docker 容器是否运行。
2. 云厂商安全组是否放行 8493。
3. 虚拟机防火墙是否放行 8493。

## 9. 第六步：安装定时更新

### 9.1 确保宿主机有 Cron 服务

Ubuntu 或 Debian：

```bash
sudo apt update
sudo apt install -y cron
sudo systemctl enable --now cron
```

CentOS 或 RHEL：

```bash
sudo yum install -y cronie
sudo systemctl enable --now crond
```

### 9.2 安装定时任务

```bash
cd /opt/mkdocs_tao
./docker_deploy/install_cron.sh
```

默认情况下，定时任务每 10 分钟执行一次 [update.sh](update.sh)。

如果你希望修改更新频率，请编辑 [deploy.env.example](deploy.env.example) 对应字段并同步到 deploy.env 中的 CRON_EXPR。

例如：

- 每 10 分钟一次：*/10 * * * *
- 每 30 分钟一次：*/30 * * * *
- 每小时一次：0 * * * *

## 10. 第七步：手动更新

即使安装了定时任务，你也可以随时手动触发更新：

```bash
cd /opt/mkdocs_tao
./docker_deploy/update.sh
```

该脚本会：

1. 拉取 GitHub 最新代码。
2. 重新构建镜像。
3. 重建运行中的容器。

## 11. 常见运维命令

### 查看容器日志

```bash
docker logs -f mkdocs-tao
```

如果你修改了容器名，请把 mkdocs-tao 换成实际配置值。

### 查看当前定时任务

```bash
crontab -l
```

### 查看更新日志

```bash
tail -f docker_deploy/update.log
```

### 手动停止容器

```bash
docker stop mkdocs-tao
```

### 手动启动容器

```bash
docker start mkdocs-tao
```

## 12. 常见问题排查

### 问题一：8493 端口无法访问

排查顺序：

1. 执行 docker ps，确认容器已启动。
2. 执行 curl http://127.0.0.1:8493，确认本机可访问。
3. 检查安全组是否放行 TCP 8493。
4. 检查虚拟机防火墙是否拦截 8493。

### 问题二：update.sh 执行失败，提示本地有未提交改动

说明部署目录中存在本地修改。建议做法：

- 如果这些改动不需要保留，重新克隆一份仓库用于部署。
- 如果需要保留，请先提交或备份后再继续。

该脚本默认不会强制覆盖本地改动，以避免误删文件。

### 问题三：Cron 没有执行

请检查：

1. Cron 服务是否已启动。
2. crontab -l 中是否已经安装对应任务。
3. update.log 中是否有报错信息。

### 问题四：构建失败，提示 MkDocs 依赖缺失

当前 [Dockerfile](Dockerfile) 默认只安装 MkDocs 本体。如果后续你在项目里启用了额外主题、插件或 Markdown 扩展，需要同步修改 [Dockerfile](Dockerfile) 中的 pip install 部分，把对应依赖一并装入镜像。

## 13. 推荐的实际执行顺序

为了直接上线，建议你在虚拟机上按如下顺序执行：

```bash
mkdir -p /opt
cd /opt
git clone <你的GitHub仓库地址> mkdocs_tao
cd /opt/mkdocs_tao
cp docker_deploy/deploy.env.example docker_deploy/deploy.env
chmod +x docker_deploy/*.sh
./docker_deploy/deploy.sh
./docker_deploy/install_cron.sh
```

执行完成后：

- 访问地址为 http://VM_IP:8493
- 更新方式为 GitHub 拉取 + 容器重建
- 定时更新由宿主机 Cron 负责

## 14. 一句话总结

这套部署方式的核心思想是：宿主机负责拉取 GitHub 最新代码和重建容器，容器只负责对外提供 MkDocs 构建后的静态网页，因此结构简单、维护成本低、适合个人项目或轻量文档站点的长期运行。