# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

个人知识库系统，用于管理和复习计算机技术知识。
- AI端读取知识库辅助项目开发
- 人类端通过网页浏览和复习知识库

## 常用命令

```bash
# 启动 Flask 网页服务
python web/app.py
# 浏览器打开 http://localhost:5000

# 同步 Markdown 到 SQLite 数据库
python sync/sync_to_sqlite.py
```

## 技术架构

```
知识库（E:/知识库/）
├── markdown/              # Markdown 源文件（一级分类/二级分类/*.md）
│   └── 前端开发/前端框架/   # 含 Vue/ 子目录（sub_category 仍为 "前端框架"）
├── sqlite/                # SQLite 数据库
│   └── knowledge.db
└── sync/                  # （已废弃，同步脚本在网站项目中）

网站（E:/java/Intelligent_Learning/）
├── web/                   # Flask 网页端
│   ├── app.py             # 主程序（8 个 API 端点）
│   └── templates/         # Jinja2 模板
│       └── index.html     # 单页应用，含自定义 Markdown 解析器
└── sync/                  # Markdown → SQLite 同步脚本
    └── sync_to_sqlite.py
```

### 数据流
```
Markdown 文件 ──sync_to_sqlite.py──→ SQLite ──Flask API──→ 前端 SPA
     ↑                                    ↑
  手写编辑                           sort_order 控制展示顺序
```

## 知识库分类

当前共 146 个知识点，覆盖 7 个子分类。

| 一级分类 | 二级分类（数量） |状态 |
|----------|----------|------|
| 后端开发 | Java基础(35)、Python基础(32)、数据库(22) | ✅ 已填充 |
| 前端开发 | Web基础(4)、CSS(14)、JavaScript(30)、前端框架(9) | ✅ 已填充 |
| 系统/嵌入式 | C语言、C++、数据结构、嵌入式、RTOS | ❌ 未填充 |
| AI/机器学习 | Python数据处理、机器学习、深度学习、大模型 | ❌ 未填充 |
| 工具/工程 | Git、Docker、Linux、通信协议 | ❌ 未填充 |

## 同步机制

- Markdown 文件是唯一数据源，路径模式：`{一级分类}/{二级分类}/*.md`
- 同步键为 `(title, category, sub_category)` 三元组
- category 和 sub_category 从文件路径提取（`parts[0]` 和 `parts[1]`），**不从 frontmatter 读取**
- 内容字段（content, code_example, tags, status, difficulty, level, source, priority, sort_order 等）每次同步以 Markdown 为准覆写
- 复习字段（mastery, review_count, last_reviewed_at, next_review_date）UPDATE 时保留原值，INSERT 时取 frontmatter 的 mastery（默认 0）
- Markdown 中删除的文件会在同步时从数据库删除（orphan cleanup）
- 代码块提取后正文中用 `:::code-block:::` 占位符标记位置，前端渲染时跳过该占位符

## Markdown Frontmatter 格式

```yaml
---
title: 知识点标题
category: 一级分类
sub_category: 二级分类
tags: ["标签1", "标签2"]
status: 已学/待学/废弃
level: 入门/进阶/高级
source: 来源
priority: 高/中/低
mastery: 0-5
difficulty: 1-5
sort_order: 10
personal_notes: 个人备注
---
```

### sort_order 规则
- 每个子分类内独立编号，步长 10（10, 20, 30...），方便后续插入
- 所有 `/api/points` 和 `/api/search` 查询按 `sort_order ASC` 排序
- 新增知识点必须添加 `sort_order`，否则默认为 0（排在最前面）
- 全部 146 个知识点已完成 sort_order 编排

## 数据库

- 路径：`E:/知识库/sqlite/knowledge.db`
- 主表：knowledge_points（17 列，含 `sort_order`）
- 索引：category、sub_category、status+mastery、tags

## API 端点

所有列表类接口均按 `sort_order ASC` 排序。

| 端点 | 说明 |
|------|------|
| `GET /api/categories` | 获取一级分类列表 |
| `GET /api/subcategories?category=X` | 获取指定一级分类的子分类 |
| `GET /api/points?category=X&sub_category=Y` | 获取知识点列表（按 sort_order 排序） |
| `GET /api/search?q=keyword` | 搜索知识点（按 sort_order 排序） |
| `GET /api/flashcard` | 获取随机闪卡（RANDOM） |
| `POST /api/flashcard/answer` | 闪卡答题（答对 mastery+1，答错-1） |
| `GET /api/test` | 获取随机测验题（含 3 个干扰选项，RANDOM） |
| `POST /api/test/answer` | 提交答案（答对 mastery+1） |

## AI端工作流程

1. 开始新项目时，读取知识库了解用户已掌握的技术
2. 设计方案时，优先使用用户已掌握的知识
3. 发现知识缺口，记录清单，不打断思路
4. 代码完成后展示知识缺口清单
5. 用户确认后，存入知识库 → 自动触发同步脚本