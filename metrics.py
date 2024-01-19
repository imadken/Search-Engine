import pandas as pd
import matplotlib.pyplot as plt


def plot(r=[],p=[]):
    plt.title("Courbe precision Rappel")
    plt.xlabel("recall")
    plt.ylabel("precision")
    # plt.xlim(0, 1)
    # plt.ylim(-0.1, 1.1)
    plt.scatter(r,p,color='blue') 
    plt.plot(r,p, linestyle='-', color='red', label='Lines')

def Precision(results_df,real_pertinent):
    
    selected_docs = len(results_df['Doc'].unique())
    # print(results_df)
    # print(real_pertinent)
    # print(length)
    
    
    pertinent_docs = set(results_df[results_df['Relevance']!= 0]["Doc"]).intersection(real_pertinent)
    
    # print(f"length of pertinent selected docs = {len(pertinent_docs)}, all selected = {selected_docs}")
    
    return (len(pertinent_docs)/selected_docs)

def Precision_5(results_df,real_pertinent):
    pertinent_docs = set(results_df[results_df['Relevance']!= 0]["Doc"].iloc[:5]).intersection(real_pertinent)
    return (len(pertinent_docs)/5)

def Precision_10(results_df,real_pertinent):
    pertinent_docs = set(results_df[results_df['Relevance']!= 0]["Doc"].iloc[:10]).intersection(real_pertinent)
    return (len(pertinent_docs)/10)   


def Recall(results_df,real_pertinent):
   
    pertinent_docs = set(results_df[results_df['Relevance']!= 0]["Doc"]).intersection(real_pertinent)
    
    return (len(pertinent_docs)/len(real_pertinent))

def F1_score(results_df,real_pertinent):
    p = Precision(results_df,real_pertinent)
    r = Recall(results_df,real_pertinent)
    return (2*r*p)/(r+p)

def display_metrics(results_df,real_pertinent):
    
    return pd.DataFrame([[Precision(results_df,real_pertinent),
                         Precision_10(results_df,real_pertinent),Precision_5(results_df,real_pertinent),
                         Recall(results_df,real_pertinent),F1_score(results_df,real_pertinent)]],
                        columns=["Precision","Precision@10","Precision@5","Recall","F1-score"])
    


def real_precision_recall(results_df,real_pertinent):
    
    result = []
    # print(results_df["Doc"].tolist())
    # print(real_pertinent)
    pertinent_courant = 0
    # Relevance
    pertinents = len(set(real_pertinent).intersection(results_df["Doc"].tolist()))
    
    print(f"doc pertinents = {set(real_pertinent).intersection(results_df['Doc'].tolist())}")
    
    if pertinents == 0 : pertinents = 1
    
    results_df = results_df.reset_index(drop=True)
    for index, row in results_df.iterrows():
        
        if row["Relevance"]!=0 and (row["Doc"] in real_pertinent) : pertinent_courant += 1
        
        p = pertinent_courant/(index+1)
        r = pertinent_courant/ pertinents
        result.append([p,r])
        
    return pd.DataFrame(result,columns=["precision","recall"])
    
    
def interpolated_precision_recall(real_df):
    
    
    result = []
    
    for recall in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
        max = 0
        for index , row in real_df.iterrows():
            if row["recall"] >= recall and max < row["precision"] :
                max = row["precision"]
        
        result.append([max,recall])
        
                
    return pd.DataFrame(result,columns=["precision","recall"])       

   
    
if __name__ =="__main__":
    # interpolated_precision_recall(1)
    pass