from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'  # セッション管理のためのキー

# データベース設定（PostgreSQL）
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://guest:password@postgres_db/my-db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ユーザーモデル
class Users(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# クラブモデル
class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)

# メンバーモデル
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    club = db.relationship('Clubs', backref=db.backref('members', lazy=True))

# データベース初期化
@app.route('/init', methods=['GET'])
def init_db():
    db.create_all()
    admin = Users(id='001', name='Admin', password='admin', is_admin=True)
    db.session.add(admin)
    db.session.commit()
    return "Database initialized!"

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']
        user = Users.query.filter_by(id=user_id, password=password).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('home'))
        else:
            return "Invalid credentials!"
    return render_template('login.html')

# ログアウト
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# ホームページ
@app.route('/', methods=['GET'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    clubs = Clubs.query.all()
    members = Members.query.all()
    return render_template('index.html', clubs=clubs, members=members, is_admin=session.get('is_admin', False))

# ユーザ登録（管理者専用）
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'user_id' not in session or not session.get('is_admin', False):
        return "Unauthorized", 403
    if request.method == 'POST':
        user_id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        is_admin = True if request.form.get('is_admin') == 'on' else False
        new_user = Users(id=user_id, name=name, password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_user.html')

# クラブ登録
@app.route('/add_club', methods=['POST'])
def add_club():
    if 'user_id' not in session or not session.get('is_admin', False):
        return "Unauthorized", 403
    club_name = request.form['club_name']
    description = request.form['description']
    capacity = request.form['capacity']
    new_club = Clubs(club_name=club_name, description=description, capacity=int(capacity))
    db.session.add(new_club)
    db.session.commit()
    return redirect(url_for('home'))

# クラブ削除（管理者のみ）
@app.route('/clubs/<int:club_id>', methods=['DELETE'])
def delete_club(club_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        return {"message": "Unauthorized"}, 403
    club = Clubs.query.get(club_id)
    if not club:
        return {"message": "Club not found"}, 404
    db.session.delete(club)
    db.session.commit()
    return {"message": "Club deleted successfully"}, 200

# メンバー登録
@app.route('/add_member', methods=['POST'])
def add_member():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    name = request.form['name']
    grade = int(request.form['grade'])
    club_id = int(request.form['club_id'])
    contact = request.form['contact']
    new_member = Members(name=name, grade=grade, club_id=club_id, contact=contact)
    db.session.add(new_member)
    db.session.commit()
    return redirect(url_for('home'))

# メンバー削除（管理者のみ）
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if 'user_id' not in session or not session.get('is_admin', False):
        return {"message": "Unauthorized"}, 403
    member = Members.query.get(member_id)
    if not member:
        return {"message": "Member not found"}, 404
    db.session.delete(member)
    db.session.commit()
    return {"message": "Member deleted successfully"}, 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
