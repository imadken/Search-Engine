import os
import pandas as pd
import nltk
from math import sqrt,log10
import re


def load_processed_docs(folder_path):
    """Reads all files in a given Folder

    Returns:
        dict:dictionnary of all files that have been read
    """

    docs_content = dict()

    # Ensure the path is a directory
    if os.path.isdir(folder_path):
        # List all files in the directory
        files = os.listdir(folder_path)

        for file_name in files:
            # Check if the file is a text file
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                content = pd.read_csv(file_path, sep=" ")

                # Store the text content in the dictionary
                docs_content[file_name.replace(".txt", "")] = content

    return docs_content


def load_descripteurs_and_inverse():
    """returns a dictionnary with all descripteurs and inverse documents
     example : {"inverse_split_port":datadrame(term,doc,frequency,weight),...}
    """

    descripteurs, inverses = load_processed_docs(
        "descripteurs"), load_processed_docs("inverse")

    descripteurs.update(inverses)

    return descripteurs




def split_tokenizer(txt):
    return [token for token in txt.split()]

def regex_tokenizer(txt,regex='(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[\.\,]\d+)?%?|\w+(?:[\-/]\w+)*'):
    reg = nltk.RegexpTokenizer(regex)
    return reg.tokenize(txt)

def stop_remove(tokens):
    stop = nltk.corpus.stopwords.words('english')
    return [term.lower() for term in tokens if term.lower() not in stop]

def porter_stem(tokens):
    porter = nltk.PorterStemmer()
    return[porter.stem(term) for term in tokens]

def lancester_stem(tokens):
    # lancester = nltk.PorterStemmer()
    lancester = nltk.LancasterStemmer()
    return[lancester.stem(term) for term in tokens]


def process_query(query,tokenize= "regex",stemming="Port"):
    
    """tokenize, remove stopwords and stem
       
       query : the searched sentence
       tokenize : regex or split
       stemming : port for porter else lancester
       
    Returns:
        _type_: _description_
    """
    
    tokens = regex_tokenizer(query) if tokenize.lower()=="regex" else split_tokenizer(query)
    tokens = stop_remove(tokens)
    tokens = porter_stem(tokens) if stemming.lower()== "port" else lancester_stem(tokens)
    
    return tokens

def Scalar(query_tokens,inverse_doc):
    result=dict()
    # sum_w_i=dict()
    for term in query_tokens:  
        search_result = inverse_doc[inverse_doc["term"] == term]
        for i in range(len(search_result)):
           result[search_result.iloc[i,1]] = result.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
            #  sum_w_i[search_result.iloc[i,1]] = sum_w_i.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
    
    
    # for key , value in sum_w_i.items():
        # result[key]  = value 
   
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"])   


def Cosine(query_tokens,inverse_doc):
    
    result=dict()
    
    sum_w_i = dict()
    sum_w_i_2 = dict()
    nbr_query_terms = dict()
    
    
    for i in range(len(inverse_doc)):
            sum_w_i_2[inverse_doc.iloc[i,1]] = sum_w_i_2.get(inverse_doc.iloc[i,1],0)+(pow(inverse_doc.iloc[i,-1],2))
    
    for term in query_tokens:  
        search_result = inverse_doc[inverse_doc["term"] == term]

        for i in range(len(search_result)):
            sum_w_i[search_result.iloc[i,1]] = sum_w_i.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
            nbr_query_terms[search_result.iloc[i,1]] = nbr_query_terms.get(search_result.iloc[i,1],0) + 1
            
     
    for key , value in sum_w_i.items():
 
         
        # result[key]  = value / (sqrt(sum_w_i_2[key])*sqrt(nbr_query_terms[key])) 
        result[key]  = value / (sqrt(sum_w_i_2[key])*sqrt(len(query_tokens))) 
        
     
         
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"]).reset_index(drop=True) 


