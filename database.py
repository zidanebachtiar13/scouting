from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float
import pandas as pd

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    password: Mapped[str] = mapped_column(String(100))

class Team(db.Model):
    __tablename__ = 'teams'
    alias: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    img_url: Mapped[str] = mapped_column(String(100), nullable=False)
    players = relationship('Player', back_populates='team')

class Player(db.Model):
    __tablename__ = 'players'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[str] = mapped_column(String(10), nullable=False)
    market_value: Mapped[str] = mapped_column(String(10), nullable=False)
    img_url: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[str] = mapped_column(String(5), nullable=False)
    team_alias: Mapped[str] = mapped_column(String(20), db.ForeignKey('teams.alias'))
    team = relationship('Team', back_populates='players')
    stats = relationship('Statistic', back_populates='player')

class Statistic(db.Model):
    __tablename__ = 'stats'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    total_played: Mapped[int] = mapped_column(Integer)
    started: Mapped[int] = mapped_column(Integer)
    minutes_per_game: Mapped[int] = mapped_column(Integer)
    goals_conceded_per_game: Mapped[float] = mapped_column(Float)
    saves_per_game: Mapped[str] = mapped_column(String(20))
    goals: Mapped[int] = mapped_column(Integer)
    scoring_frequency: Mapped[str] = mapped_column(String(20))
    goals_per_game: Mapped[float] = mapped_column(Float)
    shots_per_game: Mapped[float] = mapped_column(Float)
    shots_on_target_per_game: Mapped[float] = mapped_column(Float)
    assists: Mapped[int] = mapped_column(Integer)
    key_passes_per_game: Mapped[float] = mapped_column(Float)
    accurate_per_game: Mapped[str] = mapped_column(String(20))
    acc_long_balls: Mapped[str] = mapped_column(String(20))
    acc_crosses: Mapped[str] = mapped_column(String(20))
    clean_sheets: Mapped[int] = mapped_column(Integer)
    interceptions_per_game: Mapped[float] = mapped_column(Float)
    balls_recovered_per_game: Mapped[float] = mapped_column(Float)
    dribbled_past_per_game: Mapped[float] = mapped_column(Float)
    clearances_per_game: Mapped[float] = mapped_column(Float)
    errors_leading_to_shot: Mapped[int] = mapped_column(Integer)
    succ_dribbles: Mapped[str] = mapped_column(String(20))
    total_duels_won: Mapped[str] = mapped_column(String(20))
    aerial_duels_won: Mapped[str] = mapped_column(String(20))
    fouls: Mapped[float] = mapped_column(Float)
    was_fouled: Mapped[float] = mapped_column(Float)
    offsides: Mapped[float] = mapped_column(Float)
    goal_kicks_per_game: Mapped[float] = mapped_column(Float)
    yellow: Mapped[int] = mapped_column(Integer)
    yellow_red: Mapped[int] = mapped_column(Integer)
    red: Mapped[int] = mapped_column(Integer)
    player_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('players.id'))
    player = relationship('Player', back_populates='stats')

account = open('account.txt', 'r')
users = []
for acc in account:
    acc = acc.split(',')
    users.append({'username': acc[0], 'password': acc[1][:-1]})

teams = [{'alias': 'arema', 'name': 'Arema FC', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLYLBf0LmY32zajndwW0OxlgcrntemSniQAQ&s'},
         {'alias': 'bali', 'name': 'Bali United', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYxJ2JNKB7W_8ChneVsAERXExVTACSnkqngg&s'},
         {'alias': 'bhayangkara', 'name': 'Bhayangkara Presisi Indonesia FC', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/f/f3/Logo_Bhayangkara_FC.png'},
         {'alias': 'borneo', 'name': 'Borneo FC Samarinda', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6xf36Y0O_qt8BXo3zv16ZOQgXJtjwmtH70g&s'},
         {'alias': 'dewa', 'name': 'Dewa United FC', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/5/53/Dewa_United_FC.png'},
         {'alias': 'madura', 'name': 'Madura United FC', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/8/8a/Madura_United_FC.png'},
         {'alias': 'persebaya', 'name': 'Persebaya Surabaya', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/thumb/a/a1/Persebaya_logo.svg/1200px-Persebaya_logo.svg.png'},
         {'alias': 'persib', 'name': 'Persib Bandung', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/thumb/1/12/Logo_Persib.png/1200px-Logo_Persib.png'},
         {'alias': 'persija', 'name': 'Persija Jakarta', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/9/94/Persija_Jakarta_logo.png'},
         {'alias': 'persikabo', 'name': 'Persikabo 1973', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/0/05/Persikabo_1973_logo.png'},
         {'alias': 'persik', 'name': 'Persik Kediri', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTCJbsiy3Ksq2YIP62CaOHO5E_aBwaDygPow&s'},
         {'alias': 'persis', 'name': 'Persis Solo', 'img_url': 'https://upload.wikimedia.org/wikipedia/en/thumb/d/d6/Persis_Solo_logo.svg/1200px-Persis_Solo_logo.svg.png'},
         {'alias': 'persita', 'name': 'Persita Tangerang', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQod1lWtIXBZlpI_TunZbkc6rcN7M24YZm9pQ&s'},
         {'alias': 'barito', 'name': 'PS Barito Putera', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNEuEnMLS60jNva-Ov5BT2vvZLpLvi2AvInQ&s'},
         {'alias': 'psis', 'name': 'PSIS Semarang', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/f/f5/PSIS_logo.svg'},
         {'alias': 'psm', 'name': 'PSM Makassar', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnG2sW6o4ebIHtuPsAUiEZlgNn1eI_E2LD5A&s'},
         {'alias': 'pss', 'name': 'PSS Sleman', 'img_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQwqi5D7KEW3boyDUQ7dmz6aQdi5VAjmlf-g&s'},
         {'alias': 'rans', 'name': 'RANS Nusantara FC', 'img_url': 'https://upload.wikimedia.org/wikipedia/id/6/6f/RANS_Nusantara_FC_logo_baru.svg'}]

players = pd.read_csv('stats.csv')

code = {'Arema FC': 'arema',
        'Bali United': 'bali',
        'Bhayangkara Presisi Indonesia FC': 'bhayangkara',
        'Borneo FC Samarinda': 'borneo',
        'Dewa United FC': 'dewa',
        'Madura United FC': 'madura',
        'Persebaya Surabaya': 'persebaya',
        'Persib Bandung': 'persib',
        'Persija Jakarta': 'persija',
        'Persikabo 1973': 'persikabo',
        'Persik Kediri': 'persik',
        'Persis Solo': 'persis',
        'Persita Tangerang': 'persita',
        'PS Barito Putera': 'barito',
        'PSIS Semarang': 'psis',
        'PSM Makassar': 'psm',
        'PSS Sleman': 'pss',
        'RANS Nusantara FC': 'rans'}
