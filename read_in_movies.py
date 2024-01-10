import pandas as pd

def get_movie_titles():
    df = pd.read_csv('movies_metadata.csv', low_memory=False)
    df = df[["title", "release_date"]]
    df.dropna(inplace=True)
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["year"] = df["release_date"].dt.year
    df = df[(df["year"] > 2000) & (df["year"] < 2021)]
    sample_data = df.sample(5000)
    sample_data["title"].to_csv("our_movie_titles.csv", index=False)


def get_movies_from_omdb(input_file_name:str):
    titles = pd.read_csv(input_file_name)


get_movie_titles()