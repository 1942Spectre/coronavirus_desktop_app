import pandas as pd
import json
import requests


def get_df():
    
    response = requests.get("https://api.covid19api.com/summary")
    parsed_json = json.loads(response.text)
    
    country_data = parsed_json["Countries"]
    df = pd.DataFrame(country_data)
    
    return df


def get_country(country, df = get_df() ):
    return df[df.Country == country]

