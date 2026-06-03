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
);

CREATE INDEX IF NOT EXISTS idx_category ON knowledge_points(category);
CREATE INDEX IF NOT EXISTS idx_sub_category ON knowledge_points(sub_category);
CREATE INDEX IF NOT EXISTS idx_status_mastery ON knowledge_points(status, mastery);
CREATE INDEX IF NOT EXISTS idx_tags ON knowledge_points(tags);