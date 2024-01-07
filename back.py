import os
import pandas as pd
import nltk
from math import sqrt,log10
from Bool import Boolean_model
from time import time



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
        "lisa/descripteurs"), load_processed_docs("lisa/inverse")

    descripteurs.update(inverses)

    return descripteurs




def split_tokenizer(txt):
    return [token for token in txt.split()]

# def regex_tokenizer(txt,regex='(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[\.\,]\d+)?%?|\w+(?:[\-/]\w+)*'):
def regex_tokenizer(txt,regex="(?:[A-Za-z]\.)+|[A-Za-z]+[\-@]\d+(?:\.\d+)?|\d+[A-Za-z]+|\d+(?:[\.\,]\d+)?%?|\w+(?:[\-/]\w+)*"):
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
    query_tokens = list(set(query_tokens))
    for term in query_tokens:  
        search_result = inverse_doc[inverse_doc["term"] == term]
        for i in range(len(search_result)):
           result[search_result.iloc[i,1]] = result.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
            #  sum_w_i[search_result.iloc[i,1]] = sum_w_i.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
    
    # all_docs = inverse_doc['doc'].unique()
    # for doc in all_docs:
    #     if doc not in result.keys():
    #         result[doc]=0
    # for key , value in sum_w_i.items():
        # result[key]  = value 
   
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"])   

# def load_sum_w_i_2(inverse_doc):
#       sum_w_i_2 = dict()
#       for i in range(len(inverse_doc)):
#                   sum_w_i_2[inverse_doc.iloc[i,1]] = sum_w_i_2.get(inverse_doc.iloc[i,1],0)+(pow(inverse_doc.iloc[i,-1],2))
#       return sum_w_i_2
    



def Cosine(query_tokens,inverse_doc):
    
    result=dict()
    query_tokens = list(set(query_tokens))
    sum_w_i = dict()
    # sum_w_i_2 = dict()
    # sum_w_i_2 = sumpow2
    nbr_query_terms = dict()
    grouped_data = inverse_doc.groupby("doc")["weight"].apply(lambda x: (x**2).sum())
    sum_w_i_2 = grouped_data.to_dict()
    
    

    # s= time()
    # for i in range(len(inverse_doc)):
    #         sum_w_i_2[inverse_doc.iloc[i,1]] = sum_w_i_2.get(inverse_doc.iloc[i,1],0)+(pow(inverse_doc.iloc[i,-1],2))
    # print(f"time for sumpow2 is {time()-s}")
    for term in query_tokens:  
        search_result = inverse_doc[inverse_doc["term"] == term]

        for i in range(len(search_result)):
            sum_w_i[search_result.iloc[i,1]] = sum_w_i.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
            nbr_query_terms[search_result.iloc[i,1]] = nbr_query_terms.get(search_result.iloc[i,1],0) + 1
            
     
    for key , value in sum_w_i.items():
        # result[key]  = value / (sqrt(sum_w_i_2[key])*sqrt(nbr_query_terms[key])) 
        result[key]  = value / (sqrt(sum_w_i_2[key])*sqrt(len(query_tokens))) 
        
    # all_docs = inverse_doc['doc'].unique()
    # for doc in all_docs:
    #     if doc not in result.keys():
    #         result[doc]=0 
         
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"]).reset_index(drop=True) 


def Jaccard(query_tokens,inverse_doc):
    result=dict()
    query_tokens = list(set(query_tokens))
    sum_w_i = dict()
    # sum_w_i_2 = dict()
    nbr_query_terms = dict()

    grouped_data = inverse_doc.groupby("doc")["weight"].apply(lambda x: (x**2).sum())
    sum_w_i_2 = grouped_data.to_dict()
    
    # for i in range(len(inverse_doc)):
    #         sum_w_i_2[inverse_doc.iloc[i,1]] = sum_w_i_2.get(inverse_doc.iloc[i,1],0)+(pow(inverse_doc.iloc[i,-1],2))
    
    for term in query_tokens:  
        search_result = inverse_doc[inverse_doc["term"] == term]
 
        for i in range(len(search_result)):
       
            sum_w_i[search_result.iloc[i,1]] = sum_w_i.get(search_result.iloc[i,1],0) + search_result.iloc[i,-1]
            nbr_query_terms[search_result.iloc[i,1]] = nbr_query_terms.get(search_result.iloc[i,1],0) + 1
     
    for key , value in sum_w_i.items():
        
        # result[key]  = value / ((nbr_query_terms[key])+(sum_w_i_2[key])-value) 
        result[key]  = value / ((len(query_tokens))+(sum_w_i_2[key])-value) 
    
    # all_docs = inverse_doc['doc'].unique()
    # for doc in all_docs:
    #     if doc not in result.keys():
    #         result[doc]=0    
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"]) 


