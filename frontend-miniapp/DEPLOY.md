# 钉钉小程序打包指南

## 方法一：使用 HBuilderX（推荐）

### 1. 下载安装 HBuilderX
- 访问 https://www.dextudio.cn/
- 下载标准版 App 开发版
- 安装后打开

### 2. 导入项目
1. 文件 → 导入 → 从本地目录导入
2. 选择 `/Users/yinxin/Desktop/sales-coach-system/frontend-miniapp` 目录
3. 项目类型选择 "uni-app"

### 3. 配置钉钉小程序
1. 打开 `manifest.json`
2. 在 "App模块配置" 中勾选 "钉钉"
3. 填入你的钉钉小程序 `appid`

### 4. 运行调试
1. 运行 → 运行到小程序模拟器 → 钉钉小程序
2. 下载钉钉开发者工具
3. 即可在模拟器中预览

### 5. 打包发布
1. 发行 → 小程序-钉钉
2. 会生成 `dist/build/mp-dingtalk` 目录
3. 用钉钉开发者工具打开该目录
4. 上传到钉钉后台

---

## 方法二：使用 Vue CLI（需要额外配置）

```bash
# 全局安装 vue-cli
npm install -g @vue/cli

# 创建 uni-app 项目（会提示选择模板）
vue create -p dcloudio/uni-preset-vue my-project

# 将现有文件复制到新项目
```

---

## 当前项目状态

✅ 后端框架已搭建完成
✅ 前端页面已创建
✅ 基础路由已配置
⏳ 需要使用 HBuilderX 完成打包

## 测试建议

1. 先在 H5 环境测试页面和 API 联通
2. 确认无误后再打包钉钉小程序
3. 使用钉钉开发者工具的真机调试功能
