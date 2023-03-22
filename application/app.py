from flask import Flask, render_template, url_for, request, redirect
from db import Articles, create_session, DBSettings

app = Flask(__name__)
DBSettings().setup_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create-article", methods=['POST', 'GET'])
def add_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Articles(title=title, intro=intro, text=text)

        try:
            with create_session() as session:
                session.add(article)
            return redirect("/posts")
        except:
            return "Error creating article"
    else:
        return render_template("add_article.html")


@app.route("/posts")
def posts():
    with create_session() as session:
        articles = session.query(Articles).order_by(Articles.date).all()
        return render_template("posts.html", articles=articles)


@app.route("/get_articles")
def get_articles():
    with create_session() as session:
        articles = session.query(Articles).all()
        articles_data = {}
        for i in articles:
            articles_data[i.id] = {
                "Date": i.date,
                "Intro": i.intro,
                "Article text": i.text
            }
    return articles_data


@app.route("/posts/<int:id>")
def post_detail(id):
    with create_session() as session:
        article = session.query(Articles).get(id)

        return render_template("posts_detail.html", article=article)


@app.route("/posts/<int:id>/delete")
def post_delete(id):
    try:
        with create_session() as session:
            session.query(Articles).filter(Articles.id == id).delete()
        return redirect("/posts")
    except:
        return "Article deletion error"


@app.route("/posts/<int:id>/update", methods=['POST', 'GET'])
def post_update(id):
    if request.method == "POST":
        try:
            with create_session() as session:
                session.query(Articles).filter(Articles.id == id).update({
                    Articles.title: request.form["title"],
                    Articles.intro: request.form["intro"],
                    Articles.text: request.form["text"]
                })
            return redirect("/posts")
        except:
            return "Article deletion error"
    else:
        with create_session() as session:
            article = session.query(Articles).get(id)
            return render_template("post_update.html", article=article)


def testing_app():
    app.config["TESTING"] = True
    return app


if __name__ == "__main__":
    app.run(debug=True)
