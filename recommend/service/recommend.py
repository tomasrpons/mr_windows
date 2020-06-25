import pandas as pd
import os
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def combine_features(row):

    return row['Cast 1'] +" "+row['Director 1']+" "+row["Genre"]+" "+row["Writer 1"]+" "+row["Release Date"]+" "+row["Title"]

def recommend(title):
    try:
        def get_title_from_index(index):
            movie = pd.read_sql_query(""" SELECT DISTINCT "Title", "Url" FROM "movies" WHERE "index" = ? """,con=con, params=[index])
            return movie

        path = os.path.dirname(os.path.abspath(__file__))
        con = sqlite3.connect(path + "\\moviesDB")

        df = pd.read_sql_query("""SELECT DISTINCT  "index", "Cast 1", "Director 1", "Genre", "Rating", "Writer 1", "Release Date", "Title" from "movies" """, con=con)


        features = ["Cast 1", "Director 1", "Genre", "Rating", "Writer 1", "Release Date", "Title"]

        movie = df[df["Title"].str.lower() == title.lower()].values[0]
    
        df = df[df["Genre"] == movie[3]]

        for feature in features:

            df[feature] = df[feature].fillna('')


        data =[]

        for _, row in df.iterrows():
            data.append(combine_features(row))

        df_final = pd.DataFrame({"combined_features":data})

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df_final["combined_features"])
        cosine_sim = cosine_similarity(count_matrix)
        similar_movies =  list(enumerate(cosine_sim[movie[0]]))
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

        titles = []
        urls = []

        for element in sorted_similar_movies[:5]:
            movie = get_title_from_index(element[0])
            titles.append(movie["Title"].values[0])
            urls.append(movie["Url"].values[0])

        final = {"Title": titles, "Url":urls}

        return final
    except:
        return None
