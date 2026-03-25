# Azure Speech 设置指南

## 1. 注册 Azure 账号
- 访问 https://azure.microsoft.com/free/
- 用 Microsoft 账号登录
- 免费版包含每月 **5000 字符免费额度**

## 2. 创建 Speech 资源
1. 登录 Azure Portal (https://portal.azure.com)
2. 点击 "Create a resource"
3. 搜索 "Speech" 并选择 "Speech" 服务
4. 填写信息：
   - **Resource group**: 新建或选择现有（如 `news-tts`）
   - **Region**: 选择 East US 或 West US
   - **Name**: `dailynews-tts`
   - **Pricing tier**: 选择 **Free F0**（免费）
5. 点击 "Review + create" → "Create"

## 3. 获取 API Key 和 Region
1. 等待资源创建完成
2. 进入 Speech 资源页面
3. 左侧菜单点击 "Keys and Endpoint"
4. 复制 **KEY 1** 和 **Region**（如 `eastus`）

## 4. 配置到项目
把 Key 和 Region 添加到代码中的 `AZURE_CONFIG` 对象里。

## 免费额度
- 每月 **5000 字符免费**
- 超出后约 $1/100万字符
- 你的新闻简报每天大约 2000-3000 字符，够用！
