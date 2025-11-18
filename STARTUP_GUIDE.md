# 🚀 TradingAgents 启动指南

> 适合新手的完整启动文档，教你如何启动整个项目的所有服务

---

## 📋 目录

1. [准备工作](#准备工作)
2. [启动数据库服务](#启动数据库服务)
3. [启动后端服务](#启动后端服务)
4. [启动前端服务](#启动前端服务)
5. [验证服务](#验证服务)
6. [常见问题](#常见问题)
7. [停止服务](#停止服务)

---

## 📝 准备工作

### 1. 确认环境

确保你已经安装：
- ✅ Python 3.10+
- ✅ Node.js 16+
- ✅ Docker Desktop（用于运行 MongoDB 和 Redis）

### 2. 检查 Docker 是否运行

```bash
# 检查 Docker 状态
docker --version

# 如果没启动，打开 Docker Desktop 应用
```

---

## 🗄️ 启动数据库服务

### 第1步：启动 MongoDB 和 Redis

```bash
# 进入项目目录
cd /Users/adam/Documents/TradingAgents-CN

# 使用 Docker Compose 启动数据库服务
docker-compose up -d mongodb redis
```

**说明：**
- `docker-compose up`：启动服务
- `-d`：后台运行（detached mode）
- `mongodb redis`：只启动这两个服务

### 第2步：验证数据库启动

```bash
# 查看运行的容器
docker ps

# 应该看到类似输出：
# CONTAINER ID   IMAGE         PORTS                      NAMES
# xxx            mongo:7.0     0.0.0.0:27017->27017/tcp   tradingagents-mongodb
# xxx            redis:7.2     0.0.0.0:6379->6379/tcp     tradingagents-redis
```

### 第3步：查看数据库日志（可选）

```bash
# 查看 MongoDB 日志
docker logs tradingagents-mongodb

# 查看 Redis 日志
docker logs tradingagents-redis
```

---

## ⚙️ 启动后端服务

### 第1步：打开新终端窗口

保持数据库运行，打开一个**新的终端窗口**

### 第2步：进入项目目录

```bash
cd /Users/adam/Documents/TradingAgents-CN
```

### 第3步：激活虚拟环境

```bash
# 激活虚拟环境
source venv/bin/activate

# 成功后，终端提示符会变成：
# (venv) adam@Adams-Mac TradingAgents-CN %
```

### 第4步：启动后端

```bash
# 方式1：使用 main.py（推荐）
python main.py

# 方式2：使用模块方式
python -m app

# 方式3：直接使用 uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**看到以下输出表示成功：**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**后端地址：** http://localhost:8000

---

## 🎨 启动前端服务

### 第1步：再打开一个新终端窗口

保持后端运行，打开**另一个新的终端窗口**

### 第2步：进入前端目录

```bash
cd /Users/adam/Documents/TradingAgents-CN/frontend
```

### 第3步：安装依赖（首次运行需要）

```bash
# 如果是第一次运行，需要先安装依赖
npm install

# 或使用 yarn
yarn install
```

### 第4步：启动前端开发服务器

```bash
# 使用 npm
npm run dev

# 或使用 yarn
yarn dev
```

**看到以下输出表示成功：**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**前端地址：** http://localhost:5173

---

## ✅ 验证服务

### 1. 检查所有服务状态

**打开浏览器，依次访问：**

| 服务 | 地址 | 状态检查 |
|------|------|---------|
| 前端 | http://localhost:5173 | 看到登录页面 ✅ |
| 后端 API | http://localhost:8000/docs | 看到 API 文档 ✅ |
| 后端健康检查 | http://localhost:8000/health | 看到 `{"status":"ok"}` ✅ |
| MongoDB | localhost:27017 | Docker 容器运行中 ✅ |
| Redis | localhost:6379 | Docker 容器运行中 ✅ |

### 2. 完整的服务架构

```
┌─────────────────────────────────────────────────┐
│                   浏览器                         │
│            http://localhost:5173                │
└────────────────────┬────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────┐
│              前端 (Vue.js)                       │
│         端口: 5173 (开发模式)                     │
└────────────────────┬────────────────────────────┘
                     │ API 请求
                     ↓
┌─────────────────────────────────────────────────┐
│            后端 (FastAPI)                        │
│              端口: 8000                          │
└────────┬───────────────────────┬─────────────────┘
         │                       │
         ↓                       ↓
┌────────────────┐      ┌────────────────┐
│   MongoDB      │      │     Redis      │
│   端口: 27017  │      │   端口: 6379   │
│  (Docker容器)  │      │  (Docker容器)  │
└────────────────┘      └────────────────┘
```

---

## ❓ 常见问题

### 问题1：后端启动失败，提示 `ModuleNotFoundError`

**原因：** 虚拟环境未激活或依赖未安装

**解决：**
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 安装依赖
pip install -e .

# 3. 重新启动
python main.py
```

---

### 问题2：前端启动失败，提示 `command not found: npm`

**原因：** Node.js 未安装

**解决：**
```bash
# 使用 Homebrew 安装 Node.js
brew install node

# 验证安装
node --version
npm --version
```

---

### 问题3：MongoDB 连接失败

**原因：** Docker 容器未启动

**解决：**
```bash
# 检查容器状态
docker ps

# 如果没有看到 mongodb 容器，重新启动
docker-compose up -d mongodb redis

# 查看日志排查问题
docker logs tradingagents-mongodb
```

---

### 问题4：端口被占用

**错误信息：** `Address already in use`

**解决：**
```bash
# 查看占用端口的进程
# macOS/Linux:
lsof -i :8000    # 后端端口
lsof -i :5173    # 前端端口
lsof -i :27017   # MongoDB 端口
lsof -i :6379    # Redis 端口

# 杀死进程
kill -9 <PID>

# 或者修改端口（在配置文件中）
```

---

### 问题5：虚拟环境激活失败

**错误信息：** `source: no such file or directory: venv/bin/activate`

**原因：** 虚拟环境不存在

**解决：**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活
source venv/bin/activate

# 安装依赖
pip install -e .
```

---

## 🛑 停止服务

### 停止前端

在前端终端窗口按：`Ctrl + C`

### 停止后端

在后端终端窗口按：`Ctrl + C`

### 停止数据库

```bash
# 停止所有 Docker 容器
docker-compose down

# 只停止但不删除容器
docker-compose stop

# 停止并删除所有数据（谨慎使用！）
docker-compose down -v
```

---

## 📊 完整启动流程总结

### 终端窗口安排（建议开3个终端）

**终端1 - 数据库：**
```bash
cd /Users/adam/Documents/TradingAgents-CN
docker-compose up -d mongodb redis
docker logs -f tradingagents-mongodb  # 查看日志（可选）
```

**终端2 - 后端：**
```bash
cd /Users/adam/Documents/TradingAgents-CN
source venv/bin/activate
python main.py
```

**终端3 - 前端：**
```bash
cd /Users/adam/Documents/TradingAgents-CN/frontend
npm run dev
```

### 启动顺序

1. ✅ **先启动数据库**（MongoDB + Redis）
2. ✅ **再启动后端**（等数据库启动完成）
3. ✅ **最后启动前端**

---

## 🎯 快速启动命令（复制使用）

### 一键启动数据库
```bash
cd /Users/adam/Documents/TradingAgents-CN && docker-compose up -d mongodb redis
```

### 一键启动后端
```bash
cd /Users/adam/Documents/TradingAgents-CN && source venv/bin/activate && python main.py
```

### 一键启动前端
```bash
cd /Users/adam/Documents/TradingAgents-CN/frontend && npm run dev
```

---

## 💡 开发技巧

### 1. 使用 tmux 或 screen 管理多个终端

```bash
# 安装 tmux
brew install tmux

# 创建会话
tmux new -s trading

# 分割窗口
# Ctrl+b 然后按 " (水平分割)
# Ctrl+b 然后按 % (垂直分割)
```

### 2. 保存别名到 .zshrc

编辑 `~/.zshrc`，添加：
```bash
# TradingAgents 快捷命令
alias ta-db='cd /Users/adam/Documents/TradingAgents-CN && docker-compose up -d mongodb redis'
alias ta-backend='cd /Users/adam/Documents/TradingAgents-CN && source venv/bin/activate && python main.py'
alias ta-frontend='cd /Users/adam/Documents/TradingAgents-CN/frontend && npm run dev'
alias ta-stop='cd /Users/adam/Documents/TradingAgents-CN && docker-compose down'
```

然后：
```bash
source ~/.zshrc

# 之后可以直接使用
ta-db         # 启动数据库
ta-backend    # 启动后端
ta-frontend   # 启动前端
ta-stop       # 停止所有服务
```

---

## 📚 相关文档

- [后端 API 文档](http://localhost:8000/docs)
- [项目 README](./README.md)
- [Docker Compose 配置](./docker-compose.yml)

---

## ✨ 启动成功的标志

当所有服务正常运行时：

- ✅ 浏览器访问 http://localhost:5173 能看到登录页面
- ✅ 浏览器访问 http://localhost:8000/docs 能看到 API 文档
- ✅ `docker ps` 能看到 mongodb 和 redis 容器
- ✅ 三个终端窗口都在运行，没有错误信息

**恭喜！🎉 你已经成功启动了整个项目！**

---

有问题随时查看这个文档，或者询问我！

