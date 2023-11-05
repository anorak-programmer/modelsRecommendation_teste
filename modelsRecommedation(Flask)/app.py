import pickle
import pandas as pd
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Carregue a lista de filmes uma vez ao iniciar o aplicativo
with open('models/filmes_dataframe.pkl', 'rb') as file:
    filmesData = pickle.load(file)

#Não saberei explicar em detalhes, mas, em resumo, usa uma API que busca a logo dos filmes
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = filmesData[filmesData['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = filmesData.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(filmesData.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

@app.route("/", methods=["GET", "POST"])
def index():
    movie_list = filmesData['title'].values

    if request.method == "POST":
        selected_movie = request.form["movie"]
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    else:
        selected_movie = ""
        recommended_movie_names = []
        recommended_movie_posters = []

    return render_template("index.html", movie_list=movie_list, selected_movie=selected_movie, recommended_movie_names=recommended_movie_names, recommended_movie_posters=recommended_movie_posters)

if __name__ == "__main__":
    # Carregar o modelo em um novo código
    with open('models/modelo.pkl', 'rb') as file:
        similarity = pickle.load(file)

    app.run(debug=True)
