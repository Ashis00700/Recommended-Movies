import pickle
import streamlit as st
import requests

st.set_page_config(
    page_title="Netflix Style Recommender",
    page_icon="🎬",
    layout="wide"
)

# ------------------------
# CUSTOM CSS
# ------------------------
st.markdown("""
<style>
    .stApp{
        background-color:#141414;
        color:white;
    }

    .title{
        font-size:50px;
        font-weight:bold;
        color:#E50914;
        text-align:center;
        margin-bottom:20px;
    }

    .movie-rank{
        font-size:40px;
        font-weight:900;
        color:white;
        text-shadow:4px 4px 8px black;
        text-align:center;
    }

    .movie-title{
        text-align:center;
        font-weight:bold;
        font-size:16px;
        padding-top:10px;
        min-height:60px;
    }

    div[data-baseweb="select"] > div{
        background-color:#222222;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------
# TMDB POSTER
# ------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    response = requests.get(url)

    if response.status_code != 200:
        return ""

    data = response.json()

    poster_path = data.get("poster_path")

    if not poster_path:
        return ""

    return f"https://image.tmdb.org/t/p/w500/{poster_path}"


# ------------------------
# RECOMMENDATION FUNCTION
# ------------------------
def recommend(movie):

    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_names = []
    recommended_posters = []

    for i in distances[1:6]:   # Top 5 only

        movie_id = movies.iloc[i[0]].movie_id

        recommended_names.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_names, recommended_posters


# ------------------------
# LOAD FILES
# ------------------------
movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# ------------------------
# HEADER
# ------------------------
st.markdown(
    '<div class="title">NETFLIX MOVIE RECOMMENDER</div>',
    unsafe_allow_html=True
)

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Choose a Movie",
    movie_list
)

if st.button("Get Recommendations"):

    names, posters = recommend(selected_movie)

    st.markdown(
        f"## Because you watched **{selected_movie}**"
    )

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            st.markdown(
                f'<div class="movie-rank">#{idx+1}</div>',
                unsafe_allow_html=True
            )

            st.image(
                posters[idx],
                use_container_width=True
            )

            st.markdown(
                f'<div class="movie-title">{names[idx]}</div>',
                unsafe_allow_html=True
            )