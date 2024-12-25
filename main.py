from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# データベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///club_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# テーブル定義
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    contact = db.Column(db.String(50), nullable=False)

    # リレーションを定義（クラブ情報にアクセスできるようにする）
    club = db.relationship('Clubs', backref=db.backref('members', lazy=True))

class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    club_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)

# ホームページ（部活と新入生の登録ページを統合）
@app.route('/', methods=['GET'])
def home():
    clubs = Clubs.query.all()  # 部活一覧を取得
    members = Members.query.all()    
    return render_template('index.html', clubs=clubs, members=members)

# 部活の登録フォーム
@app.route('/add_club', methods=['POST'])
def add_club():
    club_name = request.form['club_name']
    description = request.form['description']
    capacity = request.form['capacity']

    new_club = Clubs(
        club_name=club_name,
        description=description,
        capacity=int(capacity)
    )
    db.session.add(new_club)
    db.session.commit()
    return redirect(url_for('home'))

# 新入生の登録フォーム
@app.route('/add_member', methods=['POST'])
def add_member():
    name = request.form['name']
    grade = int(request.form['grade'])
    club_id = int(request.form['club_id'])
    contact = request.form['contact']

    new_member = Members(
        name=name,
        grade=grade,
        club_id=club_id,
        contact=contact
    )
    db.session.add(new_member)
    db.session.commit()
    return redirect(url_for('home'))

# 初期化用エンドポイント
@app.route('/init', methods=['GET'])
def init_db():
    db.create_all()
    return "Database initialized!"

# 部活の登録（API経由）
@app.route('/clubs', methods=['POST'])
def create_club():
    data = request.json
    new_club = Clubs(
        club_name=data['club_name'],
        description=data.get('description', ''),
        capacity=data['capacity']
    )
    db.session.add(new_club)
    db.session.commit()
    return jsonify({'message': 'Club created successfully!'})

# 部活一覧の取得（API経由）
@app.route('/clubs', methods=['GET'])
def get_clubs():
    clubs = Clubs.query.all()
    return jsonify([{
        'id': club.id,
        'club_name': club.club_name,
        'description': club.description,
        'capacity': club.capacity
    } for club in clubs])

# 新入生登録（API経由）
@app.route('/members', methods=['POST'])
def register_member():
    data = request.json
    new_member = Members(
        name=data['name'],
        grade=data['grade'],
        club_id=data['club_id'],
        contact=data['contact']
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member registered successfully!'})

# 新入生一覧の取得（API経由）
@app.route('/members', methods=['GET'])
def get_members():
    members = Members.query.join(Clubs, Members.club_id == Clubs.id).add_columns(
        Members.id, Members.name, Members.grade, Members.contact, Clubs.club_name).all()
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'grade': member.grade,
        'contact': member.contact,
        'club_name': club_name
    } for member, club_name in members])

# 登録情報の編集
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Members.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    data = request.json
    member.name = data.get('name', member.name)
    member.grade = data.get('grade', member.grade)
    member.contact = data.get('contact', member.contact)
    member.club_id = data.get('club_id', member.club_id)
    db.session.commit()
    return jsonify({'message': 'Member updated successfully!'})

# 登録情報の削除
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Members.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)