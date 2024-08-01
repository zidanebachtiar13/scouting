from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, current_user, logout_user
from database import db, User, users, Team, teams, Player, players, Statistic, code
from ml import recommended_k_players_df
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '36dd292533174299fb0c34665df468bb881756ca9eaf9757d0cfde38f9ededa1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

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
    goals_conceded_per_game = player['Goals conceded per game']
    saves_per_game = player['Saves per game']
    clean_sheets = player['Clean sheets']
    goal_kicks_per_game = player['Goal kicks per game']
    if pd.isna(goals_conceded_per_game):
        goals_conceded_per_game = 0
    if pd.isna(saves_per_game):
        saves_per_game = 0
    if pd.isna(clean_sheets):
        clean_sheets = 0
    if pd.isna(goal_kicks_per_game):
        goal_kicks_per_game = 0
        
    new_player = Player(
            name = player['Name'],
            age = player['Age'],
            height = player['Height'],
            market_value = player['Market Value'],
            img_url = player['img_url'],
            position = player['Position'],
            team_alias = code[player['Team']])
    new_stats = Statistic(
            total_played = player['Total played'],
            started = player['Started'],
            minutes_per_game = player['Minutes per game'],
            goals_conceded_per_game = goals_conceded_per_game,
            saves_per_game = saves_per_game,
            goals = player['Goals'],
            scoring_frequency = player['Scoring frequency'],
            goals_per_game = player['Goals per game'],
            shots_per_game = player['Shots per game'],
            shots_on_target_per_game = player['Shots on target per game'],
            assists = player['Assists'],
            key_passes_per_game = player['Key passes per game'],
            accurate_per_game = player['Accurate per game'],
            acc_long_balls = player['Acc. long balls'],
            acc_crosses = player['Acc. crosses'],
            clean_sheets = clean_sheets,
            interceptions_per_game = player['Interceptions per game'],
            balls_recovered_per_game = player['Balls recovered per game'],
            dribbled_past_per_game = player['Dribbled past per game'],
            clearances_per_game = player['Clearances per game'],
            errors_leading_to_shot = player['Errors leading to shot'],
            succ_dribbles = player['Succ. dribbles'],
            total_duels_won = player['Total duels won'],
            aerial_duels_won = player['Aerial duels won'],
            fouls = player['Fouls'],
            was_fouled = player['Was fouled'],
            offsides = player['Offsides'],
            goal_kicks_per_game = goal_kicks_per_game,
            yellow = player['Yellow'],
            yellow_red = player['Yellow-red'],
            red = player['Red'],
            player_id = i+1)
    with app.app_context():
        db.session.add(new_player)
        db.session.add(new_stats)
        db.session.commit()
