import uvicorn
from fastapi import FastAPI, Query, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import vsm

app = FastAPI()
templates = Jinja2Templates(directory= 'templates')
app.mount('/static', StaticFiles(directory= 'static'), name = 'static')

# query = ''
# alpha = ''
# docs_output = list()
data = " "
val = "yes"

@app.get('/')
def hello_World():
     return {'Sucesss': 'Sucessfully Loaded'}

@app.get('/basic')
def homepage(request: Request):
    return templates.TemplateResponse('index.html',{'request':request,})

@app.post('/basic')
# The id/name for each form attribute must match parameter name
# 422 Unprocesseble entity means there is some error in XML file(HTML code)

def homepage(request:Request, query: str= Form(...), alpha: str = Form(...)):

        query = vsm.stopwords_removal(query)
        query_list = []
        tf_idf_query_score = []
        cos_sim = []
        data = ' '.join([str(elem) for elem in query])

        for terms in query:
            terms = vsm.cleaning(terms)
            query_list.append(terms)   
        tf_idf_query_score = vsm.tf_idf(query_list)

        docs_intersect_set = set()
        for index, terms in enumerate(query_list):
            for k, v in vsm.tokens_dict.items():
                if terms == k:
                    for docs in v:
                        docs_intersect_set.add(docs)  
        
        docs_intersect_set = sorted(docs_intersect_set)
        for items in docs_intersect_set:
            docs_score = list()
            for terms in query_list:
    #             print(terms)
    #             print(items)
                try:
                    index_ = vsm.cleaned_docs[items-1].index(terms)
                    docs_score.append(vsm.doc_vec[items-1][index_])
                    
                except ValueError:
                    docs_score.append(0)   #For terms that are present in query, but not in document
                    
            cos_sim.append(vsm.cosine_similarity(tf_idf_query_score, docs_score))
            cos_sim = sorted(cos_sim, reverse = True)

            total_doc = 0
            output_dict = dict()
            content = list()
            for index, value in enumerate(cos_sim):
                if value >= float(alpha):  # Alpha value is 0.001
                #  print (f'Doc No: {docs_intersect_set[index]} is retrieved with cosine similarity value of : {value}')
                    output_dict[docs_intersect_set[index]] = value
                    total_doc = total_doc + 1
                    with open ("Abstracts/" + str(docs_intersect_set[index]) + ".txt","r") as file:
                    # Removing punctations manually because some conventions are modified.
                        file = file.read()
                        content.append(file)
        vsm.visualize(output_dict)
        return templates.TemplateResponse('index.html', {'request':request, 'total_doc':total_doc, 
            'results': output_dict , 'data': data , 'enumerate': enumerate, 'content':content})

        # print(f'Total documents retrieved: {total_doc}'
        # if action=='Search':     --Conditional Rendering

if __name__ == 'main':
    uvicorn.run(app)