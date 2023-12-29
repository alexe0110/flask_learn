# flask_learn

Веб приложение на фреймворке Flask в котором есть возможность добавлять статьи
просматривать их спиоск, просматривать кажждую отдельно

Работа с БД, создание там запипей, чтение из нее


## Локальный запуск 
Развернуть окружение
Создать БД

Определить энв со строкой подключения к БД
```
BLOG_DB_URL=postgresql://postgres:postgres@0.0.0.0:5432/blog
export BLOG_DB_URL=postgresql://user:mysecretpassword@0.0.0.0:5433/blog
```

Создать виртуальное окружение
```
make init
```

Запустить БД

    docker-compose up -d db

Запуск
```bash
gunicorn --chdir application app:app
```

## Запуск в контейнере 

```bash
make run
```

## Миграции

Нужно чтобы в `migrations/env.py:9` была указана актуальная БД
Сравнить текущее состояние в бд и наши модели - сделать ревизию
```
.venv/bin/alembic revision --autogenerate -m "DB Creation"
```
После этого в `migrations/versions` появятся миграции

Чтобы запустить миграции выполнить команду указав хэш
```
alembic upgrade 08fbdbfff985
```

### 

# Flask

`@app.route('/')`  для отслеживания урл адреса, создает связь между URL-адресом, заданным как аргумент, и функцией

`@app.route("/user/<string:name>/<int:id>")` переменный урл

```python
@app.route("/user/<string:name>/<int:id>")
def user(name, id):
    return "Привет,  " + name + " " + str(id)
```

`@app.route("/create-article", methods=['POST', 'GET'])` в аргументе methods указываются методы которые можем принимать

Работа с POST запросом, если приходит пост то пишем в базу

```python
@app.route("/create-article", methods=['POST', 'GET'])
def add_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Articles(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/")
        except:
            return "Случилась ошибка"
    else:
        return render_template("add_article.html")
```

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    return "Hello World"

@app.route('/about')
def about():
    return "About page"

if __name__ == "__main__":
    app.run()
```

### **Шаблоны**

Для отделения функциональной части сайта от визуальной были созданы различные шаблонизаторы, что выполняют роль отделения логической части сайта от визуальной. В библиотеке Flask таким шаблонизатором является Jinja

Функция `render_template` позволяет подключить html шаблоны, выводить большие HTML-шаблоны, напичканые кодом из шаблонизатора Jinja. Пример `return render_template("index.html")`

Папка `templates` содержит html шаблоны 

`{% block <name> %}{% endblock %}`  переменная name в html коде

`{% extends "ПУТЬ К HTML ФАЙЛУ" %}` наследуем от html файла к которому указали путь

Для подключения стилей

Папка `static` хранит статические файлы (css, js, jpg и тд.)

В основном `base.html` шаблоне можно прописать базовую структуру для всех HTML файлов и описать переменные фрагменты:

```html
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block body %}{% endblock %}
</body>
</html>
```

Внутрь базового шаблона можно встроить HTML блоки и заменить содержимое block content. Чтобы это сделать создаем новый HTML файл и прописываем наследование структуры из базового файла:

```html
{% extends 'base.html'%}

{% block title %}Главная страница{% endblock %}

{% block body %}
<h1>Осноавная страница!</h1>
{% endblock %}
```

### **Базы данных**

SQLAlchemy - библиотека для работы с SQL 

`app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"` подключение к базе данных blog.db

В основном файле можно записать как один, так и несколько классов, каждый из которых будет выполнять роль определенной таблицы в базе данных.

Для **описания полей** внутри таблицы необходимо прописать переменные внутри классов. В каждую переменную устанавливается определенное значение, что соответсвует типу устанавливаемых данных в поле таблицы и обязательность/дефолтное значение.

Подробднее [https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/)

При получении объекта из базы данных всегда возвращается ID записи, поэтому лучше в классе модели дописывать магический метод «__repr__». В нём можно указать какое значение будет возвращается при получении объекта из БД.

**Получение данных из БД**

`model = User.query.first()`  получить первую запись
`model = User.query.all()` получить все записи из таблицы

Чтобы передать данные в HTML шаблон, укажите второй параметр в функции `render_template()`:

```python
model = User.query.all() # Получение всех записей
# Вызов шаблона и передача в него данных
return render_template('html-template.html', parametr_name=model)
```

```python
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
db = SQLAlchemy(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

		def __repr__(self):
			return '<Article %r>' % self.id
```

Описание обработчика в app.py

```python
@app.route("/posts")
def posts():
    articles = Articles.query.order_by(Articles.date).all()
    return render_template("posts.html", articles=articles)
```

Построение страницы 

```html
{% extends 'base.html'%}

{% block title %}
Все статьи на сайте
{% endblock %}

{% block body %}
<div class="container">
    <h1>Статьи</h1>
    {% for el in articles %}
    <div class="alert alert-info">
        <h2>{{ el.title }}</h2>
        <p>{{ el.intro }}</p>
        <p><b>{{ el.date.date() }}</b></p>
        <a class="btn btn-info" href="/posts/{{el.id}}">Детали</a>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

На хероку, чтобы с poetry
```bash
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
git push...
```