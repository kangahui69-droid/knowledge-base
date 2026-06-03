# 个人知识库系统

基于 Markdown + Flask 的个人知识库系统，用于管理和复习计算机技术知识。

## 功能

- **浏览模式**：按分类浏览知识点，像看书一样
- **闪卡记忆**：随机弹出知识点，复习记忆
- **测试模式**：四选一提问，检验掌握程度
- **搜索功能**：按标题、标签、分类搜索

## 技术栈

- 后端：Flask (Python)
- 数据库：SQLite
- 同步：Markdown → SQLite 自动同步

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/<username>/knowledge-base.git
cd knowledge-base

# 安装依赖
pip install -r web/requirements.txt

# 初始化数据库
python sync/sync_to_sqlite.py

# 启动服务
python web/app.py
# 浏览器打开 http://localhost:5000
```

## 公网访问

使用 Cloudflare Tunnel 将本地服务暴露到公网：

```bash
# 安装 cloudflared（一次性）
# 下载地址：https://github.com/cloudflare/cloudflared/releases

# 启动隧道
cloudflared tunnel --url http://localhost:5000
# 复制输出的公网URL即可访问
```

## 项目结构

```
knowledge-base/
├── web/              # 网页端代码
├── sync/             # 同步脚本
├── db/               # 数据库相关
├── knowledge/        # 知识库 Markdown
├── docs/             # 文档
└── README.md
```

## 许可证

MIT