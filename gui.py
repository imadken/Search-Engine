import gradio as gr
import pandas as pd
from back import load_descripteurs_and_inverse , process_query ,RSV
from re import escape
import nltk
porter_stemmer = nltk.PorterStemmer()
lanc_stemmer = nltk.LancasterStemmer()

# Gradio interface

# load descripteurs and inverses
processed_docs_dict = load_descripteurs_and_inverse()


def search_engine(search_term, tokenization, lancester, display_option, Search_Method,pertinence,Vector_space_model,K,B):
    global processed_docs_dict

    # retrieve inputs

    words = "regex" if tokenization == True else "split"

    stem = "lancester" if lancester == True else "port"

    collection = "inverse" if display_option == "docsperterm" else "descripteur"
    
    if pertinence == True and search_term!="":
        
        query = process_query(search_term,tokenize=words,stemming=stem)
        result_df = RSV(query , processed_docs_dict[f"inverse_{words}_{stem}"] ,Vector_space_model,search_term,stem,K,B)

    
    elif pertinence== True and search_term=="":
           result_df=f"please enter a query"
        
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
             result_df = result_df[result_df["doc"] == f"D{search_term}"]
             # print(f" {search_term} = {len(result_df)}")
    
         
    if type(result_df)==str:
        return result_df
         
    return result_df.reset_index().to_html(index=False)
    # return result_df[['doc', 'term', 'frequency', 'weight']].to_html(index=False)


iface = gr.Interface(
    fn=search_engine,
    inputs=[
        gr.Textbox(label="Search Term"),
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
        gr.Number(label="B",value=1.5)
    ],
    outputs=gr.HTML(),
    live=True,
    allow_flagging="never",
    title="Search Engine",
    theme=gr.themes.Soft()
)

iface.launch(inbrowser=True)

