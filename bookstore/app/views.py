from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
import mysql.connector as sql


fulln = ''
email = ''
paswrd = ''
utype = 0

booktitle = ''
auther = ''
department = ''
page = 0
bookId = 0

con = sql.connect(host="localhost", user="root",
                  passwd="Huraira786@", database='bookstore')
dbCursor = con.cursor()

# Create your views here.


# Login page
def login(request):
    global email, paswrd
    if request.method == "POST":
        d = request.POST
        for key, value in d.items():
            if key == "email":
                email = value
            if key == "password":
                paswrd = value
        query = "select * from user where email='{}' and password='{}'".format(
            email, paswrd)
        dbCursor.execute(query)
        data = tuple(dbCursor.fetchall())
        if data == ():
            return render(request, 'error.html')
        else:
            # render(request, "booklist.html")
            # request.session.set_expiry(84000)
            request.session['userType'] = ''
            request.session['userType'] = "admin" if data[0][4] == "1" else "student"
            return HttpResponseRedirect('../booklist')

    return render(request, 'login_page.html')


# Signup page
def signup(request):
    if request.session['userType'] != "admin":
        return HttpResponseRedirect('../booklist')
    global fulln, email, paswrd, utype
    if request.method == "POST":
        post_data = request.POST
        for key, value in post_data.items():
            if key == "full_name":
                fulln = value
            if key == "email":
                email = value
            if key == "password":
                paswrd = value
            if key == "type":
                utype = value
        query = "insert into user(fullname,email,password,user_type) Values('{}','{}','{}',{})".format(
            fulln, email, paswrd, utype)
        dbCursor.execute(query)
        con.commit()
    return render(request, 'signup_page.html')


# Booklist
def booklist(request):
    if request.session['userType'] == "student":
        is_student = 1
    else:
        is_student = 0
    dbCursor.execute('select * from books')
    data = dbCursor.fetchall()
    print(list(data))
    return render(request, 'booklist.html', {'bookList': data, 'student': is_student})


# DeleteBook
def deleteBook(request, id):
    print(id)
    dbCursor.execute('DELETE from books where id={}'.format(id))
    con.commit()
    return HttpResponseRedirect('../booklist')


# AddBooks
def addbooks(request):
    if request.session['userType'] != "admin":
        return HttpResponseRedirect('../booklist')
    global booktitle, auther, department, page
    if request.method == "POST":
        post_data = request.POST
        for key, value in post_data.items():
            if key == "book_title":
                booktitle = value
            if key == "auther":
                auther = value
            if key == "department":
                department = value
            if key == "pages":
                page = value
        query = "insert into books(book_title,auther_name,department,page_count) Values('{}','{}','{}',{})".format(
                booktitle, auther, department, page)
        dbCursor.execute(query)
        con.commit()
        return HttpResponseRedirect('../booklist')
    return render(request, 'addbooks.html', {'message': "test"})


# updatebook


def updatebookdb(request, id):
    global booktitle, auther, department, page
    if request.method == "POST":
        post_data = request.POST
        for key, value in post_data.items():
            if key == "book_title":
                booktitle = value
            if key == "auther":
                auther = value
            if key == "department":
                department = value
            if key == "pages":
                page = value
            query = "update books set book_title='{}',auther_name='{}',department='{}',page_count={} where id={}".format(
                booktitle, auther, department, page, id)
            dbCursor.execute(query)
            con.commit()
    return HttpResponseRedirect('../booklist')


def updatebook(request, id):
    if request.session['userType'] != "admin":
        return HttpResponseRedirect('../booklist')
    query = "select * from books where id={}".format(id)
    bookId = id
    dbCursor.execute(query)
    data = dbCursor.fetchall()
    return render(request, 'updatebook.html', {'bookdata': data})
