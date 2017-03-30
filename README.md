# SearchEnginePY
This project does:
Collect Wikipedia Articles in a The xml format: 
<page>
  <id>
  <title>
  <text>
  <links>
</page>
the links are all the links the document points to but we didn't use this option
To run it:
run the scrap_wiki.py,
it wil create  a test.dat file containing the articles.


Then, createIndex_tfidf.py will create the inverted index and the title index.

Finally, run the ex.py file to start the Flask server on port 5000.

You can now run it on your browser :)

