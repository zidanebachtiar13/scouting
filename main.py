from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from database import db, Team, teams, Player, players, code

app = Flask(__name__)
app.config['SECRET_KEY'] = '36dd292533174299fb0c34665df468bb881756ca9eaf9757d0cfde38f9ededa1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
Bootstrap5(app)

db.init_app(app)

with app.app_context():
    db.create_all()

'''
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
def select_team():
    clubs = db.session.execute(db.select(Team)).scalars()
    return render_template('index.html', clubs=clubs)

@app.route('/players/<alias>')
def select_player(alias):
    result = db.get_or_404(Team, alias)
    players = result.players
    return render_template('players.html', players=players)

@app.route('/auth')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
