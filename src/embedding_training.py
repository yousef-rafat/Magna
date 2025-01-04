from sentence_transformers import SentenceTransformer
from text_processing import TextSplitter
import faiss
import math
import os

splitter = TextSplitter()

# Values to be updated once
index, embedding_model = None, None

def save_data(text, document_name: str):
    """ Used to save data to the data folder. It creates a new folder for every new document added.
        It then adds all the text chunks in the newly created folder as text file documents with incrementing values
    """
    splits_path = os.path.join(os.getcwd(), "data", document_name)

    os.makedirs(splits_path, exist_ok = True)

    for i, chunk in enumerate(text):
        file_path = os.path.join(splits_path, f"doc_{i}.txt")
        with open(file_path, "w") as f:
            f.write("%s\n" % chunk)

def init_index(text: str, rag_path: str, document_name: str):

    """ init_index is meant to be ran once by the user. It initalizes the index and the embedding model that will be used.
        For the init_index function to work, it has to be passed a text string as data.
    """

    global index
    global embedding_model

    dims = 768
    index =  faiss.IndexFlatL2(dims)

    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    splitted_text = splitter.split_text(text)

    embeddings = embedding_model.encode(splitted_text)

    dims = embeddings.shape[1] 
    
    nlist = int(math.sqrt(len(embeddings))) # Number of clusters 
    quantizer = faiss.IndexFlatL2(dims)
    
    index = faiss.IndexIVFFlat(quantizer, dims, nlist) 
    print("Index intialized.")

    print("Training and adding the embeddings.")
    index.train(embeddings)
    index.add(embeddings)

    save_data(splitted_text, document_name)

    print("Saving the index")
    faiss.write_index(index, rag_path)

def train_and_update_index(text: str, rag_path: str, document_name: str, do_retrain = True):

    """ Function is used to train the new index on new data and update it or to just add the data to the index
        rag_path is where the index is store. Document Name is the name of the document without the .pdf, .doxc, etc.
    """

    splitted_text = splitter.split_text(text)
    index = faiss.read_index(rag_path)

    if do_retrain:

        # Read all the data we have saved before
        all_splits = []

        save_dir = os.path.join(os.getcwd(), "data")

        # It goes into each folder in the data folder and gets the indiviual files into the variable all_splits
        for folder in os.listdir(save_dir):
            folder_dir = os.path.join(save_dir, folder)

            if os.path.exists(folder_dir):

                for file in os.listdir(folder_dir):
                    file_path = os.path.join(folder_dir, file)

                    with open(file_path, "r") as f:
                        text = [line.strip() for line in f]
                        all_splits.extend(text)
            else:
                print("Tried to read an invalid folder path")

        all_splits = "\n".join(all_splits)

        combined_text = list(set(splitted_text + all_splits))
        embeddings = embedding_model.encode(combined_text)

        index.train(embeddings)
        index.add(embeddings)

    else:
        embeddings = embedding_model.encode(splitted_text)
        index.add(embeddings)

    save_data(splitted_text, document_name)

    faiss.write_index(index, rag_path)


def retrive_documents(query, all_splits, index, k = 3):
    """ Function to retrive documents from the index """    

    query_embedding = embedding_model.encode([query])
    _, indices = index.search(query_embedding, k)
    retrived_documents = [all_splits[i] for i in indices[0]]

    return retrived_documents

docs_cache = []

def inference(query, text, k = 3):
    """ The function will be used for handling usual user queries """
    documents = retrive_documents(query, text, index, k = k)
    for doc in documents:
        print(doc + "\n")
        docs_cache.append(doc)