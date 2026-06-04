# Claude Code 配置

## 项目概述

个人知识库系统，用于管理和复习计算机技术知识。
- AI端读取知识库辅助项目开发
- 人类端通过网页浏览和复习知识库

## 知识库路径

- 知识库根目录：`E:/知识库/`
- Markdown 文件：`E:/知识库/markdown/`
- SQLite 数据库：`E:/知识库/sqlite/knowledge.db`
- 项目代码目录：`E:/java/Intelligent_Learning/`
- 设计文档：`E:/java/Intelligent_Learning/个人知识库系统设计文档.md`

## 知识库分类

| 一级分类 | 说明 |
|----------|------|
| 后端开发 | Java基础、Spring生态、Python基础、Web框架、数据库 |
| 前端开发 | Web基础、前端框架、构建工具、可视化 |
| 系统/嵌入式 | C语言、C++、数据结构、嵌入式、RTOS |
| AI/机器学习 | Python数据处理、机器学习、深度学习、大模型 |
| 工具/工程 | Git、Docker、Linux、通信协议 |
| 待学习区 | 暂未掌握的技术 |
| 综合/踩坑区 | 踩坑记录、项目经验 |

## AI端工作流程

1. 开始新项目时，读取 `knowledge/` 了解用户已掌握的技术
2. 设计方案时，优先使用用户已掌握的知识
3. 发现知识缺口，记录清单，不打断思路
4. 代码完成后展示知识缺口清单
5. 用户确认后，存入知识库 → 自动触发同步脚本

## 知识点模板格式

```markdown
---
title: 知识点名称
category: 一级分类
sub_category: 二级分类
tags: ["标签1", "标签2"]
status: 已学
level: 入门
source: 来源
priority: 中
mastery: 3
difficulty: 1
created_at: 2024-10-12
updated_at: 2024-10-12
---

# 知识点名称

## 内容摘要
...

## 代码示例
```代码```...

## 个人备注
...
```