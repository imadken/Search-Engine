import gradio as gr
import pandas as pd
from back import load_descripteurs_and_inverse , process_query ,RSV
from metrics import Precision, Precision_5, Precision_10,real_precision_recall,interpolated_precision_recall,plot,display_metrics
from parsing import Load_queries, Load_relevance

from re import escape
import nltk
import matplotlib.pyplot as plt


porter_stemmer = nltk.PorterStemmer()
lanc_stemmer = nltk.LancasterStemmer()

# Gradio interface

# load descripteurs and inverses
processed_docs_dict = load_descripteurs_and_inverse()
# load queries and relevent docs
queries = Load_queries()
relevant_docs = Load_relevance()




def search_engine(search_term,QueryId,tokenization, lancester, display_option, Search_Method,pertinence,Vector_space_model,K,B):
    global processed_docs_dict
    
    #init
    plot()
    evaluation_df = pd.DataFrame([],columns=["Precision","Precision@10","Precision@5","Recall","F1-score"])
    
    # retrieve inputs

    words = "regex" if tokenization == True else "split"

    stem = "lancester" if lancester == True else "port"

    collection = "inverse" if display_option == "docsperterm" else "descripteur"
    
    
    
    if pertinence== True and search_term=="" and QueryId == "None":
           result_df=f"please enter a query"
    
    # elif pertinence == True and search_term!="":
    elif pertinence == True :
        #if query is selected then use it
        if QueryId != "None": 
            # print(queries[QueryId])
            search_term = queries[QueryId]
        
        query = process_query(search_term,tokenize=words,stemming=stem)
        # result_df = RSV(query , processed_docs_dict[f"inverse_{words}_{stem}"] ,Vector_space_model,search_term,stem,K,B,sumpow2[f"inverse_{words}_{stem}"])
        result_df = RSV(query , processed_docs_dict[f"inverse_{words}_{stem}"] ,Vector_space_model,search_term,stem,K,B)
        if QueryId != "None" and type(result_df)!=str:
            
            # print(f"processed query {query}")
            
            real = real_precision_recall(result_df.iloc[:10],relevant_docs[QueryId])
            interpolated = interpolated_precision_recall(real)
            
            # evaluation_df = display_metrics(result_df,relevant_docs[QueryId])
            evaluation_df = display_metrics(result_df,relevant_docs[QueryId])
            
            plot(interpolated["recall"],interpolated["precision"]) 
            
            print(real)
            print(interpolated)
            
    
    
           
        
    else:
         if lancester == True:
            search_term = lanc_stemmer.stem(search_term)
         else:
            search_term = porter_stemmer.stem(search_term) 
    # output
         if search_term == "":
             result_df = processed_docs_dict[f"{collection}_{words}_{stem}"]
         
         elif collection == "inverse":
     
             result_df = processed_docs_dict[f"{collection}_{words}_{stem}"]
     
             if Search_Method == "Whole word":
                 result_df = result_df[result_df["term"] == search_term]
             elif Search_Method == "Starts with":
                 result_df = result_df[result_df["term"].str.startswith(
                     search_term)]
             else:
                 result_df = result_df[result_df["term"].str.contains(
                     escape(search_term))]
                 
         else:
             result_df = processed_docs_dict[f"{collection}_{words}_{stem}"]
             try:
                result_df = result_df[result_df["doc"] == int(search_term)]
             except ValueError:
                 gr.Warning("Please enter a document number, only integers are accepted")
                    
             # print(f" {search_term} = {len(result_df)}")
    
        
    # if type(result_df)==str:
    #     return result_df
    if type(result_df)==str:
        gr.Warning(result_df)
        return pd.DataFrame([]), evaluation_df, plt
    
    
    
    
         
    # result_df.reset_index(inplace=True)
    # print(result_df.reset_index().columns)
    # return result_df.reset_index(drop=True)
    # return result_df.reset_index(drop=True).to_html(index=False)
    return result_df.reset_index(drop=True),evaluation_df, plt
    # return result_df[['doc', 'term', 'frequency', 'weight']].to_html(index=False)


iface = gr.Interface(
    fn=search_engine,
    inputs=[
        gr.Textbox(label="Search Term"),
        gr.Dropdown(label="QueryId", choices= ["None"]+list(queries.keys()), value="None"),
        gr.Checkbox(label="Tokenization",value=True),
        gr.Checkbox(label="Lancaster"),
        gr.Radio(choices=["docsperterm", "termsperdoc"],
                 label="display Option", value="docsperterm"),
        gr.Dropdown(label="Search Method", choices=[
                    "Whole word", "Starts with", "Contains"], value="Contains"),
        gr.Checkbox(label="Pertinence"),
        gr.Dropdown(label="Model", choices=[
                    "Scalar", "Cosine", "Jaccard","BM25","Bool"], value="Scalar"),
        gr.Number(label="K",value=2.0),
        gr.Number(label="B",value=0.5)
    ],
    # outputs=gr.HTML(),
    # outputs=[gr.HTML(), gr.HTML()],
    outputs=[gr.DataFrame(), gr.DataFrame(), gr.Plot()],
    # outputs=gr.DataFrame(),
    live=False,
    allow_flagging="never",
    title="Search Engine",
    theme=gr.themes.Soft()
    
    
)

iface.launch(inbrowser=True)

