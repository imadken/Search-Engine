import os
import pandas as pd


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
