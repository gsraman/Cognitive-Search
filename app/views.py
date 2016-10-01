from app import app
from flask import render_template,request,redirect,url_for,session
import wikipedia
import requests

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search',methods=['POST'])
def search():
    search_query =  request.form['search']
    wiki_page = wikipedia.page(str(search_query))

    res = requests.post('http://node-red-gsraman.au-syd.mybluemix.net/wiki', data=)
    if res.ok:
        print res.json()
    return "Sorry"
