from flask import Flask, render_template, request, jsonify, g
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "E:/知识库/sqlite/knowledge.db"

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/categories')
def get_categories():
    db = get_db()
    cursor = db.execute(
        "SELECT DISTINCT category FROM knowledge_points WHERE status != '废弃' ORDER BY category"
    )
    categories = [row['category'] for row in cursor]
    return jsonify(categories)

@app.route('/api/points')
def get_points():
    category = request.args.get('category')
    sub_category = request.args.get('sub_category')

    db = get_db()
    if category and sub_category:
        cursor = db.execute(
            "SELECT * FROM knowledge_points WHERE category = ? AND sub_category = ? AND status != '废弃' ORDER BY sort_order ASC",
            [category, sub_category]
        )
    elif category:
        cursor = db.execute(
            "SELECT * FROM knowledge_points WHERE category = ? AND status != '废弃' ORDER BY sort_order ASC",
            [category]
        )
    else:
        cursor = db.execute("SELECT * FROM knowledge_points WHERE status != '废弃' ORDER BY sort_order ASC")

    points = [dict(row) for row in cursor]
    return jsonify(points)

@app.route('/api/subcategories')
def get_subcategories():
    category = request.args.get('category')
    db = get_db()
    cursor = db.execute(
        "SELECT DISTINCT sub_category FROM knowledge_points WHERE category = ? AND status != '废弃' ORDER BY sub_category",
        [category]
    )
    subcategories = [row['sub_category'] for row in cursor]
    return jsonify(subcategories)

@app.route('/api/search')
def search():
    keyword = request.args.get('q', '')
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM knowledge_points WHERE (title LIKE ? OR content LIKE ? OR tags LIKE ?) AND status != '废弃' ORDER BY sort_order ASC",
        [f'%{keyword}%', f'%{keyword}%', f'%{keyword}%']
    )
    points = [dict(row) for row in cursor]
    return jsonify(points)

@app.route('/api/flashcard')
def flashcard():
    db = get_db()
    cursor = db.execute(
        "SELECT * FROM knowledge_points WHERE status != '废弃' ORDER BY RANDOM() LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        return jsonify(dict(row))
    return jsonify(None)

@app.route('/api/flashcard/answer', methods=['POST'])
def flashcard_answer():
    data = request.get_json()
    point_id = data.get('id')
    correct = data.get('correct', False)

    db = get_db()

    # 获取当前 mastery
    cursor = db.execute("SELECT mastery FROM knowledge_points WHERE id = ?", [point_id])
    row = cursor.fetchone()
    if not row:
        return jsonify({'error': '知识点不存在'}), 404

    current_mastery = row['mastery']

    # 计算新 mastery
    if correct:
        new_mastery = min(5, current_mastery + 1)
    else:
        new_mastery = max(1, current_mastery - 1)

    # 更新数据库
    db.execute('''
        UPDATE knowledge_points
        SET mastery = ?,
            review_count = review_count + 1,
            last_reviewed_at = datetime('now', 'localtime')
        WHERE id = ?
    ''', [new_mastery, point_id])
    db.commit()

    return jsonify({'success': True, 'mastery': new_mastery})

@app.route('/api/test')
def test():
    sub_category = request.args.get('sub_category')
    db = get_db()

    # 获取一个随机题目
    if sub_category:
        cursor = db.execute(
            "SELECT * FROM knowledge_points WHERE sub_category = ? AND status != '废弃' ORDER BY RANDOM() LIMIT 1",
            [sub_category]
        )
    else:
        cursor = db.execute(
            "SELECT * FROM knowledge_points WHERE status != '废弃' ORDER BY RANDOM() LIMIT 1"
        )

    question = cursor.fetchone()
    if not question:
        return jsonify(None)

    # 获取3个错误选项（同分类）
    if sub_category:
        cursor = db.execute(
            "SELECT * FROM knowledge_points WHERE sub_category = ? AND id != ? AND status != '废弃' ORDER BY RANDOM() LIMIT 3",
            [sub_category, question['id']]
        )
    else:
        cursor = db.execute(
            "SELECT * FROM knowledge_points WHERE id != ? AND status != '废弃' ORDER BY RANDOM() LIMIT 3",
            [question['id']]
        )

    wrong_options = [dict(row) for row in cursor]

    return jsonify({
        'question': dict(question),
        'options': wrong_options
    })

@app.route('/api/test/answer', methods=['POST'])
def test_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_id = data.get('selected_id')

    db = get_db()

    # 获取题目信息
    cursor = db.execute("SELECT * FROM knowledge_points WHERE id = ?", [question_id])
    question = cursor.fetchone()
    if not question:
        return jsonify({'error': '题目不存在'}), 404

    is_correct = (selected_id == question_id)

    # 如果答对了，更新 mastery
    if is_correct:
        current_mastery = question['mastery']
        new_mastery = min(5, current_mastery + 1)
        db.execute('''
            UPDATE knowledge_points
            SET mastery = ?,
                review_count = review_count + 1,
                last_reviewed_at = datetime('now', 'localtime')
            WHERE id = ?
        ''', [new_mastery, question_id])
        db.commit()
    else:
        new_mastery = question['mastery']

    return jsonify({
        'correct': is_correct,
        'correct_id': question_id,
        'mastery': new_mastery
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)