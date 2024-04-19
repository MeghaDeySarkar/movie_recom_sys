import streamlit as st
import pickle
import pandas as pd
import requests
import bz2
import _pickle as cPickle

def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b2cb03809d85817a4c3a457af92cff5f&language=en-US'.format(movie_id))
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters
    
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open('similarity.pkl','rb'))
similarity = decompress_pickle('similarity1.pbz2')

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search for a movie', movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], use_column_width=True)
        st.write(names[0])
        
    with col2:
        st.image(posters[1], use_column_width=True)
        st.write(names[1])

    with col3:
        st.image(posters[2], use_column_width=True)
        st.write(names[2])
        
    with col4:
        st.image(posters[3], use_column_width=True)
        st.write(names[3])
        
    with col5:
        st.image(posters[4], use_column_width=True)
        st.write(names[4])

# Custom CSS to style the page
st.markdown(
    """
    <style>
    .st-bw {
        background-color: #f0f2f6;
    }
    .css-1j7mbtc {
        font-family: Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
