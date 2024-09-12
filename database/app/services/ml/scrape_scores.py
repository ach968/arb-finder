import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function to extract scores from the HTML
def extract_scores(html):
    soup = BeautifulSoup(html, "html.parser")
    matches = []

    # Find all the match rows
    # match_rows = soup.find_all("ul", class_="match row cf")
    
    match_rows = soup.find_all("ul",class_=lambda x: x and all(c in x for c in ['match', 'row', 'cf']))    
    # print(match_rows)

    for match in match_rows:
        # print(match.prettify())
        date = match.find("span",attrs={"data-match-status":"complete"})
        if not date:
            print(match.prettify())
            break
        # if match.find("span", class_=['timezone-convert-match-week']):
        #     print("Element found")
        #     print(match.find("span", class_=['timezone-convert-match-week']))
        # else:
        #     print("Element not found")
        # date = match.find("span", class_=['`timezone-convert-match-month']).get('data-time')
        # home_team = match.find("a", class_="team home").text.strip()
        # away_team = match.find("a", class_="team away").text.strip()
        # score = match.find("span", class_="bold ft-score").text.strip()

        # matches.append(
        #     {
        #         "Date": date,
        #         "Home Team": home_team,
        #         "Away Team": away_team,
        #         "Score": score,
        #     }
        # )

    return matches


# Function to save the scores to a CSV file
def save_scores_to_csv(matches, file_name="match_scores.csv"):
    df = pd.DataFrame(matches)
    df.to_csv(file_name, index=False)
    print(f"Saved {len(matches)} matches to {file_name}")


def scrape_scores():
    url = "https://footystats.org/england/premier-league/fixtures"

    # Fetch the HTML content from the URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text

        # print(html_content)

        matches = extract_scores(html_content)
    
        save_scores_to_csv(matches)
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
