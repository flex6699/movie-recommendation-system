import pandas as pd

import streamlit as st
import pickle
import requests
from sklearn.metrics.pairwise import cosine_similarity

import os

streamlit_api_key = os.environ.get('STREAMLIT_API_KEY')
def fetch_poster(id):
    response=requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key={streamlit_api_key}&language=en-US")
    data=response.json()
    print(data["poster_path"])
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]
def recommend(title):
    idx=movies2idx[title];
    if type(idx)==pd.Series:
        idx=idx.iloc[0]
    query=similarity[idx];
    scores=cosine_similarity(query,similarity)
    scores=scores.flatten()
    recommended_idx=(-scores).argsort()[1:6]
    recommended_movies=[]
    recommended_posters=[]

    for i in recommended_idx:
        recommended_posters.append(fetch_poster(movies_list["id"].iloc[i]));
        recommended_movies.append(movies_list["original_title"].iloc[i]);
    return recommended_movies,recommended_posters

st.title("Movie Recommender System")
movies_list=pickle.load(open("movies.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))
movies_list=pd.DataFrame(movies_list)
movies2idx=pd.Series(movies_list.index,index=movies_list["original_title"])


select_movie_name=st.selectbox("Type Movie Name",movies_list["original_title"].values)
if st.button("Recommend"):
    names,posters=recommend(select_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