def doc_size(doc_name,inverse_doc):
    # return len(inverse_doc[inverse_doc["doc"] == doc_name])
    return inverse_doc[inverse_doc["doc"] == doc_name]["frequency"].sum()
    
def docs_mean(inverse_doc):
    doc_sizes = inverse_doc.groupby("doc")["frequency"].sum()
    return doc_sizes.mean()    
# def docs_mean(inverse_doc):
    
#     docs = inverse_doc["doc"].unique()
#     sum = 0
#     for doc in docs:
#         sum += doc_size(doc,inverse_doc)
    
#     return sum/len(docs)  
def docs_size(inverse_doc):
    doc_sizes = inverse_doc.groupby("doc")["frequency"].sum().to_dict()
    return doc_sizes  
# def docs_size(inverse_doc):
#     dl = dict()
#     docs = inverse_doc["doc"].unique()
#     for doc in docs:
#         dl[doc] = doc_size(doc,inverse_doc)
#     return dl    

def BM25(query_tokens,inverse_doc,K=2,B=1.5,N=5999):
    s = time()
    avdl = docs_mean(inverse_doc)
    dl =docs_size(inverse_doc)
    print(f"time for sumpow2 is {time()-s}")
    result = dict()
    
    for term in query_tokens: 
        
        search_result = inverse_doc[inverse_doc["term"] == term]
        
        frequency = dict()
        n_i = len(search_result["doc"].unique())
        
        for i in range(len(search_result)):
            frequency[search_result.iloc[i,1]] = search_result.iloc[i,2]

        for key , value in frequency.items():
  
           result[key]  = result.get(key,0) + ((value/(value+((B*dl[key]/avdl)+1-B)*K)) * log10((N-n_i+0.5)/(n_i+0.5)))
    
    # all_docs = inverse_doc['doc'].unique()
    # for doc in all_docs:
    #     if doc not in result.keys():
    #         result[doc]=0     
    # return result.items()        
    return pd.DataFrame(result.items(),columns=["Doc","Relevance"]).reset_index(drop=True) 


def is_valid_query(query):
    
    tokens = ["1" if token.lower() not in ("and", "or", "not") else token.lower() for token in query.split()]
    
    if tokens[-1]=='not':return False
    
    try:
        Boolean_model.evaluate(" ".join(tokens))
        return True
    except ValueError:
        return False
 

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
         
         #if term not in inverse doc
         if len(search_result) == 0:
             query = query.replace(term,"0")
             continue
         
         for i in range(len(search_result)):
            documents.setdefault(search_result.iloc[i,1], []).append(term)
    # print(documents)
    
    results=dict()
    
    #when all terms are not in inverse doc
    if len(documents)==0:
        result = [(doc,0) for doc in list(inverse_doc["doc"].unique())]
        Boolean_model.evaluate(query) 
        return pd.DataFrame(result,columns=["Doc","Relevance"]).reset_index(drop=True)  
     
    #evaluation result for all docs where at least one term appear   
    for key , doc_terms in documents.items():
        
            query_copy = query
            for t in query_terms:
                cont = False
                for term in doc_terms:
                    if term in t:
                        cont =True
                if cont: query_copy = query_copy.replace(t,"1") 
                else:query_copy = query_copy.replace(t,"0")         
     
            results[key] = Boolean_model.evaluate(query_copy)
               
    # all_docs = inverse_doc['doc'].unique()
    # for doc in all_docs:
    #     if doc not in results.keys():
    #         results[doc]=0
    return pd.DataFrame(results.items(),columns=["Doc","Relevance"]).reset_index(drop=True) 
    # return f" '{query}' is  a valid query"     




# def RSV(query , processed_docs_dict , Vector_space_model,search_term,stemming,K,B,sumpow2):
def RSV(query , processed_docs_dict , Vector_space_model,search_term,stemming,K,B):
    
    if Vector_space_model == "Scalar":
        return Scalar(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    elif Vector_space_model == "Cosine":
           
        return Cosine(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    
    elif Vector_space_model == "Jaccard" :
       return Jaccard(query,processed_docs_dict).sort_values(by=["Relevance"],ascending=False)
    
    elif Vector_space_model == "BM25": 
         return BM25(query,processed_docs_dict,K=K,B=B).sort_values(by=["Relevance"],ascending=False)
    # # print(result_df)
    elif Vector_space_model == "Bool" :
            # return pd.DataFrame([is_valid_query(search_term)],columns=["valid"])    
            return Bool_model(search_term,processed_docs_dict,stemming)
    else:raise ValueError(f"option -{Vector_space_model}- not Supported")        

    
    
    
    

    
        
if __name__ == "__main__":
            
        # print(is_valid_query("terme term"))
        print(is_valid_query("1 and 1 not"))
        
        
        
        
        