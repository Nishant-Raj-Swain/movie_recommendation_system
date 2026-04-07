import pickle
import streamlit as st
import requests
import time
import warnings
import os
import gdown   # ✅ added

warnings.filterwarnings("ignore")  # ✅ hide warnings


# ✅ ONLY similarity.pkl from Google Drive
SIMILARITY_URL = "https://drive.google.com/file/d/14_al_FKw5r8nnn98-0_3GPdWw3uZKGIr/view?usp=sharing"

if not os.path.exists("similarity.pkl"):
    gdown.download(SIMILARITY_URL, "similarity.pkl", quiet=False)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=91e50bd6f2b317f3a5827f9cd407311d&language=en-US".format(movie_id)

    for _ in range(3):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')

                if poster_path and poster_path != "None":
                    return "https://image.tmdb.org/t/p/w500" + poster_path

        except:
            pass

    return "https://via.placeholder.com/500x750?text=Not+Available"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        time.sleep(0.3)
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header('🎬 Movie Recommender System')

# ❗ movie_list.pkl stays LOCAL (no change)
movies = pickle.load(open('movie_list.pkl','rb'))

# ✅ similarity.pkl downloaded from Drive
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0] + "?v=1", use_container_width=True)

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1] + "?v=1", use_container_width=True)

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2] + "?v=1", use_container_width=True)

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3] + "?v=1", use_container_width=True)

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4] + "?v=1", use_container_width=True)