'''

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        elif current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def main():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.id == 1:
        return redirect(url_for('admin'))
    return render_template('index.html', logged_in=current_user.is_authenticated)

@app.route('/teams')
def select_team():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    clubs = db.session.execute(db.select(Team)).scalars()
    return render_template('select.html', clubs=clubs, logged_in=current_user.is_authenticated)

@app.route('/players/<alias>')
def select_player(alias):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    result = db.get_or_404(Team, alias)
    players = result.players
    return render_template('select.html', players=players, logged_in=current_user.is_authenticated)

@app.route('/player/<int:id>')
def player_details(id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    player = db.get_or_404(Player, id)
    stats = player.stats
    recommendations = recommended_k_players_df(player.name, 4)[0][2:]
    recommendation = [x + 1 for x in recommendations]
    recommendations = Player.query.filter(Player.id.in_(recommendation)).all()
    return render_template('player.html', player=player, stats=stats, recommendations=recommendations, logged_in=current_user.is_authenticated)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
       search = db.session.query(Player).filter(or_(Player.name.like('%' + request.form['search'] + '%'), Player.position.like('%' + request.form['search'] + '%'))).all()
       return render_template('search.html', players=search)
    return render_template('search.html', logged_in=current_user.is_authenticated)

@app.route('/auth', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.session.execute(db.select(User).where(User.username == request.form['username'])).scalar()
        if not user or not check_password_hash(user.password, request.form['password']):
            flash('Incorrect username or password')
            return redirect(url_for('login'))
        elif user.id == 1:
            login_user(user)
            return redirect(url_for('admin'))
        elif user.id != 1:
            login_user(user)
            return redirect(url_for('main'))
    return render_template('login.html', logged_in=current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@admin_only
def admin():
    return render_template('admin.html', logged_in=current_user.is_authenticated)

@app.route('/list/<route>')
@admin_only
def list(route):
    if route == 'teams':
        lists = db.session.execute(db.select(Team)).scalars()
    elif route == 'players':
        lists = db.session.execute(db.select(Player)).scalars()
    elif route == 'users':
        lists = db.session.execute(db.select(User)).scalars()
    return render_template('list.html', lists=lists, route=route, logged_in=current_user.is_authenticated)

@app.route('/add/<route>', methods=['GET', 'POST'])
@admin_only
def add(route):
    if request.method == 'POST':
        if route == 'teams':
            new_team = Team(alias=request.form['alias'],
                            name=request.form['team_name'],
                            img_url=request.form['img_url'])
            db.session.add(new_team)
            db.session.commit()
            return redirect(url_for('list', route=route))
        elif route == 'players':
            new_player = Player(name=request.form['name'],
                                age=request.form['age'],
                                height=request.form['height'],
                                market_value=request.form['market_value'],
                                img_url=request.form['img_url'],
                                position=request.form['position'],
                                team_alias=request.form['team_alias'])
            db.session.add(new_player)
            db.session.commit()
            return redirect(url_for('list', route=route))
        elif route == 'users':
            user = db.session.execute(db.select(User).where(User.username == request.form['username'])).scalar()
            if user:
                flash('User exist')
                return redirect(url_for('add', route=route))
            elif request.form['password'] != request.form['retype_password']:
                flash('Password mismatch')
                return redirect(url_for('add', route=route))
            else:
                new_user = User(username=request.form['username'],
                                password=generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('list', route=route))
    return render_template('form.html', route=route, logged_in=current_user.is_authenticated)

@app.route('/edit/<route>', methods=['GET', 'POST'])
@admin_only
def edit(route):
    code = request.args.get('code')
    if route == 'teams':
        data = db.get_or_404(Team, code)
    elif route == 'players':
        data = db.get_or_404(Player, code)
    elif route == 'users':
        data = db.get_or_404(User, code)
    if request.method == 'POST':
        if route == 'teams':
            data.alias = request.form['alias']
            data.name = request.form['team_name']
            data.img_url = request.form['img_url']
            db.session.commit()
            return redirect(url_for('list', route=route))
        elif route == 'players':
            data.name = request.form['name']
            data.age = request.form['age']
            data.height = request.form['height']
            data.market_value = request.form['market_value']
            data.img_url = request.form['img_url']
            data.position = request.form['position']
            data.team_alias = request.form['team_alias']
            db.session.commit()
            return redirect(url_for('list', route=route))
        elif route == 'users':
            if not check_password_hash(data.password, request.form['current_password']):
                flash('Current password incorrect')
                return redirect(url_for('edit', code=code, route=route))
            elif request.form['new_password'] != request.form['retype_password']:
                flash('New password mismatch')
                return redirect(url_for('edit', code=code, route=route))
            else:
                data.password = generate_password_hash(request.form['new_password'], method='pbkdf2:sha256', salt_length=8)
                db.session.commit()
                return redirect(url_for('list', route=route))
    return render_template('form.html', route=route, data=data, logged_in=current_user.is_authenticated)

@app.route('/delete/<route>')
@admin_only
def delete(route):
    code = request.args.get('code')
    if route == 'teams':
        data = db.get_or_404(Team, code)
    elif route == 'players':
        data = db.get_or_404(Player, code)
    elif route == 'users':
        data = db.get_or_404(User, code)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('list', route=route))

if __name__ == '__main__':
    app.run(debug=True)
