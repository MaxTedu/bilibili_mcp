# 🎮 Bilibili MCP Server

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" width="50" alt="Python">
  <img src="https://img.shields.io/badge/MCP-Server-FF69B4?style=for-the-badge" alt="MCP Server">
  <img src="https://img.shields.io/badge/Bilibili-API-00A1D6?style=for-the-badge" alt="Bilibili API">
</p>

<p align="center">
  <img src="https://count.getloli.com/get/@bilibili-mcp?theme=gelbooru" alt="Hits">
  <img src="https://img.shields.io/github/stars/yourusername/bilibili-mcp?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/forks/yourusername/bilibili-mcp?style=for-the-badge" alt="Forks">
</p>

---

## ✨ 简介 Introduction

> 🌸 让你的 AI 助手成为你在 B 站的最佳搭档！🚀
>
> 这是一个基于 **Model Context Protocol (MCP)** 的 B 站工具服务器，让你的 AI 可以通过自然语言帮你发弹幕、评论、点赞、投币、收藏，还能一键三连！💖

```
    ╔═══════════════════════════════════════════════════════════╗
    ║     ♡  ♡  ♡  Bilibili MCP Server  ♡  ♡  ♡              ║
    ║                                                           ║
    ║   ┌─────────────────────────────────────────────────┐     ║
    ║   │  🎯 发送弹幕  |  💬 评论互动  |  ❤️ 点赞投币     │     ║
    ║   │  ⭐ 一键三连  |  🔍 视频搜索  |  📺 批量操作     │     ║
    ║   └─────────────────────────────────────────────────┘     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
```

---

## 🎯 功能特性 Features

| 功能 | 状态 | 说明 |
|------|:----:|------|
| 🎮 发送弹幕 | ✅ | 支持自定义时间、颜色、模式、字体大小 |
| 💬 发送评论 | ✅ | 支持指定分P视频评论 |
| 📊 获取视频信息 | ✅ | 获取标题、播放量、点赞、投币、收藏等 |
| ❤️ 点赞/取消点赞 | ✅ | 精准控制点赞状态 |
| 💰 投币 | ✅ | 支持1-2个币，可同时点赞 |
| ⭐ 收藏/取消收藏 | ✅ | 管理视频收藏 |
| 🤖 一键三连 | ✅ | 点赞+投币+收藏，一气呵成！ |
| 📜 获取弹幕列表 | ✅ | 查看视频弹幕 |
| 💭 获取评论列表 | ✅ | 查看视频评论 |
| 🔍 搜索视频 | ✅ | 关键词搜索 |
| 👤 获取用户投稿 | ✅ | 查看UP主投稿列表 |
| 📝 批量评论 | ✅ | 批量评论指定UP主的视频 |

---

## 🚀 快速开始 Quick Start

### 1️⃣ 安装依赖 Installation

```bash
# 克隆项目
git clone https://github.com/yourusername/bilibili-mcp.git
cd bilibili-mcp

# 安装依赖
pip install -r requirements.txt
```

> ⚠️ **小提示**: 推荐使用虚拟环境！
> ```bash
> python -m venv .venv
> .venv\Scripts\activate  # Windows
> source .venv/bin/activate  # Linux/Mac
> pip install -r requirements.txt
> ```

### 2️⃣ 配置账号凭证 Configuration

#### 📋 获取你的凭证

