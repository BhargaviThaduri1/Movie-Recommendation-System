import pickle
import requests
from flask import Flask,render_template,redirect,url_for,request

app = Flask(__name__)

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    tagline = data['tagline']
    url = data['homepage']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path,tagline,url


def Recommend_Funtion(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    urls = []
    taglines=[]
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        full_path,tag,url = fetch_poster(movie_id)
        recommended_movie_posters.append(full_path)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        taglines.append(tag);
        urls.append(url)

    for u in urls:
        if u:
            print(u)

    return recommended_movie_names,recommended_movie_posters,taglines,urls


@app.route('/')
def home():
    return render_template('home.html',movies=movie_list)


@app.route('/recommend',methods=['POST'])
def recommend():
    if request.method=='POST':
        selected_movie = request.form['movie']
        return redirect(url_for('getMovie',selected_movie=selected_movie))


@app.route('/getMovie/<selected_movie>')
def getMovie(selected_movie):
    recommended_movie_names, recommended_movie_posters,taglines,urls = Recommend_Funtion(selected_movie)
    return render_template('movies.html',selected_movie=selected_movie,recommended_movie_names= recommended_movie_names,recommended_movie_posters=recommended_movie_posters,taglines=taglines,urls=urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

