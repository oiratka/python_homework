import pandas as pd


def clean_data():
    #Load scraped data
    df_pp = pd.read_csv("csv/players_pitchers_data.csv")
    df_teams = pd.read_csv("csv/teams_data.csv")

    print(f"Total rows before cleaning players&pitchers: {len(df_pp)}")

    #Clean player&pitcher data
    df_pp_clean = df_pp[df_pp["Statistic"] != "Statistic"].copy() #removes duplicated header rows
    df_pp_clean = df_pp_clean[~df_pp_clean['Name'].isin(['To Be Determined'])]# drop rows where Name is to be determined (placeholder)
    df_pp_clean = df_pp_clean[~df_pp_clean['Team'].isin(['--'])]# drop rows where Team has '--' (placeholder)

    print(f"Rows after dropping bad data p&p: {len(df_pp_clean)}")
    # check for duplicates just in case
    print(f"Duplicates before dropping: {df_pp_clean.duplicated().sum()}")
    df_pp_clean = df_pp_clean.drop_duplicates()
    print(f"Duplicates after dropping: {df_pp_clean.duplicated().sum()}")
    
    #convert data to appropriate numerics types
    df_pp_clean['Year'] = pd.to_numeric(df_pp_clean['Year'], errors = 'coerce').astype('Int64')
    df_pp_clean['#'] = pd.to_numeric(df_pp_clean['#'], errors = 'coerce')

    #Clean TEAMS data
    print(f"Total rows before cleaning teams standing: {len(df_teams)}")

    #remove rows without actual data
    df_teams_clean = df_teams[~df_teams['Team'].str.contains("Standings", na=False)].copy()
    df_teams_clean['GB'] = df_teams_clean['GB'].replace('-',0) #replace non0numeric value '-'

    #convert Win/Loss/Tie/GB to numeric values
    for col in ['W', 'L', 'T', 'GB']:
        df_teams_clean[col] = pd.to_numeric(df_teams_clean[col], errors='coerce').round().astype('Int64')
    #convert year and wp colums
    df_teams_clean['Year'] = pd.to_numeric(df_teams_clean['Year'], errors='coerce').astype('Int64')
    df_teams_clean['WP'] = pd.to_numeric(df_teams_clean['WP'], errors='coerce').round(2)
    
    #drop rows missing essential fields
    df_teams_clean = df_teams_clean.dropna(subset=['Year', 'Team'])
    print(df_teams_clean[['Team', 'W', 'L', 'T', 'GB']].head(10).to_string(index=False))
    
    #save clean data
    df_pp_clean.to_csv("csv/players_pitchers_data_clean.csv", index=False)
    df_teams_clean.to_csv("csv/teams_data_clean.csv", index=False)

    return df_pp_clean, df_teams_clean

def main():
    clean_data()
    

if __name__ == '__main__':
    main()