1. 在浏览器中登录 [Bilibili](https://www.bilibili.com) 🎫
2. 按 `F12` 打开开发者工具
3. 切换到 **「Application」** → **「Cookies」** → **`https://www.bilibili.com`**
4. 复制以下三个值：
   - `SESSDATA`
   - `bili_jct`
   - `buvid3`

#### 📝 创建配置文件

```bash
# Windows
copy configexample.json config.json

# Linux/Mac
cp configexample.json config.json
```

编辑 `config.json`：

```json
{
  "sessdata": "这里粘贴你的SESSDATA",
  "bili_jct": "这里粘贴你的bili_jct",
  "buvid3": "这里粘贴你的buvid3"
}
```

> 🔒 **安全提醒**: 请妥善保管你的凭证！切勿泄露给他人！

### 3️⃣ 配置到 Claude Code

在 Claude Code 的 MCP 配置文件中添加服务器配置：

**Windows:** `%APPDATA%\Claude\code_desktop_config.json`

**Mac/Linux:** `~/.config/Claude/code_desktop_config.json`

```json
{
  "mcpServers": {
    "bilibili": {
      "type": "stdio",
      "command": "python",
      "args": ["D:\\path\\to\\bilibili-mcp\\server.py"]
    }
  }
}
```

> 💡 **提示**: 请将 `args` 中的路径替换为你实际的 `server.py` 绝对路径！

### 4️⃣ 重启 Claude Code

重启应用后，你就可以开始与你的 AI 助手互动啦！🎉

---

## 🎮 使用示例 Usage Examples

### 📺 获取视频信息

```
🤖 用户: 帮我看看这个视频的信息：BV1xx411q7Mv

📊 Bilibili MCP:
   视频标题: xxx
   UP主: xxx
   播放量: xxx
   点赞: xxx
   投币: xxx
   收藏: xxx
   弹幕: xxx
   评论: xxx
```

### 🎮 发送弹幕

```
🤖 用户: 给 BV1xx411q7Mv 在第10秒发个弹幕说"太精彩了！"

🎉 Bilibili MCP:
   弹幕发送成功！
   视频: BV1xx411q7Mv
   内容: 太精彩了！
   时间: 10秒
```

### 💬 发送评论

```
🤖 用户: 给 BV1xx411q7Mv 发个评论："这个视频做得真好，学到了很多！"

🎉 Bilibili MCP:
   评论发送成功！
   视频: BV1xx411q7Mv
   内容: 这个视频做得真好，学到了很多！
```

### 🤖 一键三连

```
🤖 用户: 给 BV1xx411q7Mv 来个一键三连

🎊 Bilibili MCP:
   一键三连成功！
   视频: BV1xx411q7Mv
   
   ✅ 点赞成功
   ✅ 投币1个成功
   ✅ 收藏成功
```

---

## ⚠️ 注意事项 Important Notes

```
┌─────────────────────────────────────────────────────────┐
│  🎌 社区准则 Community Guidelines                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ⚠️ 请遵守B站社区规范，不要恶意刷屏                      │
│  ⏰ 弹幕发送间隔建议至少5秒                              │
│  🚫 不要用于商业用途或骚扰他人                          │
│  🔑 Cookie有效期有限，可能需要定期更新                   │
│  📚 仅供个人学习使用                                    │
│                                                         │
│  💖 文明弹幕，和谐社区！                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 项目结构 Project Structure

```
bilibili-mcp/
│
├── 🎯 server.py              # MCP服务器主文件
├── 📋 configexample.json     # 配置文件模板（示例）
├── ⚙️ config.json            # 你的配置文件（需自行创建）
├── 📦 requirements.txt       # Python依赖列表
├── 📖 README.md              # 说明文档
└── 🙈 .gitignore             # Git忽略文件
```

---

## 🛠️ 技术栈 Tech Stack

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Python%20SDK-FF69B4?style=for-the-badge)
![Bilibili API](https://img.shields.io/badge/Bilibili-API-00A1D6?style=for-the-badge&logo=bilibili&logoColor=white)

</p>

- **[MCP Python SDK](https://pypi.org/project/mcp/)** - Model Context Protocol 核心框架
- **[bilibili-api-python](https://github.com/Nemo2011/bilibili-api)** - B站API封装库
- **[aiohttp](https://docs.aiohttp.org/)** - 异步HTTP请求库

---

## 🤝 贡献指南 Contributing

欢迎提交 Issue 和 Pull Request！💖

1. 🍴 Fork 本项目
2. 🔨 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 💾 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 📤 推送到分支 (`git push origin feature/AmazingFeature`)
5. 🎉 开启一个 Pull Request

---

## 📜 开源许可证 License

本项目采用 [MIT License](LICENSE) 开源。

---

## 🙏 致谢 Acknowledgments

- 感谢 [bilibili-api-python](https://github.com/Nemo2011/bilibili-api) 项目的优秀封装
- 感谢 [MCP](https://modelcontextprotocol.io/) 提供的协议框架
- 感谢所有 Contributors 的贡献！🌟

---

<p align="center">

```
    ╔══════════════════════════════════════════╗
    ║                                          ║
    ║     🎭 感谢使用 Bilibili MCP Server 🎭   ║
    ║                                          ║
    ║     🌟 Star ⭐ | 🍴 Fork 🍴 | 📖 Docs    ║
    ║                                          ║
    ║     Made with ❤️  by 二次元爱好者         ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
```

</p>

<p align="center">

[![Bilibili](https://img.shields.io/badge/Bilibili-Channel-00A1D6?style=for-the-badge&logo=bilibili)](https://space.bilibili.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github)](https://github.com/yourusername)

</p>

---

> 🎌 *"每一个弹幕都是一份快乐，每一条评论都是一份支持"* 🎌
>
> **如果这个项目对你有帮助，请给我们一个 ⭐ 吧！**
