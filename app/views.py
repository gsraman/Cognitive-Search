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
    i = 1;
    j = 1;
    payload = { "entities1": [] , "relations" : []}
    search_query =  request.form['search']
    wiki_page = wikipedia.page(str(search_query))
    wiki_content = wiki_page.content.encode('utf-8')
    res = requests.post('http://node-red-gsraman.au-syd.mybluemix.net/wiki', data=wiki_content)
    if res.ok:
        result = res.json()
        if float(result['taxonomy'][0]['score']) > 0.3:
            taxonomy = str(result['taxonomy'][0]['label']).split("/")
            taxonomy.remove('')
            for element in taxonomy:
                payload["entities1"].append({"key": i , "value1" : element})
                i+=1
                if int(taxonomy.index(element)) != 0:
                    payload["relations"].append({"key1": taxonomy.index(element)+1 , "key2": int(taxonomy.index(element)), "relation" : "belongs to" })
            payload["entities1"].append({"key": i , "value1" : search_query })
            payload["relations"].append({"key1": i , "key2": i-1, "relation" : "belongs to" })
        try:
            payload["entities1"].append({"key": i+1 , "value1" : result["concept"][0]["website"] })
            payload["relations"].append({"key1": i, "key2": i+1 , "relation" : "found at" })
        except:
            print "No web"
        try:
            payload["entities1"].append({"key": i+2 , "value1" : result["concept"][0]["dbpedia"] })
            payload["relations"].append({"key1": i, "key2": i+2 , "relation" : "found at" })
        except:
            print "No db"
        try:
            payload["entities1"].append({"key": i+3 , "value1" : result["concept"][0]["freebase"] })
            payload["relations"].append({"key1": i, "key2": i+3 , "relation" : "found at" })
        except:
            print "no freebase"
        try:
            payload["entities1"].append({"key": i+4 , "value1" : result["concept"][0]["yago"] })
            payload["relations"].append({"key1": i, "key2": i+4 , "relation" : "found at" })
        except:
            return render_template('concept-map.html',payload=payload)
    return render_template('concept-map.html',payload=payload)
    return "Sorry couldn't find the term"
