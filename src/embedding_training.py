from sentence_transformers import SentenceTransformer
from text_processing import TextSplitter
import faiss
import math
import os

splitter = TextSplitter()

index_path = os.path.join(os.getcwd().split("src")[0], "data", "index.index")
model_path = os.path.join(os.getcwd().split("src")[0], "model")


def save_data(text, document_name: str):
    """ Used to save data to the data folder. It creates a new folder for every new document added.
        It then adds all the text chunks in the newly created folder as text file documents with incrementing values
    """
    splits_path = os.path.join(os.getcwd().split("src")[0], "data", document_name)

    os.makedirs(splits_path, exist_ok = True)

    for i, chunk in enumerate(text):
        file_path = os.path.join(splits_path, f"doc_{i}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("%s" % chunk)

def load_data():
    """ Function used to load data from the folders we saved them in. """

    all_splits = []

    save_dir = os.path.join(os.getcwd().split("src")[0], "data")

    for folder in os.listdir(save_dir):
        folder_dir = os.path.join(save_dir, folder)
        
        if not os.path.isdir(folder_dir):
            continue

        if os.path.exists(folder_dir):

            for file in os.listdir(folder_dir):
                file_path = os.path.join(folder_dir, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    text = [line.strip() for line in f]
                    all_splits.append(text)
        else:
            print("Tried to read an invalid folder path")

    return all_splits

def init_index(text: str, document_name: str):

    """ init_index is meant to be ran once by the user. It initalizes the index and the embedding model that will be used.
        For the init_index function to work, it has to be passed a text string as data.
    """

    dims = 768
    index =  faiss.IndexFlatL2(dims)

    embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding_model.save(model_path)

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
    faiss.write_index(index, index_path)

def train_and_update_index(text: str, document_name: str, do_retrain = True):

    """ Function is used to train the new index on new data and update it or to just add the data to the index
        index_path is where the index is store. Document Name is the name of the document without the .pdf, .doxc, etc.
    """

    splitted_text = splitter.split_text(text)

    index = faiss.read_index(index_path)
    embedding_model = SentenceTransformer(model_path)

    if do_retrain:

        all_splits = load_data()
        print(all_splits[0])

        combined_text = list(set(splitted_text + list(all_splits)))
        embeddings = embedding_model.encode(combined_text)

        print("Retraining the index...")
        index.train(embeddings)
        index.add(embeddings)

    else:
        embeddings = embedding_model.encode(splitted_text)

        print("Training the index...")
        index.add(embeddings)

    print("Saving data...")
    save_data(splitted_text, document_name)

    faiss.write_index(index, index_path)


def retrive_documents(query, all_splits, k = 3):
    """ Function to retrive documents from the index """

    index = faiss.read_index(index_path) 
    embedding_model = SentenceTransformer(model_path)   

    query_embedding = embedding_model.encode([query])
    _, indices = index.search(query_embedding, k)
    retrived_documents = [all_splits[i] for i in indices[0]]

    return retrived_documents

docs_cache = []

def inference(query: str, text, document_name: str, k = 3, retrain = False):
    """ The function will be used for handling usual user queries """

    if text is not None:
        train_and_update_index(text, document_name = document_name, do_retrain = retrain)

    all_splits = load_data()

    documents = retrive_documents(query, all_splits, k = k)
    for i, doc in enumerate(documents):
        print(f"\n\033[1mDocument Number ({i + 1})\033[0m\n")
        print("\n".join(doc))
        docs_cache.append(doc)