import requests
import requests
from xml.etree import ElementTree
from yattag import Doc, indent

#scrap source code html
def get_page(url):
    try:
        session = requests.Session()
        result = session.get(url)
        return str(result.content)
    except:
        return ""
    return ""

def get_next_url(page):
    start_link=page.find("a href")
    if(start_link==-1):
        return None,0
    start_quote=page.find('"',start_link)
    end_quote=page.find('"',start_quote+1)
    url=page[start_quote+1:end_quote]
    return url,end_quote

#get all wiki links from page
def get_all_wiki_links(page):
    links=[]
    while(True):
        url,n=get_next_url(page)
        page=page[n:]
        if url and url[0:5]=='/wiki' and ':' not in url:
            links.append('https://en.wikipedia.org'+url)
        if url:
            continue
        else:
            break
    return links


## scrap id,title,content from xml wiki page
def scrap_page(link):
    tree = ElementTree.fromstring(get_page(link))
    title = tree[1].find('{http://www.mediawiki.org/xml/export-0.10/}title').text.encode('utf-8')
    id_wiki = tree[1].find('{http://www.mediawiki.org/xml/export-0.10/}id').text
    page_content = tree[1][3].find('{http://www.mediawiki.org/xml/export-0.10/}text').text.encode('utf-8')
    return title,id_wiki, page_content

# put extraction in xml format 
def xml_format(title,id_wiki, page_content, links):
    doc, tag, text = Doc().tagtext()

    with tag('page'):
        with tag('id'):
            text(id_wiki)
        with tag('title'):
            text(title)
        with tag('text'):
            text(page_content)
        with tag('links'):
            for l in links:
                with tag('link'):
                    text(l.encode('utf-8'))
                    
    result = indent(
        doc.getvalue()
    )

    return result

#merge two lists with checking scraped
def union(a,b,scraped):
    for e in b:
        if e not in a:
            print e
            if e not in scraped:
                a.append(e)	
	
#start scraping from the link given in seed and stop at 50000 links scraped as defined below
def scrap_web(seed,writer):
    toscrap=[seed]
    scraped=[]
    while toscrap:
        p=toscrap.pop()
        #print p
        links=get_all_wiki_links(get_page(p))

        try:
            title,id_wiki, page_content=scrap_page('https://en.wikipedia.org/wiki/Special:Export'+p[p.rfind('/'):])
            xml_res=xml_format(title,id_wiki, page_content,links)
            writer.write(xml_res + '\n')
        except:
            pass
        scraped.append(p)
        union(toscrap,links,scraped)
        if len(scraped)==50000:
            return toscrap,scraped
            break

#saving the result data in test.dat starting from the wiki page Web Search Engine
with open('test.dat', 'w') as writer:
    scrap_web('https://en.wikipedia.org/wiki/Web_search_engine',writer)