import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# ── Load data ──────────────────────────────────────
FOLDER = r"C:\Users\xuzhe\Desktop\IS1520"
games   = pd.read_csv(f"{FOLDER}\\games.csv")
teams   = pd.read_csv(f"{FOLDER}\\teams.csv")

# ── Clean & prep ───────────────────────────────────
games['GAME_DATE_EST'] = pd.to_datetime(games['GAME_DATE_EST'])
games['SEASON'] = games['SEASON'].astype(int)

# Only use recent seasons (2015-2022)
games = games[games['SEASON'].between(2015, 2022)]

# Win flag for home team
games['HOME_WIN'] = (games['HOME_TEAM_WINS'] == 1).astype(int)

# Merge team abbreviation for home team
teams_abbr = teams[['TEAM_ID', 'ABBREVIATION', 'NICKNAME']].copy()
games = games.merge(teams_abbr, left_on='HOME_TEAM_ID', right_on='TEAM_ID', how='left')

# ── Aggregations ───────────────────────────────────

# 1. Average home points scored per team (last 3 seasons)
recent = games[games['SEASON'] >= 2020]
team_pts = recent.groupby('ABBREVIATION').agg(
    AVG_PTS=('PTS_home', 'mean'),
    WINS=('HOME_WIN', 'sum'),
    GAMES=('HOME_WIN', 'count')
).reset_index()
team_pts['WIN_PCT'] = team_pts['WINS'] / team_pts['GAMES'] * 100
team_pts = team_pts.sort_values('AVG_PTS', ascending=False).head(15)

# 2. League-wide average points per season (scoring trend)
season_pts = games.groupby('SEASON').agg(
    AVG_HOME=('PTS_home', 'mean'),
    AVG_AWAY=('PTS_away', 'mean')
).reset_index()

# 3. Home vs Away win rate per season
season_home_win = games.groupby('SEASON')['HOME_WIN'].mean().reset_index()
season_home_win.columns = ['SEASON', 'HOME_WIN_RATE']

# ── Plot ───────────────────────────────────────────
fig = plt.figure(figsize=(16, 13))
fig.patch.set_facecolor('#F7F9FC')
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# Color palette
C1 = '#1D428A'  # NBA blue
C2 = '#C8102E'  # NBA red
C3 = '#FDB927'  # NBA gold

# ── Subplot 1: Avg points per team (top 15) ────────
ax1 = fig.add_subplot(gs[0, :])
ax1.set_facecolor('white')

colors = [C1 if i < 5 else ('#4472C4' if i < 10 else '#7BAFD4') for i in range(len(team_pts))]
bars = ax1.bar(team_pts['ABBREVIATION'], team_pts['AVG_PTS'], color=colors, edgecolor='white', width=0.7)

# Add value labels
for bar in bars:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=8.5, color='#333333')

ax1.set_title('Average Home Points Scored — Top 15 NBA Teams (2020–2022)', fontsize=14, fontweight='bold', pad=10)
ax1.set_xlabel('Team', fontsize=11)
ax1.set_ylabel('Avg Points per Game', fontsize=11)
ax1.set_ylim(100, 120)
ax1.spines[['top', 'right']].set_visible(False)
ax1.grid(axis='y', alpha=0.3)
ax1.tick_params(axis='x', labelsize=9)

# ── Subplot 2: Scoring trend by season ─────────────
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_facecolor('white')

ax2.plot(season_pts['SEASON'], season_pts['AVG_HOME'], color=C1, linewidth=2.5,
         marker='o', markersize=6, label='Home Team')
ax2.plot(season_pts['SEASON'], season_pts['AVG_AWAY'], color=C2, linewidth=2.5,
         marker='s', markersize=6, label='Away Team')
ax2.fill_between(season_pts['SEASON'], season_pts['AVG_HOME'], season_pts['AVG_AWAY'],
                 alpha=0.12, color=C3)

ax2.set_title('NBA Scoring Trend by Season', fontsize=13, fontweight='bold', pad=10)
ax2.set_xlabel('Season', fontsize=10)
ax2.set_ylabel('Avg Points per Game', fontsize=10)
ax2.legend(fontsize=9)
ax2.spines[['top', 'right']].set_visible(False)
ax2.grid(alpha=0.3)
ax2.tick_params(axis='x', labelsize=9)

# ── Subplot 3: Home win rate by season ─────────────
ax3 = fig.add_subplot(gs[1, 1])
ax3.set_facecolor('white')

bar_colors = [C1 if v >= 0.6 else C2 for v in season_home_win['HOME_WIN_RATE']]
ax3.bar(season_home_win['SEASON'].astype(str), season_home_win['HOME_WIN_RATE'] * 100,
        color=bar_colors, edgecolor='white', width=0.6)
ax3.axhline(50, color='gray', linestyle='--', linewidth=1, alpha=0.7, label='50% line')

for i, (_, row) in enumerate(season_home_win.iterrows()):
    ax3.text(i, row['HOME_WIN_RATE'] * 100 + 0.5,
             f"{row['HOME_WIN_RATE']*100:.1f}%", ha='center', va='bottom', fontsize=9)

ax3.set_title('Home Court Advantage — Win Rate by Season', fontsize=13, fontweight='bold', pad=10)
ax3.set_xlabel('Season', fontsize=10)
ax3.set_ylabel('Home Team Win Rate (%)', fontsize=10)
ax3.set_ylim(0, 75)
ax3.spines[['top', 'right']].set_visible(False)
ax3.grid(axis='y', alpha=0.3)
ax3.legend(fontsize=9)

# ── Main title ─────────────────────────────────────
fig.suptitle('NBA Team Performance Analysis (2015–2022)',
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig(f"{FOLDER}\\nba_figure.png", dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()
print("✅ 图片已保存！")
