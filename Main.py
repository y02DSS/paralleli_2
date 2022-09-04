# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import datetime
import os
#import Email
#from werkzeug.utils import secure_filename

UPLOAD_FOLDER_PICTURE = 'static/picture/picture_user/'
UPLOAD_FOLDER_BOOK = 'static/books/book_user/'
ALLOWED_EXTENSIONS_PICTURE = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_BOOK = set(['pdf', 'doc', 'docx'])


app = Flask(__name__, static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Baze.db'
app.config['UPLOAD_FOLDER_PICTURE'] = UPLOAD_FOLDER_PICTURE
app.config['UPLOAD_FOLDER_BOOK'] = UPLOAD_FOLDER_BOOK


# run_with_ngrok(app)
db = SQLAlchemy(app)


class Photos(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Photo = db.Column(db.String())
    Photos_min = db.Column(db.String())
    Caption = db.Column(db.String())


class News(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Photo = db.Column(db.String())
    Name_photo = db.Column(db.String())
    Coment = db.Column(db.String())


class Author_info(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String())
    Photo = db.Column(db.String())
    Date = db.Column(db.String())


class GG_user(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name_book = db.Column(db.String(), unique=True)
    Name = db.Column(db.String(200))
    Email = db.Column(db.String())
    Coment = db.Column(db.String())
    Date = db.Column(db.Integer())
    Photo = db.Column(db.String())
    Photo_2 = db.Column(db.String())
    Photo_3 = db.Column(db.String())
    Type = db.Column(db.String())
    Link = db.Column(db.String())
    Link_2 = db.Column(db.String())
    Show = db.Column(db.Integer())

class GG(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200))
    Name_book = db.Column(db.String(), unique=True)
    Coment = db.Column(db.String())
    Date = db.Column(db.Integer())
    Photo = db.Column(db.String())
    Photo_2 = db.Column(db.String())
    Photo_3 = db.Column(db.String())
    Type = db.Column(db.String())
    Link = db.Column(db.String())
    Link_2 = db.Column(db.String())





@app.route('/')
def main():
    return render_template('main.html', main="active", title="Главная")


@app.route('/event')
def event():
    return render_template('event.html',  event="active", title="События")


@app.route('/our_library')
def our_library():
    defaultValForFilter = "Выбрать сортировку:"

    is_filter_on_date = defaultValForFilter
    is_filter_on_alphabet = defaultValForFilter

    tasks = []
    tasks_user = GG_user.query.filter_by(Show=1)

    args = request.args

    if "is_filter_on_date" in args:
        is_filter_on_date = args["is_filter_on_date"]

    if "is_filter_on_alphabet" in args:
        is_filter_on_alphabet = args["is_filter_on_alphabet"]

    if is_filter_on_date == 'По возрастанию':
        tasks = GG.query.order_by(GG.Date).all()
    elif is_filter_on_date == 'По убыванию':
        tasks = GG.query.order_by(GG.Date.desc()).all()
    elif is_filter_on_alphabet == 'От А ... До Я':
        tasks = GG.query.order_by(GG.Name_book).all()
    elif is_filter_on_alphabet == 'От Я ... До А':
        tasks = GG.query.order_by(GG.Name_book.desc()).all()
    else:
        tasks = GG.query.all()

    return render_template(
        'our_library.html',
        tasks=tasks,
        tasks_user=tasks_user,
        is_filter_on_date=is_filter_on_date,
        is_filter_on_alphabet=is_filter_on_alphabet,
        our_library="active",
        title="Наша библиотека"
    )


# @app.route('/our_library/filter', methods=['POST'])
# def filter():

#     return render_template('our_library.html', tasks=tasks, our_library="active", title = "Наша библиотека")

@app.route('/our_library/filter', methods=['POST'])
def filter():
    is_filter_on_alphabet = ""
    is_filter_on_date = ""

    if ("sort_sort" in request.form):
        if str(request.form['sort_sort']) == 'По возрастанию':
            is_filter_on_date = str(request.form['sort_sort'])
        elif str(request.form['sort_sort']) == 'По убыванию':
            is_filter_on_date = str(request.form['sort_sort'])
        else:
            is_filter_on_date = ""

    if ("sort_name" in request.form):
        if str(request.form['sort_name']) == 'От А ... До Я':
            is_filter_on_alphabet = str(request.form['sort_name'])
        elif str(request.form['sort_name']) == 'От Я ... До А':
            is_filter_on_alphabet = str(request.form['sort_name'])
        else:
            is_filter_on_alphabet = ""

    return (lambda:
            redirect("/our_library?" + "is_filter_on_alphabet=" +
                     str(is_filter_on_alphabet))
            if len(is_filter_on_alphabet) != 0
            else
            redirect("/our_library?" + "is_filter_on_date=" +
                     str(is_filter_on_date))
            if len(is_filter_on_date) != 0
            else redirect("/our_library"))()


@app.route('/gallery')
def gallery():
    tasks = Photos.query.all()
    return render_template('gallery.html', tasks=tasks, gallery="active", title="Галерея")


@app.route('/projects')
def projects():
    return render_template('projects.html', projects="active", title="Проекты")


@app.route('/authors_opinion')
def contacts1():
    Members = ['Асенова К.Л.', 'Бартфельд Б.Н.', 'Белов И.Л.', 'Глушкин О.Б.',
                'Карпенко В.М.', 'Никитин М.А.', 'Нисневич Б.А.', 'Погоняев С.В.',
                'Попов А. В.', 'Соловьёва (Ковалева) В.Б.', 'Татарикова-Карпенко Ал.А.', 'Гетман С. (Clandestinus)',
                'Батрушевич В.', 'Ковтун А.', 'Моргулева И.', 'Альмухаметова М.В.',
                'Малай Р.В.', 'Силецкая И.С.']
    Members_honorary = ['Голубев В.Л.', 'Горбачева (Стебихова) Н.Н.', 'Зорин В.А.', 'Симкин С.Х',
                'Юшко Г.А.']
    return render_template('authors_opinion.html', Members=Members, Members_honorary=Members_honorary, authors_opinion="active", title="Персонали ПЕН-центра")


@app.route('/frequent_opinion')
def frequent_opinion():
    author = request.args.get('author')
    if author:
        tasks = Author_info.query.all()
        author_Baze = Author_info.query.filter_by(Name=str(author)[:-7]).first()
        author_text = open('static/text_authors/' + str(author)[:-7] + ".txt", encoding="utf-8")
        author_info = author_text.read().replace('\n', '<br>').split('$!$')
        return render_template('frequent_opinion_author.html', title=author, author_date=author_Baze.Date, author_photo=author_Baze.Photo, author_info=author_info[0], author_books=author_info[1], author_name=str(author)[:-7], tasks = tasks, encoding='latin-1')
    else:
        tasks = Author_info.query.all()
        return render_template('frequent_opinion.html', frequent_opinion="active",tasks = tasks, title="Авторское слово")
    

@app.route('/young_voice')
def young_voice():
    return render_template('young_voice.html', young_voice="active", title="Молодые голоса")

@app.route('/admin')
def admin():
    tasks_user = GG_user.query.all()
    show = GG_user.Show
    return render_template('admin.html', tasks_user=tasks_user,  title="Частное мнение")

@app.route('/book/<Link>')
def book(Link):
    return send_file('Произведения/'+Link)


@app.route('/book_user/<Link_user>')
def book_user(Link_user):
    return send_file('Произведения/'+Link_user)


@app.route('/book_user_true/<Link_user>')
def book_user_true(Link_user):
    user=GG_user.query.filter_by(ID=int(Link_user)).first()
    user.Show = 1
    db.session.commit()
    mailr = user.Email
    Email.all1(mailr, wordr='принято')
    return redirect(url_for('admin'))

@app.route('/book_user_false/<Link_user>')
def book_user_false(Link_user):
    user = GG_user.query.filter_by(ID=int(Link_user)).first()
    mailr = user.Email
    Email.all1(mailr, wordr='не принято')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

def allowed_file_picture(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_PICTURE

def allowed_file_book(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS_BOOK


@app.route('/create_task', methods=['POST'])
def create_task():
    new_task = GG(Name_book=request.form['Name_book'], Name=request.form['Name'], Coment=request.form['Coment'],
                  Date='Date', Photo=request.form['Photo'], Photo_2=request.form['Photo_2'], Photo_3=request.form['Photo_3'],
                  Type=request.form['Type'], Link=request.form['Link'], Link_2=request.form['Link_2'])
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('our_library'))


@app.route('/create_task_users', methods=['GET', 'POST'])
def create_task_users():
    filename_book = 'Не добавленно'
    filename_photo = 'Не добавленно'
    if request.method == 'POST':
        file_P = request.files['Photo']
        if file_P and allowed_file_picture(file_P.filename):
            filename_photo = secure_filename(file_P.filename)
            file_P.save(os.path.join(app.config['UPLOAD_FOLDER_PICTURE'], filename_photo))
        file_B = request.files['Link']
        if file_B and allowed_file_book(file_B.filename):
            filename_book = secure_filename(file_B.filename)
            file_B.save(os.path.join(app.config['UPLOAD_FOLDER_BOOK'], filename_book))
    new_task = GG_user(Name_book=request.form['Name_book'], Name=request.form['Name'], Email=request.form['Email'], Coment=request.form['Coment'],
                       Date='Date', Photo=filename_photo, Photo_2='Photo_2', Photo_3='Photo_3',
                       Type=request.form['Type'], Link=filename_book, Link_2='Не добавленно', Show=0)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('our_library'))


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
    # app.run()
