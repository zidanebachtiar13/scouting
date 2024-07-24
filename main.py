from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from database import db, User, users, Team, teams, Player, players, code
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '36dd292533174299fb0c34665df468bb881756ca9eaf9757d0cfde38f9ededa1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
Bootstrap5(app)

db.init_app(app)

with app.app_context():
    db.create_all()

'''
for user in users:
    new_user = User(
            username = user['username'],
            password = generate_password_hash(user['password'], method='pbkdf2:sha256', salt_length=8))
    with app.app_context():
        db.session.add(new_user)
        db.session.commit()

for team in teams:
    new_team = Team(
            alias = team['alias'],
            name = team['name'],
            img_url = team['img_url'])
    with app.app_context():
        db.session.add(new_team)
        db.session.commit()

for i, player in players.iterrows():
    new_player = Player(
            name = player['Name'],
            age = player['Age'],
            height = player['Height'],
            market_value = player['Market Value'],
            img_url = player['img_url'],
            position = player['Position'],
            team_alias = code[player['Team']])
    with app.app_context():
        db.session.add(new_player)
        db.session.commit()
'''

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/teams')
def select_team():
    clubs = db.session.execute(db.select(Team)).scalars()
    return render_template('select.html', clubs=clubs)

@app.route('/players/<alias>')
def select_player(alias):
    result = db.get_or_404(Team, alias)
    players = result.players
    return render_template('select.html', players=players)

@app.route('/player/<int:id>')
def player_details(id):
    return render_template('player.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
       search = db.session.query(Player).filter(or_(Player.name.like('%' + request.form['search'] + '%'), Player.position.like('%' + request.form['search'] + '%'))).all()
       return render_template('search.html', players=search)
    return render_template('search.html')

@app.route('/auth')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/list/<route>')
def list(route):
    if route == 'teams':
        lists = db.session.execute(db.select(Team)).scalars()
    elif route == 'players':
        lists = db.session.execute(db.select(Player)).scalars()
    elif route == 'users':
        lists = db.session.execute(db.select(User)).scalars()
    return render_template('list.html', lists=lists, route=route)

@app.route('/add')
def add():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
