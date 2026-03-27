from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load your data
new = pickle.load(open('movies_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Your function (modified to return list instead of print)
def recommendationsystem(movie):
    index = new[new['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    for i in distance[1:6]:
        recommended_movies.append(new.iloc[i[0]].title)

    return recommended_movies


@app.route('/', methods=['GET', 'POST'])
def home():
    movie_list = new['title'].values

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommendations = recommendationsystem(selected_movie)
        return render_template('index.html', movies=movie_list, recs=recommendations)

    return render_template('index.html', movies=movie_list)


if __name__ == '__main__':
    app.run(debug=True)