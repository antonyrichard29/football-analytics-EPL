import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from prettytable import PrettyTable
import random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

get_ipython().run_line_magic('matplotlib', 'inline')
# load dataset
# Replace 'your_path_here.csv' with the correct path to your dataset
epl_df = pd.read_csv('your_path_here')
epl_df.head()
# Print a summary ofthe DataFrame
epl_df.info()
# Print summary statistics of the DataFrame
epl_df.describe()
# Count the number of missing values (NaN) in each column of epl_df
epl_df.isna().sum()
# Create 2 new columns
epl_df['MinsPerMatch'] = (epl_df['Mins'] / epl_df['Matches']).astype(int)
epl_df['GoalsPerMatch'] = (epl_df['Goals'] / epl_df['Matches']).astype(float)
epl_df.head()
# Total Goals
Total_Goals = epl_df['Goals'].sum()
print(Total_Goals)
# Penalty Goals
Total_PenaltyGoals = epl_df['Penalty_Goals'].sum()
print(Total_PenaltyGoals)
# Penalty Attempts
Total_PenaltyAttempts = epl_df['Penalty_Attempted'].sum()
print(Total_PenaltyAttempts)
# Pie chart for penalties missed vsscored
plt.figure(figsize = (13, 6))
pl_not_scored = epl_df['Penalty_Attempted'].sum() - Total_PenaltyGoals
data = [pl_not_scored, Total_PenaltyGoals]
labels = ['Penalties Missed', 'Penalty Scored']
color_palette = sns.color_palette("Paired")
plt.pie(data, labels = labels, colors = color_palette, autopct = '%.0f%%')
plt.show()
# Unique positions
epl_df['Position'].unique()
# Total FW Players
epl_df[epl_df['Position'] == 'FW']
# Players from different nations
np.size((epl_df['Nationality'].unique()))
# Most players from which countries
nationality = epl_df.groupby('Nationality').size().sort_values(ascending = False)
nationality.head(10).plot(kind = 'bar', figsize = (12, 6), color = sns.color_palette('magma'))
# Clubs with maximum players in their squad
epl_df['Club'].value_counts().nlargest(5).plot(kind = 'bar', color =sns.color_palette("viridis"))
# Clubs with latest players in their squad
epl_df['Club'].value_counts().nsmallest(5).plot(kind = 'bar', color =
sns.color_palette("viridis"))
# Players based on age group
Under20 = epl_df[epl_df['Age'] <= 20]
age20_25 = epl_df[(epl_df['Age'] > 20) & (epl_df['Age'] <= 25)]
age25_30 = epl_df[(epl_df['Age'] > 25) & (epl_df['Age'] <= 30)]
Above30 = epl_df[epl_df['Age'] > 30]
# Assuming the following DataFrame exist: Under20, age20_25, age25_30 and Above30
x =np.array([Under20['Name'].count(),age20_25['Name'].count(),age25_30['Name'].count(),Above30['Name'].count()])
mylabels = ["<=20", ">20 & <=25", ">25 & <=30", ">30"]
plt.title('Total Players with Age Groups', fontsize=20)
plt.pie(x, labels=mylabels, autopct = "%.1f%%")
plt.show()
# Total under 20 players in each club
players_under_20 = epl_df[epl_df['Age'] < 20]
players_under_20['Club'].value_counts().plot(kind = 'bar', color =sns.color_palette("cubehelix"))
# Under 20 players in Manu
players_under_20[players_under_20["Club"] == 'Manchester United']
# Under 20 players in Chelsea
players_under_20[players_under_20["Club"] == 'Chelsea']
# Average age of players in each club
plt.figure(figsize = (12, 6))
sns.boxplot(x = 'Club', y = 'Age', data = epl_df)
plt.xticks(rotation = 90)
# Group the English Premier League DataFrame (epl_df) by club and count the number of players in each club
num_player = epl_df.groupby('Club').size()
data = (epl_df.groupby('Club')['Age'].sum()) / num_player
data.sort_values(ascending = False)
# Total assists from each club
Assits_by_club = pd.DataFrame(epl_df.groupby('Club', as_index = False)['Assists'].sum())
sns.set_theme(style = "whitegrid", color_codes = True)
ax = sns.barplot(x = 'Club', y = 'Assists', data = Assits_by_club.sort_values(by = 'Assists'), palette = 'tab20')
ax.set_xlabel("Club", fontsize = 30)
ax.set_ylabel("Assists", fontsize = 20)
plt.xticks(rotation = 75)
plt.rcParams["figure.figsize"] = (20, 8)
plt.title('Plot of Club vs Total Assists', fontsize = 20)
plt.show()
# Top 10 Assists
top_10_assists = epl_df[['Name', 'Club', 'Assists', 'Matches']].nlargest(n = 10, columns ='Assists')
top_10_assists
# Creating a DataFrame to group the total goals scored by each club
Goals_by_clubs = pd.DataFrame(epl_df.groupby('Club', as_index = False)['Goals'].sum())
sns.set_theme(style ="whitegrid", color_codes = True)
ax = sns.barplot(x = 'Club', y = 'Goals', data = Goals_by_clubs.sort_values(by ="Goals"), palette = 'rocket')
ax.set_xlabel("Club", fontsize = 30)
ax.set_ylabel("Goals", fontsize = 20)
plt.xticks(rotation =75)
plt.rcParams["figure.figsize"] = (20, 8)
plt.title('Plot of Club vs Total Goals', fontsize = 20)
plt.show()
# Most goals by players
top_10_goals = epl_df[['Name', 'Club', 'Goals', 'Matches']].nlargest(n = 10, columns ='Goals')
top_10_goals
# Goals per match
top_10_goals_per_match = epl_df[['Name', 'GoalsPerMatch', 'Matches', 'Goals']].nlargest(n = 10, columns = 'GoalsPerMatch')
top_10_goals_per_match
# Pie Chart - Goals with assist and without assist
plt.figure(figsize = (14, 7))
assists = epl_df['Assists'].sum()
data = [Total_Goals - assists, assists]
labels = ['Goals without assists', 'Goals with assists']
color = sns.color_palette('Set2')
plt.pie(data, labels = labels, colors = color, autopct ='%.0f%%')
plt.title('Percentage of Goals with Assists', fontsize = 20)
plt.show()
# Top 10 players with most yellow cards
epl_yellow = epl_df.sort_values(by = 'Yellow_Cards', ascending = False)[:10]
plt.figure(figsize = (20, 6))
plt.title("Players with the most yellow cards")
c = sns.barplot(x = epl_yellow['Name'], y = epl_yellow['Yellow_Cards'], label = 'Players', color ='yellow')
plt.ylabel('Number of Yellow Cards')
c.set_xticklabels(c.get_xticklabels(), rotation = 45)
plt.show()
# Group by Club and calculate team stats
team_stats = epl_df.groupby('Club').agg({
'Goals': 'sum',
'Assists': 'sum',
'Matches': 'sum',
'Yellow_Cards': 'sum',
'Red_Cards': 'sum' }).reset_index()
# Estimate Points (since detailed W/D/L not given)
team_stats['Points'] = np.random.randint(30, 90,size=len(team_stats)) # Placeholder random points
team_stats['Wins'] = (team_stats['Points'] // 3).astype(int)
team_stats['Draws'] = ((team_stats['Points'] % 3) + np.random.randint(0, 5, size=len(team_stats))).astype(int)
team_stats['Losses'] = 38 - (team_stats['Wins'] + team_stats['Draws'])
# Team Points
plt.figure(figsize=(16,8))
sns.barplot(x='Club', y='Points', data=team_stats.sort_values('Points', ascending=False), palette='Spectral')
plt.title('Club Pointsin EPL 20-21')
plt.xticks(rotation=90)
plt.show()
# Wins vs Losses per Club
team_stats.set_index('Club')[['Wins', 'Losses']].plot(kind='bar', stacked=True, figsize=(16,8), color=['green', 'red'])
plt.title('Wins vs Losses per Club')
plt.ylabel('Number of Matches')
plt.xticks(rotation=90)
plt.show()
player_performance = epl_df[['Name', 'Club', 'Goals', 'Assists', 'Matches', 'GoalsPerMatch']]
player_performance['CardsPerMatch'] = (epl_df['Yellow_Cards'] + epl_df['Red_Cards']) / epl_df['Matches']
# Top 10 Players - Goals Per Match
top_players = player_performance.sort_values(by='GoalsPerMatch', ascending=False).head(10)
print("Top 10 Players(Goals Per Match):")
print(top_players)
top_players[['Name', 'GoalsPerMatch']].set_index('Name').plot(kind='barh', color='blue', figsize=(10,7))
plt.title('Top 10 Players by Goals Per Match')
plt.xlabel('Goals Per Match')
plt.show()
# Creating a Match Dataset
match_data = pd.DataFrame({
'Team1': np.random.choice(team_stats['Club'], 100),
'Team2': np.random.choice(team_stats['Club'], 100)
})
# Merge points
match_data = match_data.merge(team_stats[['Club', 'Points']], left_on='Team1', right_on='Club').rename(columns={'Points':'Team1_Points'}).drop('Club', axis=1)
match_data = match_data.merge(team_stats[['Club', 'Points']], left_on='Team2', right_on='Club').rename(columns={'Points':'Team2_Points'}).drop('Club', axis=1)
# Target: Team1 wins (1) or Team2 wins (0)
match_data['Result'] = (match_data['Team1_Points'] > match_data['Team2_Points']).astype(int)
# Train-Test Split
X = match_data[['Team1_Points', 'Team2_Points']]
y = match_data['Result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Logistic Regression Model
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# Results
print("Match Prediction Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
# Bonus: Predict goals difference using Random Forest
regressor = RandomForestRegressor()
regressor.fit(X_train, y_train)
y_goals_pred = regressor.predict(X_test)
print("Sample Predicted Goals Difference:", y_goals_pred[:5])
# (I'm skipping re-pasting it here since you already have it. Assume it's there.)
def calculate_team_strength(team_df):
  attack_strength = team_df['Goals'].sum() + team_df['Assists'].sum()
  avg_goals_per_match = team_df['GoalsPerMatch'].mean()
  discipline_penalty = team_df['Yellow_Cards'].sum() * 0.1
  strength = attack_strength + avg_goals_per_match - discipline_penalty
  return strength
def predict_top_scorers(team_df):
  team_df['ScoringAbility'] = team_df['GoalsPerMatch'] + (team_df['Position'] == 'FW') * 0.5
  top_scorers = team_df.sort_values(by='ScoringAbility', ascending=False)[['Name','GoalsPerMatch', 'Position']].head(5)
  return top_scorers
# Choose match
choice = input("\nChoose Match Setup - Type 'Random' or 'Manual': ").strip().lower()
if choice == 'random':
  teams = random.sample(list(epl_df['Club'].unique()), 2)
  team1_name, team2_name = teams[0], teams[1]
else:
  team1_name = input("Enter Team 1 Name: ").strip()
  team2_name = input("Enter Team 2 Name: ").strip()
print(f"\n Predicting match between {team1_name} vs {team2_name}...")
# Team info
team1_df = epl_df[epl_df['Club'] == team1_name]
team2_df = epl_df[epl_df['Club'] == team2_name]

# Check if teams are found in the dataset
if team1_df.empty:
    print(f"Team '{team1_name}' not found in the dataset. Skipping match prediction.")
elif team2_df.empty:
    print(f"Team '{team2_name}' not found in the dataset. Skipping match prediction.")
else:
    team1_strength = calculate_team_strength(team1_df)
    team2_strength = calculate_team_strength(team2_df)
    team1_scorers = predict_top_scorers(team1_df)
    team2_scorers = predict_top_scorers(team2_df)

    # Win Probability Chart
    team_strengths = [team1_strength, team2_strength]
    labels = [team1_name, team2_name]
    colors = sns.color_palette('pastel')
    plt.figure(figsize=(7, 7))
    plt.pie(team_strengths, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Win Probability Prediction ', fontsize=20)
    plt.show()

    # Match Report PrettyTable
    table = PrettyTable()
    table.field_names = ["Team", "Predicted Goals", "Top Potential Goal Scorers"]
    team1_goals_pred = round(team1_strength / (team1_strength + team2_strength) * 5)
    team2_goals_pred = round(team2_strength / (team1_strength + team2_strength) * 5)
    team1_scorers_list = '\n'.join(team1_scorers['Name'].tolist())
    team2_scorers_list = '\n'.join(team2_scorers['Name'].tolist())
    table.add_row([team1_name, team1_goals_pred, team1_scorers_list])
    table.add_row([team2_name, team2_goals_pred, team2_scorers_list])
    print("\n" + "="*80)
    print(" Match Prediction Report ")
    print("="*80)
    print(table)

    # Predicted winner
    if team1_goals_pred > team2_goals_pred:
      winner = team1_name
    elif team2_goals_pred > team1_goals_pred:
      winner = team2_name
    else:
      winner = "Draw"
    print(f"\n Predicted Winner: {winner}")
    print("="*80)

    print("\n Starting Live Match Simulation...\n")
    minutes = 0
    team1_goals = 0
    team2_goals = 0
    goal_events = []

    # Combine top scorers for possible scorers
    team1_goal_prob = team1_scorers['Name'].tolist()
    team2_goal_prob = team2_scorers['Name'].tolist()

    while minutes <= 90:
      minutes += random.randint(1, 10) # Fast forward time randomly between 1-10 min
      if minutes > 90:
        break

      # Random chance of goal
      chance = random.random()
      if chance < 0.1: # ~10% chance that a goal is scored in that time
        scoring_team= random.choices([team1_name, team2_name], weights=[team1_strength, team2_strength])[0]
        if scoring_team == team1_name:
          scorer = random.choice(team1_goal_prob)
          team1_goals += 1
        else:
          scorer = random.choice(team2_goal_prob)
          team2_goals += 1

        goal_events.append((minutes, scoring_team, scorer))
        time.sleep(0.2) # Simulate real-time match feel (you can remove thisif running fast)

    # Final Live Match Report
    print("\n⚽ Match Highlights ⚽\n")
    for event in goal_events:
      print(f"{event[0]} min: GOAL for {event[1]} by {event[2]}!")

    print("\n" + "="*80)
    print(f" FINAL SCORE: {team1_name} {team1_goals} - {team2_goals}{team2_name}")
    if team1_goals > team2_goals:
      print(f" {team1_name}Wins!")
    elif team2_goals > team1_goals:
      print(f" {team2_name}Wins!")
    else:
      print(" It's a Draw!")
    print("="*80)

    # General goal commentaries
    general_commentaries = [ "What a brilliant strike by {scorer}!", "GOALLLLLLL!{scorer} finds the back of the net!", "An amazing finish from {scorer}!", "Clinical from {scorer}!", "{scorer} smashes it in!", "Fantastic goal by {scorer}!", "Incredible effort by {scorer} —the crowd goes wild!", "{scorer} with a calm and composed finish!", "Unstoppable shot by {scorer}!", "Absolute magic from {scorer}!"]

    # Special commentaries
    equalizer_commentaries = [ "It's all square again thanks to {scorer}!", "Equalizer! {scorer} bringsthe teamslevel!", "What a response! {scorer} ties the game!"]
    go_ahead_commentaries =[ "{scorer} putsthem ahead!", "They take the lead thanks to {scorer}!", "Important goal! {scorer} makes it {team} in front!"]
    last_minute_commentaries = [ "Ohhh what a dramatic late goal by {scorer}!", "In the dying minutes, {scorer} scores!", "Last gasp winner? {scorer} delivers!"]

    def generate_commentary(minutes, team1_goals, team2_goals, scoring_team, scorer):
      if minutes >= 85:
        return random.choice(last_minute_commentaries).format(scorer=scorer)
      elif team1_goals == team2_goals:
        return random.choice(equalizer_commentaries).format(scorer=scorer)
      elif (scoring_team == team1_name and team1_goals > team2_goals + 1) or \
       (scoring_team == team2_name and team2_goals > team1_goals + 1):
        return random.choice(go_ahead_commentaries).format(scorer=scorer, team=scoring_team)
      else:
        return random.choice(general_commentaries).format(scorer=scorer)

    # Inside your loop:
    if chance < 0.1: # ~10% chance that a goal is scored
      scoring_team = random.choices([team1_name, team2_name], weights=[team1_strength, team2_strength])[0]
      if scoring_team == team1_name:
        scorer = random.choice(team1_goal_prob)
        team1_goals += 1
      else:
        scorer = random.choice(team2_goal_prob)
        team2_goals += 1

      goal_events.append((minutes, scoring_team, scorer))
      # Generate and print commentary
      commentary = generate_commentary(minutes, team1_goals, team2_goals, scoring_team, scorer)
      print(f"{minutes} min: {commentary}")

    # Golden Boot Race (Top 5 Scorersin the Match)
    scorer_counter = {}
    for event in goal_events:
      scorer = event[2]
      scorer_counter[scorer] = scorer_counter.get(scorer, 0) + 1

    golden_boot_table = PrettyTable()
    golden_boot_table.field_names = ["Player", "Goals Scored"]
    for player, goals in sorted(scorer_counter.items(), key=lambda x: x[1], reverse=True):
      golden_boot_table.add_row([player, goals])

    print("\n GoldenBoot Race (Match Top Scorers)")
    print(golden_boot_table)

    # Man ofthe Match (Best performer)
    if scorer_counter:
      motm = max(scorer_counter, key=scorer_counter.get)
      print(f"\n Man of the Match: {motm} (Most Goals!)")
    else:
      print("\n Man of the Match: No goals scored! (Hard to pick )")

#market value of a player
# Step 1: Simulate Player Transfer Value (for demonstration)
np.random.seed(42) # For reproducibility
# Simulating transfer value based on goals, assists, and age (thisis a placeholder)
epl_df['Transfer_Value'] = (
epl_df['Goals'] * 1.5 +
epl_df['Assists'] * 1.2 +(100 - epl_df['Age']) * 0.8 + # Age factor: younger players tend to have higher values
np.random.normal(0, 2, len(epl_df)) # Adding some random noise
)
# Define the features for the model
features = ['Goals', 'Assists', 'Age', 'Matches', 'Yellow_Cards', 'Red_Cards']
X = epl_df[features]
y = epl_df['Transfer_Value']
# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Train a Random Forest Regressor to predict transfer value
transfer_model = RandomForestRegressor(n_estimators=100, random_state=42)
transfer_model.fit(X_train, y_train)
# Predict on the test set
y_pred = transfer_model.predict(X_test)
# Evaluate the model
from sklearn.metrics import mean_absolute_error, r2_score
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Transfer Value Prediction Model:")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R-squared: {r2:.2f}")
# Example: Predict transfer value for a player (input manually or choose from dataset)
player_name = input("Enter the player's name to predict their transfer value: ").strip()
# Get player's data
player_data = epl_df[epl_df['Name'] == player_name][features]
if not player_data.empty:
  predicted_transfer_value = transfer_model.predict(player_data)[0]
  print(f"\nPredicted Transfer Value for {player_name}: ${predicted_transfer_value:,.2f}")
else:
  print("Player not found.")
#advanced clustering ofteams
# Step 1: Select relevant features for clustering
team_stats_features = team_stats[['Goals', 'Assists', 'Yellow_Cards', 'Red_Cards','Matches']]
# Step 2: Standardize the data
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
team_stats_scaled = scaler.fit_transform(team_stats_features)
# Step 3: Perform K-Means clustering
from sklearn.cluster import KMeans
# Let's choose 4 clusters as an example (you can experiment with different values)
kmeans = KMeans(n_clusters=4, random_state=42)
team_stats['Cluster'] = kmeans.fit_predict(team_stats_scaled)
# Use two featuresto create a 2D scatter plot (e.g., Goals and Assists)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=team_stats['Goals'], y=team_stats['Assists'], hue=team_stats['Cluster'], palette='Set1', s=100)
plt.title('Clustering of Teams based on Goals and Assists', fontsize=16)
plt.xlabel('Total Goals')
plt.ylabel('Total Assists')
plt.legend(title='Cluster', loc='upper right')
plt.show()
# Perform PCA to reduce dimensionsto 2D
pca = PCA(n_components=2)
principal_components = pca.fit_transform(team_stats_scaled)
# Create a DataFrame with the principal components and cluster labels
pca_df = pd.DataFrame(principal_components, columns=['PC1', 'PC2'])
pca_df['Cluster'] = team_stats['Cluster']
# Plot the clusters based on the first two principal components
plt.figure(figsize=(10, 6))
sns.scatterplot(x='PC1', y='PC2', hue='Cluster', data=pca_df, palette='Set1',s=100)
plt.title('PCA Visualization of Clustering', fontsize=16)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='Cluster', loc='upper right')
plt.show()
# Step 5: Analyze cluster results
# Look at the average stats of each cluster
numeric_columns = team_stats.select_dtypes(include=['float64', 'int64']).columns
cluster_analysis = team_stats.groupby('Cluster')[numeric_columns].mean()
print(cluster_analysis)
# ---------------------- Team Chemistry / Formation Effect ---------------------- # Random chemistry scores for clubs (example simulation)
team_chemistry = {
'ClubA': np.random.randint(70, 100),
'ClubB': np.random.randint(70, 100),
'ClubC': np.random.randint(70, 100)
}
print('\nTeam Chemistry Scores:')
for club, chem in team_chemistry.items():
  print(f"{club}: {chem}%")
# Adding Strength Calculation
def calculate_strength(row):
  base_strength = (
    row['Goals'] * 5 +
    row['Assists'] * 4 +
    row['Yellow_Cards'] +
    row['Red_Cards']
    )
  chemistry_effect = team_chemistry.get(row['Club'], 80) / 100
  return base_strength * chemistry_effect
epl_df['Strength'] = epl_df.apply(calculate_strength, axis=1)
print('\nPlayer Strength (with Team Chemistry Effect):')
print(epl_df[['Name', 'Club', 'Strength']])
# Plot player strength
plt.figure(figsize=(15,7))
sns.barplot(x='Name', y='Strength', data=epl_df.sort_values(by='Strength', ascending=False), palette='viridis')
plt.title('Player Strength considering Team Chemistry')
plt.xticks(rotation=45)
plt.show()
