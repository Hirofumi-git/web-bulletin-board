from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)

# セッション用の秘密鍵（実際にはもっと強力なランダムな鍵を使うこと）
app.secret_key = 'your_secret_key_here'

# ダミーのユーザー情報（本番環境ではDBを使用すべき）
users = {'admin': 'password123', 'guest1': '000111'}

# ログイン必須のデコレーター
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ダミーのメッセージリスト（本番環境ではDBを使用すべき）
messages = []

# ホームページ（掲示板）
@app.route('/')
@login_required
def index():
    return render_template("index.html", messages=messages)

# 掲示板の投稿を処理（POST）
@app.route('/post_message', methods=['POST'])
@login_required
def post_message():
    if request.method == 'POST':
        message = request.form['message']  # フォームからメッセージを受け取る
        username = session['username']  # ログインしているユーザー名を取得
        
        if message:
            # メッセージとユーザー名を一緒に保存
            messages.append({'username': username, 'message': message})
        return redirect(url_for('index'))  # 投稿後は掲示板ページにリダイレクト

# ログインページ（GET と POST メソッド対応）
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # ユーザー情報チェック
        if username in users and users[username] == password:
            session['username'] = username  # セッションにユーザー名を保存
            return redirect(url_for('index'))  # ログイン成功後、ホームへリダイレクト
        
        return 'Invalid credentials, please try again!'  # 認証失敗メッセージ
    
    # GETリクエスト時はログインフォームを表示
    return render_template('login.html')

# ログアウト
@app.route('/logout')
def logout():
    session.pop('username', None)  # セッションからユーザー名を削除
    return redirect(url_for('login'))  # ログアウト後はログイン画面にリダイレクト

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

