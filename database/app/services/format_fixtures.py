import pandas as pd
import re

path = '/home/acheney/Downloads/epl-2024-UTC.csv'
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
    'Leicester':'Leicester City',
    "Nott'm Forest": "Nottingham Forest",
    'Ipswich':'Ipswich Town',
    
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
        # Use regex to ensure substitution is applied only once
        pattern = re.compile(r'\b' + re.escape(old) + r'\b')
        text = pattern.sub(new, text)
    return text

if __name__ == "__main__":
    format_fixtures()