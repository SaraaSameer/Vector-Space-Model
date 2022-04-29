# Vector-Space-Model
## Description
In this project, Vector Space Model is implemented for information retrieval. The weighting scheme used for VSM model is tf * idf scores which is a combination
of both tf (term frequency of term t in a document) and idf (inverse document frequency computing as (log(df)/ N).
### Dataset
The dataset for this model is a collection of 448 abstracts of some computer science journal. The language of all these documents are English. In addition to this, stopwords file for preprocesing and gold-queries results for validation testing is also provided.

## Getting Start with FASTAPI
The UI is rendered on HTML Template via FastAPI
**Steps to excute FastAPI app
1. py -m pip install fastapi uvicorn Jinja2
2. py -m uvicorn filename:app --reload
3. In the output, there is a line something like:
> INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
That line shows the URL where your app is being served, in your local machine.
4. Open the browser at http://127.0.0.1:8000.

## GUI 

![image](https://user-images.githubusercontent.com/62524722/165932073-dc09f60e-918a-400b-b37b-b0d3872a4aff.png)

