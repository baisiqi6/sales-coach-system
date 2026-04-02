# 智能销售对练系统

基于钉钉生态的企业级销售对练 AI 系统

## 项目结构

```
sales-coach-system/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # 路由层
│   │   ├── core/        # 配置
│   │   ├── services/    # 业务逻辑层
│   │   ├── models/      # 数据库模型
│   │   └── schemas/     # Pydantic 模型
│   ├── venv/            # Python 虚拟环境（依赖隔离）
│   ├── main.py          # FastAPI 入口
│   └── requirements.txt # 依赖包
│
├── frontend-miniapp/     # uni-app 销售端
│   ├── src/
│   │   ├── pages/       # 页面
│   │   ├── api/         # API 封装
│   │   └── store/       # 状态管理
│   ├── manifest.json    # uni-app 配置
│   └── pages.json       # 页面路由配置
│
└── frontend-admin/       # Vue3 主管后台（待实现）
```

## 快速开始

### 后端启动（使用虚拟环境）

```bash
cd backend

# 首次运行：创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env  # 根据实际情况修改配置

# 启动服务
python main.py
```

访问 http://localhost:8000 查看接口文档

**退出虚拟环境**：`deactivate`

### 前端启动（H5 开发调试）

```bash
cd frontend-miniapp
# 需要先安装 HBuilderX 或使用 uni-app CLI
```

### 打包钉钉小程序

使用 HBuilderX：
1. 打开项目
2. 运行 → 运行到小程序模拟器 → 钉钉小程序
3. 发行 → 小程序-钉钉

## 当前进度

- [x] 后端基础框架搭建
- [x] 前端基础框架搭建
- [x] 健康检查接口
- [x] 页面路由配置
- [ ] 数据库集成
- [ ] 钉钉 SDK 集成
- [ ] LLM 服务集成
- [ ] ASR/TTS 集成
- [ ] 对练核心功能

## 测试

### 后端测试
```bash
curl http://localhost:8000/api/v1/health
```

### 前端测试
打开小程序，点击"测试后端联通"按钮
