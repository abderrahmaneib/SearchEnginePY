#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from queryIndex_tfidf import QueryIndex
app = Flask(__name__)

q=QueryIndex()
@app.route("/search", methods=['POST', 'GET'])
def queries():
    query = request.args.get('query')
    result = q.queryIndex(query)
    #print result
    encoded = []
    try:
    	encoded = [unicode(i,encoding='UTF-8') for i in result]
    	#print encoded
    	return render_template('list.html', result=encoded, query=query, isnull="no")
    except:
    	return render_template('list.html', result=encoded, query=query, isnull="yes")


@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()

'''
<h2>Titre {{result.index(item)}}</h2>
								<p>{{ item }}</p>
								'''