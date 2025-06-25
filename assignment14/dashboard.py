import streamlit as st
import pandas as pd
import plotly.express as px


df_pp_clean = pd.read_csv("csv/players_pitchers_data_clean.csv")
df_teams_clean = pd.read_csv("csv/teams_data_clean.csv")

st.title("Baseball Stats Dashboard")
st.markdown("Explore top players and team standings in MLB")
#select year and stat type from dropdown
year_selected = st.selectbox("Select a year", df_pp_clean['Year'].sort_values().unique())
stat_selected = st.selectbox("Select a statistic", df_pp_clean['Statistic'].unique())

filtered_pp = df_pp_clean[
    (df_pp_clean['Year'] == year_selected) & 
    (df_pp_clean["Statistic"] == stat_selected)
    ]
# create a bar chart to show top 25 playesr by selected stat
fig = px.bar(
    filtered_pp.sort_values('#', ascending=False),
    x='Name',
    y="#",
    color = 'Team',
    title=f"Top MLB Players by {stat_selected} ({year_selected})"
)
st.plotly_chart(fig)

#Viz №2 Team performance over years

st.header("Team Performance over Time")

#allow user to select multiple teams
teams = sorted(df_teams_clean['Team'].unique())
teams_selected = st.multiselect("Select team(s)", options=teams, default=teams[:2])

#select year range using slider
min_year = int(df_teams_clean['Year'].min())
max_year = int(df_teams_clean['Year'].max())
year_range = st.slider(
    "Select year range", 
    min_value = min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1 #allows to slide
)
#filter team data by selection
filtered_teams = df_teams_clean[
    (df_teams_clean['Team'].isin(teams_selected)) &
    (df_teams_clean['Year'] >= year_range[0]) & 
    (df_teams_clean['Year'] <= year_range[1])
]
#if no data is avail
if filtered_teams.empty:
    st.write("No data available for the selected filters.")
else:
    fig = px.line(
        filtered_teams,
        x='Year',
        y ='W',
        color='Team',
        markers=True,
        title="Team wins over time"
    )
    fig.update_xaxes(type='category') #this solved years showing 2024.5
    st.plotly_chart(fig)
    
 #Viz №3 Win % by League
    
st.header("Average Win % by League")
#let user choose year
year_for_win = st.selectbox('Select a year for Win % by League', df_teams_clean['Year'].sort_values().unique())

avg_league_df = df_teams_clean[df_teams_clean['Year'] == year_for_win].copy()

# Calculate win percentage W/(W+L)
avg_league_df['Win%'] = avg_league_df['W'] / (avg_league_df['W'] + avg_league_df['L'])

# Group by League
league_avg = avg_league_df.groupby("League")['Win%'].mean().reset_index()
#create a bar chart
color_choice = {
    'AL' : 'orange',
    'NL' : 'blue'
}
fig = px.bar(
    league_avg,
    x="League",
    y="Win%",
    title=f"Average Win % by League {year_for_win}",
    text_auto=".2%",
    color="League",
    color_discrete_map = color_choice
)
st.plotly_chart(fig)


    
    