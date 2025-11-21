# 快速启动

## 启动步骤

### 1. 启动数据库
```bash
cd /Users/adam/Documents/TradingAgents-CN
docker-compose up -d mongodb redis
```

### 2. 启动后端
```bash
cd /Users/adam/Documents/TradingAgents-CN
source venv/bin/activate
python -m app
```

### 3. 启动前端
```bash
cd /Users/adam/Documents/TradingAgents-CN/frontend
npm run dev
```

## 验证
- 前端: http://localhost:5173
- 后端: http://localhost:8000/docs

## 停止服务
- 前端/后端: `Ctrl + C`
- 数据库: `docker-compose down`

