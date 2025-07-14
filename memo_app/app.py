from flask import Flask, request, redirect, render_template, url_for
from datetime import datetime

app = Flask(__name__)

# 🔧 MySQL 연결 함수
import MySQLdb

def get_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="1234",  
        db="memo_db",
        charset="utf8"
    )

# ✅ DB 초기화 (처음 실행 시 1번만 호출)
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date VARCHAR(20) NOT NULL,
            content TEXT
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# ✅ 홈 → 목록 리디렉션
@app.route('/')
def home():
    return redirect(url_for('show_memos'))

# ✅ 전체 목록 조회 (Read)
@app.route('/success')
def show_memos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memos ORDER BY id DESC")
    memos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", memos=memos)

# ✅ 메모 추가 (Create)
@app.route('/memo/add', methods=['POST'])
def add_memo():
    content = request.form['content']
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memos (date, content) VALUES (%s, %s)", (today, content))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('show_memos'))

# ✅ 수정 폼
@app.route('/memo/edit/<int:memo_id>')
def edit_memo(memo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memos WHERE id = %s", (memo_id,))
    memo = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("edit_memo.html", memo=memo)

# ✅ 수정 처리 (Update)
@app.route('/memo/update/<int:memo_id>', methods=['POST'])
def update_memo(memo_id):
    content = request.form['content']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE memos SET content = %s WHERE id = %s", (content, memo_id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('show_memos'))

# ✅ 삭제 처리 (Delete)
@app.route('/memo/delete/<int:memo_id>')
def delete_memo(memo_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memos WHERE id = %s", (memo_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('show_memos'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
