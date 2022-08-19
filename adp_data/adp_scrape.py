headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def adp_scrape(years):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    
    all_adp_df = pd.DataFrame()

    for year in years:
        year_str = str(year)
        page = f"https://fantasyfootballcalculator.com/adp/ppr/12-team/all/{year_str}"
        page_tree = requests.get(page, headers=headers)
        page_soup = BeautifulSoup(page_tree.content, 'html.parser')

        players = page_soup.find_all("td", {"class": "adp-player-name"})
        adp = page_soup.find_all("td", {"class": "d-none d-sm-table-cell"})

        players_list = []
        adp_list = []

        for i in np.arange(0, len(players)):
            players_list += [players[i].text]
            adp_list += [float(adp[(i*5)].text)]

        adp_df = pd.DataFrame({"Player": players_list, "adp": adp_list, "Year": year})
        all_adp_df = pd.concat([all_adp_df, adp_df], axis=0, ignore_index=True)
        
        all_adp_df["Player"] = all_adp_df['Player'].str.replace('[^\w\s]', '', regex=True)
        
    return all_adp_df