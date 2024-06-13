from flask_sqlalchemy import SQLAlchemy, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from datetime import datetime

# DB 기본 코드
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.secret_key = 'your_secret_key_here'

# 게시판 DB 연결
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'board.db')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False,
                    default=datetime.utcnow().date)
    time = db.Column(db.Time, nullable=False,
                    default=datetime.utcnow().time)
    views = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content
        self.date = datetime.utcnow().date()
        self.time = datetime.utcnow().time()

    def __repr__(self):
        return f'<Post {self.title}>'


class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)

    def __init__(self, title, start, username):
        self.title = title
        self.start = start
        self.username = username

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, email, username, password, fullname):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)  # 비밀번호 해싱
        self.fullname = fullname


with app.app_context():
    db.create_all()
    db.create_all()
    db.create_all()

    if not Memo.query.first():
        sample_user = User.query.first()
        sample_memo = Memo(title='Sample Memo', start='2024-06-13', user_id=session['user_id'])
        db.session.add(sample_memo)
        db.session.commit()


# 게시판 라우트 시작
@app.route("/board/")
def board():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = Post.query.order_by(Post.date.desc(), Post.time.desc()).paginate(
        page=page, per_page=per_page)
    return render_template('board.html', posts=posts, username=session['username'])


@app.route("/board/<int:post_id>")
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = session['username']
    return jsonify({
        'id': post.id,
        'title': post.title,
        'author': post.author,
        'date': post.date.strftime('%Y-%m-%d'),
        'time': post.time.strftime('%H:%M:%S'),
        'content': post.content,
        'views': post.views,
        'current_user': current_user
    })


@app.route("/board/create/", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        title_receive = request.form.get("title")
        author_receive = session['username']
        content_receive = request.form.get("content")

        post = Post(title=title_receive, author=author_receive,
                    content=content_receive)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('board'))
    return render_template('board.html')


@app.route("/board/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200


@app.route("/board/edit/<int:post_id>", methods=["POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    title_receive = request.form.get("title")
    content_receive = request.form.get("content")

    post.title = title_receive
    post.content = content_receive

    db.session.commit()
    return redirect(url_for('board'))


@app.route('/board/view/<int:post_id>', methods=['POST'])
def increase_view_count(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1
    db.session.commit()
    return jsonify({'success': True, 'new_view_count': post.views})
# 게시판 라우트 끝


# 캘린더 라우트 시작

@app.route('/calendar/')
def calendar():
    return render_template('calendar.html')


@app.route('/calendar/memos')
def get_memos():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    user = User.query.filter_by(username=session['username']).first()
    memos = Memo.query.filter_by(username=user.username).all()
    memos_list = [{'id': memo.id, 'title': memo.title, 'start': memo.start} for memo in memos]
    return jsonify(memos_list)


@app.route('/calendar/add_memo', methods=['POST'])
def add_memo():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    username = session['username']
    title = request.form['title']
    date = request.form['date']
    memo = Memo(title=title, start=date, username=username)
    db.session.add(memo)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/calendar/update_memo', methods=['PUT'])
def update_memo():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    username = session['username']
    memo_id = request.form['id']
    title = request.form['title']
    memo = Memo.query.filter_by(id=memo_id, username=username).first()
    if memo:
        memo.title = title
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Memo not found'}), 404


@app.route('/calendar/delete_memo', methods=['DELETE'])
def delete_memo():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized access'}), 401

    username = session['username']
    memo_id = request.get_json().get('id')
    memo = Memo.query.filter_by(id=memo_id, username=username).first()
    if memo:
        db.session.delete(memo)
        db.session.commit()
        return '', 204
    return jsonify({'error': 'Memo not found'}), 404


@app.route("/filtered_board/")
def filtered_board():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Post 모델에서 author가 'asdf'인 것들만 필터링하여 가져옵니다.
    posts = Post.query.filter_by(author=session['username']).order_by(Post.date.desc(), Post.time.desc()).paginate(
        page=page, per_page=per_page)
    
    return render_template('board.html', posts=posts, username=session.get('username'))
# 캘린더 라우트 끝

# 로그인 라우트 시작


admin = Admin(app, name='User Management', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('board', username=session['username']))
    else:
        return render_template('login.html')


@app.route('/login/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        session['username'] = user.username  # 세션에 사용자 이름 저장
        return redirect(url_for('board', username=user.username))
    else:
        flash('아이디 또는 비밀번호가 맞지 않습니다.')
        return redirect(url_for('index'))


@app.route('/login/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        # 중복된 사용자 이름 확인
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = '이미 사용 중인 닉네임입니다. 다른 닉네임을 입력해주세요.'
            return render_template('register.html', error=error)

        # 사용자 데이터베이스에 저장
        new_user = User(email, username, password, fullname)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login/welcome/<username>')
def welcome(username):
    if 'username' in session and session['username'] == username:
        user = User.query.filter_by(username=username).first()
        return render_template('welcome.html', fullname=user.fullname)
    else:
        return redirect(url_for('index'))


@app.route('/login/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# 로그인 라우트 끝


if __name__ == "__main__":
    app.run(debug=True)
