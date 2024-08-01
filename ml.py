import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('stats.csv')
df.fillna(0, inplace = True)

def process_value(x):
    x = str(x)
    if '(' in x and '%' in x:
        return float(x.split(' ')[0])
    else:
        return float(x)

df['Saves per game'] = df['Saves per game'].apply(lambda x: process_value(x))
df['Scoring frequency'] = df['Scoring frequency'].apply(lambda x: int(x.split('m')[0]))
df['Accurate per game'] = df['Accurate per game'].apply(lambda x: int(x.split('(')[1].split('%')[0]))
df['Acc. long balls'] = df['Acc. long balls'].apply(lambda x: int(x.split('(')[1].split('%')[0]))
df['Acc. crosses'] = df['Acc. crosses'].apply(lambda x: int(x.split('(')[1].split('%')[0]))
df['Succ. dribbles'] = df['Succ. dribbles'].apply(lambda x: float(x.split('(')[0]))
df['Total duels won'] = df['Total duels won'].apply(lambda x: int(x.split('(')[1].split('%')[0]))
df['Aerial duels won'] = df['Aerial duels won'].apply(lambda x: int(x.split('(')[1].split('%')[0]))

position_mapping = {
        'CF': 'Forward',
        'SS': 'Forward',
        'LW': 'Forward',
        'RW': 'Forward',
        'AMF': 'Midfielder',
        'CMF': 'Midfielder',
        'DMF': 'Midfielder',
        'LM': 'Midfielder',
        'RM': 'Midfielder',
        'CB': 'Defender',
        'LB': 'Defender',
        'RB': 'Defender',
        'GK': 'Goalkeeper'}

df['Position Group'] = df['Position'].map(position_mapping)
df['ID'] = df.index

predictors = df[['Age', 'Total played', 'Started', 'Minutes per game', 'Goals conceded per game', 'Saves per game', 'Goals', 'Scoring frequency', 'Goals per game', 'Shots per game', 'Shots on target per game','Assists', 'Key passes per game', 'Accurate per game', 'Acc. long balls', 'Acc. crosses','Clean sheets', 'Interceptions per game', 'Balls recovered per game', 'Dribbled past per game', 'Clearances per game', 'Errors leading to shot', 'Succ. dribbles', 'Total duels won', 'Aerial duels won', 'Fouls', 'Was fouled', 'Offsides', 'Goal kicks per game', 'Yellow', 'Yellow-red', 'Red']]
columns = ['Age', 'Total played', 'Started', 'Minutes per game', 'Goals conceded per game', 'Saves per game', 'Goals', 'Scoring frequency', 'Goals per game', 'Shots per game', 'Shots on target per game','Assists', 'Key passes per game', 'Accurate per game', 'Acc. long balls', 'Acc. crosses','Clean sheets', 'Interceptions per game', 'Balls recovered per game', 'Dribbled past per game', 'Clearances per game', 'Errors leading to shot', 'Succ. dribbles', 'Total duels won', 'Aerial duels won', 'Fouls', 'Was fouled', 'Offsides', 'Goal kicks per game', 'Yellow', 'Yellow-red', 'Red']

scl = StandardScaler()
predictors_scaled = pd.DataFrame(scl.fit_transform(predictors), columns=columns)

def recommended_k_players_df(player, k_players = 100):
    pos_group = list(df['Position Group'][df['Name']==player])[0]

    if pos_group == 'Forward':
        indices = list(df[(df['Position Group'] == 'Forward')|(df['Position Group'] == 'Midfielder')].index.values)
    elif pos_group == 'Midfielder':
        indices = list(df[(df['Position Group'] == 'Forward')|(df['Position Group'] == 'Midfielder')].index.values)
    elif pos_group == 'Defender':
        indices = list(df[(df['Position Group'] == 'Defender')|(df['Position Group'] == 'Forward')].index.values)
    elif pos_group == 'Goalkeeper':
        indices = list(df[(df['Position Group'] == 'Goalkeeper')].index.values)

    predictors_scaled_subset = predictors_scaled.iloc[indices, :]
    predictors_subset = predictors.iloc[indices, :]

    #Fit KNN for the k_players within that position group
    recommendations = NearestNeighbors(n_neighbors=k_players, algorithm='auto').fit(predictors_scaled_subset)

    #Pass the player name from the dataset to the function and get 5 similar players as output
    player_indices = recommendations.kneighbors(predictors_scaled_subset)[1]

    #Get player index
    df_subset = df.iloc[indices,:].reset_index()
    index = df_subset[df_subset['Name']==player].index.tolist()[0]

    #Make variables global
    global recommend_list
    global recommended_df
    global recommended_names

    recommended_list = []

    recommended_df = predictors_subset.iloc[list(player_indices[index][:]),:]
    recommend_list = list(df_subset.iloc[list(player_indices[index][:]),:].ID)
    recommend_list.insert(0, index)

    recommended_names = df['Name'][df.ID.isin(recommend_list)]
    return recommend_list, recommended_names, recommended_df
