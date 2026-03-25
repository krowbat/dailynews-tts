# Daily News TTS

基于你现有 GitHub Pages 新闻简报的语音播报前端。

## 功能

- 📰 自动加载每日新闻（从你的 krowbat.github.io/newsbriefs）
- 🔊 **语音播报**：浏览器内置 TTS，支持中文
- 🎯 **三种播报模式**：
  - 播报全部新闻
  - 播报单个分类
  - 播报单条新闻
- 📱 响应式设计，手机电脑都能用

## 工作原理

1. 访问页面时自动获取当天的新闻 HTML
2. 解析新闻内容并展示
3. 点击 🔊 按钮使用 Web Speech API 播报

## 部署到 Vercel

### 方法一：GitHub 导入（推荐）

1. 在 GitHub 创建新仓库（如 `daily-news-tts`）
2. 将代码推送到仓库
3. 登录 Vercel (vercel.com)
4. 点击 "Add New Project"
5. 选择 GitHub 仓库导入
6. 直接部署，无需额外配置

### 方法二：Vercel CLI

```bash
npm install -g vercel
vercel login
vercel --prod
```

## 本地测试

```bash
npx serve .
```

然后访问 http://localhost:3000

## 注意

- 语音播报需要浏览器支持（Chrome/Safari/Firefox 都支持）
- 默认中文语音，如果系统没有中文语音包会fallback到英文
