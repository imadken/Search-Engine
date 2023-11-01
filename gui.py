import gradio as gr
import pandas as pd
from back import load_descripteurs_and_inverse

# Sample data (replace this with your data)
# data = {
#     'term': ['apple', 'orange', 'banana'],
#     'document_id': [1, 2, 3],
#     'frequency': [5, 3, 2],
#     'weight': [0.8, 0.6, 0.4]
# }

# df = pd.DataFrame(data)

# Gradio interface

# load descripteurs and inverses
processed_docs_dict = load_descripteurs_and_inverse()


def search_engine(search_term, tokenization, stemming, display_option, grouping_option):
    global processed_docs_dict

    # retrieve inputs

    words = "regex" if tokenization == True else "split"

    stem = "lancester" if stemming == True else "port"

    collection = "inverse" if display_option == "docsperterm" else "descripteur"

    # output
    if search_term == "":
        result_df = processed_docs_dict[f"{collection}_{words}_{stem}"]

    elif collection == "inverse":

        result_df = processed_docs_dict[f"{collection}_{words}_{stem}"]
        result_df = result_df[result_df["term"] == search_term]

    else:
        result_df = processed_docs_dict[f"{collection}_{words}_{stem}"]
        result_df = result_df[result_df["doc"] == f"D{search_term}"]

    # if display_option == 'docsperterm':
    #     result_df = df[df['term'].str.contains(search_term, case=False)]
    # else:
    #     result_df = df[df['document_id'] == int(search_term)]

    return result_df.to_html(index=False)
    # return result_df[['doc', 'term', 'frequency', 'weight']].to_html(index=False)


iface = gr.Interface(
    fn=search_engine,
    inputs=[
        gr.Textbox(label="Search Term"),
        gr.Checkbox("Tokenization"),
        gr.Checkbox("Lancaster"),
        gr.Radio(choices=["docsperterm", "termsperdoc"],
                 label="display Option", value="termsperdoc")

    ],
    outputs=gr.HTML(),
    live=True
)

iface.launch()
