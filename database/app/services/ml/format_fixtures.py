import pandas as pd

path = '/home/acheney/Downloads/bundesliga-2022-UTC.csv'
df = pd.read_csv(path)

# Define the substitutions as a dictionary
substitutions = {
    'Brighton':'Brighton and Hove Albion',
    'Wolves':'Wolverhampton Wanderers',
    'Spurs':'Tottenham Hotspur',
    'Man City':'Manchester City',
    'Man Utd':'Manchester United',
    'Leeds':'Leeds United',
    'Newcastle':'Newcastle United',
    'West Ham':'West Ham United',
    'Norwich':'Norwich City',
    'Sheffield Utd':'Sheffield United',
    'Borussia Mönchengladbach':'Borussia Monchengladbach',
    'FC Augsburg':'Augsburg',
    'Mainz 05':'FSV Mainz 05',
    '1. FC Köln':'FC Koln',
    'SpVgg Greuther Fürth':'Greuther Fürth',
    'Bayer 04 Leverkusen':'Bayer Leverkusen',
    'Hertha BSC':'Hertha Berlin',
    'FC Augsburg':'Augsburg',
    'Hoffenheim':'TSG Hoffenheim',
    'FC Bayern':'Bayern Munich',
}


def format_fixtures():
    # Apply substitutions to the relevant columns
    df['Home Team'] = df['Home Team'].apply(apply_substitutions)
    df['Away Team'] = df['Away Team'].apply(apply_substitutions)

    # Save the modified DataFrame back to a CSV
    df.to_csv(path, index=False)

    print("Substitutions applied and new CSV saved.")

# Function to apply substitutions
def apply_substitutions(text):
    for old, new in substitutions.items():
        text = text.replace(old, new)
    return text

if __name__ == "__main__":
    format_fixtures()