def Jaccard(query_tokens,inverse_doc):
    result=dict()
    
    sum_w_i = dict()
    sum_w_i_2 = dict()
    nbr_query_terms = dict()
    
    for i in range(len(inverse_doc)):
            sum_w_i_2[inverse_doc.iloc[i,1]] = sum_w_i_2.get(inverse_doc.iloc[i,1],0)+(pow(inverse_doc.iloc[i,-1],2))
    
    for term in query_tokens:  
        search_result = inverse_doc[inverse_doc["term"] == term]
        
       
        # sum_v_i_ = 0
        
        for i in range(len(search_result)):
       
            sum_w_i[search_result.iloc[i,1]] = sum_w_i.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
            nbr_query_terms[search_result.iloc[i,1]] = nbr_query_terms.get(search_result.iloc[i,1],0) + 1
     
    for key , value in sum_w_i.items():
        
        # result[key]  = value / ((nbr_query_terms[key])+(sum_w_i_2[key])-value) 
        result[key]  = value / ((len(query_tokens))+(sum_w_i_2[key])-value) 
       
       
         
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"]) 


def doc_size(doc_name,inverse_doc):
    # return len(inverse_doc[inverse_doc["doc"] == doc_name])
    return inverse_doc[inverse_doc["doc"] == doc_name]["frequency"].sum()
    
    
def docs_mean(inverse_doc):
    
    docs = inverse_doc["doc"].unique()
    sum = 0
    
    for doc in docs:
        sum += doc_size(doc,inverse_doc)
    
    return sum/len(docs)  
  
def docs_size(inverse_doc):
    dl = dict()
    docs = inverse_doc["doc"].unique()
    for doc in docs:
        dl[doc] = doc_size(doc,inverse_doc)
    return dl    

def BM25(query_tokens,inverse_doc,K=1.5,B=0.75,N=6):
    
    avdl = docs_mean(inverse_doc)
    dl =docs_size(inverse_doc)
    result = dict()
    
    for term in query_tokens: 
        
        search_result = inverse_doc[inverse_doc["term"] == term]
        
        frequency = dict()
        n_i = len(search_result["doc"].unique())
        
        
        for i in range(len(search_result)):
            frequency[search_result.iloc[i,1]] = search_result.iloc[i,2]

        for key , value in frequency.items():
  
           result[key]  = result.get(key,0) + ((value/(value+((B*dl[key]/avdl)+1-B)*K)) * log10((N-n_i+0.5)/(n_i+0.5)))
         
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"]).reset_index(drop=True) 


def is_valid_query(query):
    
    tokens = [f"'{token}'" if token.lower() not in ("and", "or", "not") else token.lower() for token in query.split()]
    try:
        eval(" ".join(tokens))
    except SyntaxError:
        valid = False
    else:valid = True
    
    return valid


def Bool_model(query,inverse_doc,stemming):
    
    if not is_valid_query(query):
        return f" '{query}' is not a valid query"

    # return f" '{query}' is a valid query"
    query = query.lower()
    #get terms
    query_terms=[]
    for token in query.split():
        if token not in ("and", "or", "not"): query_terms.append(token)
    #stemmer
    tokens = porter_stem(query_terms) if stemming.lower()== "port" else lancester_stem(query_terms)   
    
    documents =dict()
    
    #for each document, append terms that exists
    for term in tokens:
         search_result = inverse_doc[inverse_doc["term"] == term]
         for i in range(len(search_result)):
            documents.setdefault(search_result.iloc[i,1], []).append(term)
    # print(documents)
    
    results=dict()
    
    for key , doc_terms in documents.items():
        
            query_copy = query
            for t in query_terms:
                cont = False
                for term in doc_terms:
                    if term in t:
                        cont =True
                if cont: query_copy = query_copy.replace(t,"1") 
                else:query_copy = query_copy.replace(t,"0")         
            
            try:
               results[key] = eval(query_copy)   
            except SyntaxError as e:
                print(e)
                return f" '{query}' is not a valid query"
                    
    # print(results)        
            
            
     
    return pd.DataFrame(results.items(),columns=["Doc","Relevance"]).reset_index(drop=True) 
    # return f" '{query}' is  a valid query"     




def RSV(query , processed_docs_dict , Vector_space_model,search_term,stemming):
    
    if Vector_space_model == "Scalar":
        return Scalar(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    elif Vector_space_model == "Cosine":
           
        return Cosine(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    
    elif Vector_space_model == "Jaccard" :
       return Jaccard(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    
    elif Vector_space_model == "BM25": 
         return BM25(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    # # print(result_df)
    elif Vector_space_model == "Bool" :
            # return pd.DataFrame([is_valid_query(search_term)],columns=["valid"])    
            return Bool_model(search_term,processed_docs_dict,stemming)    
        
        
        
        
        
        
        
        
        