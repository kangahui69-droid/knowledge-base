"""
同步脚本：将 Markdown 文件同步到 SQLite 数据库
"""
import os
import re
import sqlite3
from datetime import datetime

# 路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, 'knowledge')
DB_PATH = os.path.join(BASE_DIR, 'db', 'knowledge.db')

def init_db():
    """初始化数据库，创建表"""
    os.makedirs(os.path.join(BASE_DIR, 'db'), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            code_example TEXT DEFAULT '',
            tags TEXT DEFAULT '[]',
            status TEXT NOT NULL DEFAULT '待学',
            mastery INTEGER NOT NULL DEFAULT 0,
            difficulty INTEGER DEFAULT 1,
            level TEXT DEFAULT '入门',
            source TEXT DEFAULT '',
            priority TEXT DEFAULT '中',
            related_ids TEXT DEFAULT '[]',
            personal_notes TEXT DEFAULT '',
            review_count INTEGER DEFAULT 0,
            last_reviewed_at DATETIME,
            next_review_date DATETIME,
            created_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON knowledge_points(category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sub_category ON knowledge_points(sub_category)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status_mastery ON knowledge_points(status, mastery)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON knowledge_points(tags)')

    conn.commit()
    conn.close()
    print("数据库初始化完成")

def parse_frontmatter(content):
    """解析 Markdown 文件的 Frontmatter"""
    frontmatter = {}
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]

            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    # 处理数组格式
                    if value.startswith('[') and value.endswith(']'):
                        # 简单处理，存为 JSON 字符串
                        pass

                    frontmatter[key] = value

    return frontmatter, body.strip()

def extract_code_examples(body):
    """从正文中提取代码块"""
    code_blocks = re.findall(r'```[\s\S]*?```', body)
    code_example = '\n'.join(code_blocks)
    # 移除正文中的代码块
    content = re.sub(r'```[\s\S]*?```', '', body)
    return content.strip(), code_example.strip()

def get_all_markdown_files():
    """获取所有 Markdown 文件"""
    files = []
    for root, dirs, filenames in os.walk(KNOWLEDGE_DIR):
        for filename in filenames:
            if filename.endswith('.md'):
                files.append(os.path.join(root, filename))
    return files

def get_category_from_path(file_path):
    """从文件路径提取一级和二级分类"""
    rel_path = os.path.relpath(file_path, KNOWLEDGE_DIR)
    parts = rel_path.split(os.sep)
    category = parts[0] if len(parts) > 0 else ''
    sub_category = parts[1] if len(parts) > 1 else ''
    return category, sub_category

def sync():
    """同步 Markdown 到 SQLite"""
    if not os.path.exists(DB_PATH):
        init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 获取已有的知识点（用于保留复习数据）
    cursor.execute("SELECT id, title, category, sub_category, mastery, review_count, last_reviewed_at, next_review_date FROM knowledge_points")
    existing = {}
    for row in cursor.fetchall():
        key = (row[1], row[2], row[3])  # (title, category, sub_category)
        existing[key] = {
            'id': row[0],
            'mastery': row[4],
            'review_count': row[5],
            'last_reviewed_at': row[6],
            'next_review_date': row[7]
        }

    markdown_files = get_all_markdown_files()
    synced_titles = set()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            category, sub_category = get_category_from_path(md_file)
            frontmatter, body = parse_frontmatter(content)
            content_text, code_example = extract_code_examples(body)

            title = frontmatter.get('title', os.path.splitext(os.path.basename(md_file))[0])

            # 检查是否已存在
            key = (title, category, sub_category)
            if key in existing:
                # 增量更新：保留复习字段，更新内容字段
                record = existing[key]
                cursor.execute('''
                    UPDATE knowledge_points SET
                        content = ?,
                        code_example = ?,
                        tags = ?,
                        status = ?,
                        difficulty = ?,
                        level = ?,
                        source = ?,
                        priority = ?,
                        related_ids = ?,
                        personal_notes = ?,
                        updated_at = ?
                    WHERE id = ?
                ''', [
                    content_text,
                    code_example,
                    frontmatter.get('tags', '[]'),
                    frontmatter.get('status', '待学'),
                    frontmatter.get('difficulty', 1),
                    frontmatter.get('level', '入门'),
                    frontmatter.get('source', ''),
                    frontmatter.get('priority', '中'),
                    frontmatter.get('related_ids', '[]'),
                    frontmatter.get('personal_notes', ''),
                    now,
                    record['id']
                ])
            else:
                # 新增
                cursor.execute('''
                    INSERT INTO knowledge_points (
                        title, category, sub_category, content, code_example,
                        tags, status, mastery, difficulty, level, source,
                        priority, related_ids, personal_notes, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', [
                    title,
                    category,
                    sub_category,
                    content_text,
                    code_example,
                    frontmatter.get('tags', '[]'),
                    frontmatter.get('status', '待学'),
                    frontmatter.get('mastery', 0),
                    frontmatter.get('difficulty', 1),
                    frontmatter.get('level', '入门'),
                    frontmatter.get('source', ''),
                    frontmatter.get('priority', '中'),
                    frontmatter.get('related_ids', '[]'),
                    frontmatter.get('personal_notes', ''),
                    now,
                    now
                ])

            synced_titles.add(key)
            print(f"同步: {title} ({category}/{sub_category})")

        except Exception as e:
            print(f"错误: {md_file} - {e}")

    # 删除 orphan（Markdown 中已删除的）
    cursor.execute("SELECT id, title, category, sub_category FROM knowledge_points")
    for row in cursor.fetchall():
        key = (row[1], row[2], row[3])
        if key not in synced_titles:
            cursor.execute("DELETE FROM knowledge_points WHERE id = ?", [row[0]])
            print(f"删除 orphan: {row[1]}")

    conn.commit()
    conn.close()
    print("同步完成")

if __name__ == '__main__':
    sync()