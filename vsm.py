import re
from nltk.stem import PorterStemmer
import string
import numpy as np
import matplotlib.pyplot as plt


#------------------------Data Cleaning------------------------------
sw= []
with open ("Stopword-List.txt","r") as file:
    for line in file:
        sw+=line.split()
            
def stopwords_removal(line):
    line_without_sw = [word for word in line.split() if not word in sw]
    return line_without_sw

def cleaning(term):
        ps = PorterStemmer()
        term = term.lower()  #Normalize text
        term = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", term) #Remove Unicode
        term = re.sub(r'[^\w\s]','',term)
        term = re.sub(r'[0-9]', '', term)
        term = ps.stem(term)  #Stemming
        return term

#------------------------------- Inverted Index-----------------------------------
tokens_dict = dict()

for i in range(1,449):
    doc_no = i
    list_of_words = []
    with open ("Abstracts/" + str(doc_no) + ".txt","r") as file:
        # Removing punctations manually because some conventions are modified.
        file = file.read().replace(".","").replace("n't"," not").replace("'","").replace("]"," ").replace("[","").replace(","," ").replace("?","").replace("\n"," ").replace("-"," ").replace('/'," ").split()
        for line in file: 
            line = stopwords_removal(line)
            for word in line:
                word = cleaning(word)
                if word in tokens_dict:
                    tokens_dict[word].add(i)
                else:
                    tokens_dict[word]= {i}  #To add more docs

#---------------------------- IDF--------------------------------------------
#IDF is universal value
def IDF(word):
    len_docs = 448 # Number of documents
    for k,v in tokens_dict.items():
        if word == k:
            return 1+ np.log(len_docs / len(v))
#             return round(np.log(len_docs / len(v)),5)


#---------------------------- TF ------------------------------------------
def normalized_TF(word,doc, len_doc):
    word_count = 0
    for term in doc:
        if word == term:
            word_count +=1  
    #print(round((word_count/len_doc),2))
    return word_count

#---------------------------------- TF * IDF ---------------------------------
def tf_idf(doc):
    vec = list()
    for word in doc:
        tf = normalized_TF(word,doc,len(doc))
        idf = IDF(word)
        score = tf*idf
        vec.append(score)
        
    return vec

cleaned_docs = []
def text_cleaning():
    for i in range(1,449):
        #print(i)
        temp_doc = []
        with open ("Abstracts/" + str(i) + ".txt","r") as file:
        # Removing punctations manually because some conventions are modified.
            file = file.read().replace(".","").replace("n't"," not").replace("'","").replace("]"," ").replace("[","").replace(","," ").replace("?","").replace("\n"," ").replace("-"," ").replace('/'," ").split()
            for line in file: 
                line = stopwords_removal(line)
                for word in line:
                    word = cleaning(word)
                    if word != "":
                        temp_doc.append(word)
        cleaned_docs.append(temp_doc)

#-------------------------------- Document Vectors ---------------------------
text_cleaning()
doc_vec = []

def doc2vector(): 
    for index,doc in enumerate(cleaned_docs):
        vec =tf_idf(doc)
        doc_vec.append(vec)
doc2vector() 


#---------------------------------- Cosine Similarity-------------------------
#This function will make doc_vector that have tf_idf calculated for each term of every document
def cosine_similarity(query_score, doc_score):
#     print(np.dot(query_score,doc_score))
    dot_prod = np.dot(query_score,doc_score)
    query_vec_len = np.square(query_score).sum()
    doc_vec_len = np.square(doc_score).sum()
#     print(query_vec_len)
#     print(doc_vec_len)
    
    cosine_sim = dot_prod / (query_vec_len * doc_vec_len)
#     print(cosine_sim)
    return round(cosine_sim,5)

#------------------------------- Visualization ------------------------------------------
# This function will use matplotlib to visualize results
def visualize(result_dict):
    docs = list(result_dict.keys())
    print(docs)
    cos = list(result_dict.values())
    print(cos)
    plt.figure(figsize=(8,5))
    plt.plot(docs, cos ,"b.-", label= 'cosine-similarity')
    plt.legend()
    plt.xlabel("Documents")
    plt.ylabel("Cosine Similarity")
    # plt.title(f'Results for "{query}"')
    #plt.xticks(gas.Year[::3].tolist()+[2011])
    plt.savefig("visualization/graph.png", dpi= 300)    #dpi=300 for good resolution