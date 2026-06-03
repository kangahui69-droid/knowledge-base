---
title: HTML基础
category: 前端开发
sub_category: Web基础
tags: ["HTML", "前端", "标签", "Web基础"]
status: 已学
level: 入门
source: 课堂笔记
priority: 中
mastery: 3
difficulty: 1
created_at: 2026-06-03
updated_at: 2026-06-03
---

# HTML基础

## 内容摘要

HTML（HyperText Markup Language，超文本标记语言）是用于创建网页的标准标记语言。HTML 使用标签来描述网页的结构和内容，浏览器读取 HTML 文档并将其渲染成网页。

### 概念

- HTML 是一种**标记语言**，不是编程语言
- HTML 文档由一系列**标签**组成
- 浏览器解析 HTML 后呈现网页

### 结构标签

```html
<!DOCTYPE html>
<html>
    <head>
        <title>页面标题</title>
    </head>
    <body>
        <!-- 页面内容写在这里 -->
    </body>
</html>
```

| 标签 | 说明 |
|------|------|
| `<!DOCTYPE html>` | 声明 HTML5 文档类型 |
| `<html>` | 根标签 |
| `<head>` | 头部，存放元信息（标题、引入CSS/JS等） |
| `<title>` | 网页标题（显示在浏览器标签栏） |
| `<body>` | 主体，存放网页可见内容 |

### 标题标签

`<h1>` 到 `<h6>`，从大到小，h1 最大、h6 最小。

```html
<h1>一级标题</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<h4>四级标题</h4>
<h5>五级标题</h5>
<h6>六级标题</h6>
```

### 段落标签

`<p>` 标签定义段落。

```html
<p>这是一个段落</p>
<p>这是另一个段落</p>
```

### 水平线标签

`<hr>` 创建水平线（横线）。

```html
<p>段落1</p>
<hr>
<p>段落2</p>
```

### 文本加粗标签

`<b>` 或 `<strong>` 都用于加粗文本，`<strong>` 语义更强（表示重要内容）。

```html
<p>普通文本 <b>加粗文本</b></p>
<p>普通文本 <strong>加粗且重要</strong></p>
```

### 图片标签

`<img>` 用于在网页中嵌入图片。

```html
<img src="图片路径.jpg" alt="图片描述" width="200" height="100">
```

| 属性 | 说明 |
|------|------|
| `src` | 图片路径（必填） |
| `alt` | 图片无法显示时的替代文字 |
| `width` | 宽度 |
| `height` | 高度 |

### 音频标签

`<audio>` 用于在网页中播放音频。

```html
<audio src="music.mp3" controls></audio>
```

| 属性 | 说明 |
|------|------|
| `src` | 音频路径 |
| `controls` | 显示播放控件 |
| `autoplay` | 自动播放 |
| `loop` | 循环播放 |

### 视频标签

`<video>` 用于播放视频，用法与 audio 类似。

```html
<video src="movie.mp4" controls width="500"></video>
```

### 布局标签

HTML5 引入的语义化布局标签：

```html
<body>
    <header>头部（页眉）</header>
    <nav>导航栏</nav>
    <main>
        <article>文章内容</article>
        <section>区块</section>
        <aside>侧边栏</aside>
    </main>
    <footer>底部（页脚）</footer>
</body>
```

| 标签 | 说明 |
|------|------|
| `<header>` | 头部 |
| `<nav>` | 导航 |
| `<main>` | 主体内容 |
| `<article>` | 文章 |
| `<section>` | 章节/区块 |
| `<aside>` | 侧边栏 |
| `<footer>` | 底部 |

### 表格标签

```html
<table border="1">
    <thead>
        <tr>
            <th>姓名</th>
            <th>年龄</th>
            <th>城市</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>张三</td>
            <td>25</td>
            <td>北京</td>
        </tr>
        <tr>
            <td>李四</td>
            <td>30</td>
            <td>上海</td>
        </tr>
    </tbody>
</table>
```

| 标签 | 说明 |
|------|------|
| `<table>` | 表格 |
| `<thead>` | 表头 |
| `<tbody>` | 表体 |
| `<tr>` | 表格行 |
| `<th>` | 表头单元格 |
| `<td>` | 数据单元格 |

**常用属性**：
- `border`：边框宽度
- `cellpadding`：单元格内边距
- `cellspacing`：单元格间距
- `colspan`：跨列合并
- `rowspan`：跨行合并

### 表单标签

```html
<form action="/login" method="post">
    <!-- 文本框 -->
    <label for="username">用户名：</label>
    <input type="text" id="username" name="username">
    <br>

    <!-- 密码框 -->
    <label for="password">密码：</label>
    <input type="password" id="password" name="password">
    <br>

    <!-- 单选框 -->
    <input type="radio" id="male" name="gender" value="male">
    <label for="male">男</label>
    <input type="radio" id="female" name="gender" value="female">
    <label for="female">女</label>
    <br>

    <!-- 复选框 -->
    <input type="checkbox" id="hobby1" name="hobby" value="code">
    <label for="hobby1">编程</label>
    <input type="checkbox" id="hobby2" name="hobby" value="read">
    <label for="hobby2">阅读</label>
    <br>

    <!-- 下拉框 -->
    <select name="city">
        <option value="beijing">北京</option>
        <option value="shanghai">上海</option>
    </select>
    <br>

    <!-- 提交按钮 -->
    <button type="submit">提交</button>
    <button type="reset">重置</button>
</form>
```

| 标签 | 说明 |
|------|------|
| `<form>` | 表单 |
| `<input>` | 输入框（type 决定类型） |
| `<label>` | 表单标签 |
| `<select>` / `<option>` | 下拉选择框 |
| `<button>` | 按钮 |
| `<textarea>` | 多行文本框 |

**input 常用 type**：
- `text`：文本框
- `password`：密码框
- `radio`：单选框
- `checkbox`：复选框
- `submit`：提交按钮
- `reset`：重置按钮
- `file`：文件上传

## 个人备注

- 表单提交时，`name` 属性是必须的，否则数据不会被提交
- 单选框用相同的 `name` 互斥
- 布局标签是 HTML5 新增的，比 `<div>` 语义更强
- 表格不推荐用于页面布局（用 CSS 布局）
- 图片必须设置 `alt` 属性，有利于 SEO 和无障碍
