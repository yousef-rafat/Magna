from src.setup_and_processing import install_required_packages, get_text, remove_folder, print_saved_documents, save_cached_docs
from text_processing import find_files_from_special_folders, inference
from embedding_training import init_index
import argparse
import os

loaded_files = []
intialized = False
current_file = None

def initalize(file_path: str):

    document_name = file_path.split("/")[-1].split(".")[0]

    cwd = os.getcwd()
    rag_dir = os.path.join(cwd, "data")
    os.mkdir(rag_dir)

    install_required_packages()
    text = get_text(file_path)

    if text is None:
        print("Unsupported file extension passed. Please use PDF, DOXC, or TXT files.")
        return

    init_index(text = text, rag_path = rag_dir, document_name = document_name)

def main():
    parser = argparse.ArgumentParser(description = "AI Embedding Similarity Search For Documents")
    parser.add_argument("--file", type = str, help = "File to read and search")
    parser.add_argument("--init", action = "store_true", help = "Intializes the model, libraries, setup, etc. This command should be ran once")
    parser.add_argument("-k", type = int, default = 3, help = "Amount of returned results")
    parser.add_argument("--query", type = str, help = "The search query for searching in the document.")
    parser.add_argument("--filetypes", nargs = '+', help = "The file types to search for. PDF, DOXC, TXT")
    parser.add_argument("--search_files", action = "store_true", help = "Search for files with either a PDF, TXT, or DOXC file extensions")
    parser.add_argument("-remove", type = str, help = "Folder to remove from the index database.")
    parser.add_argument("--print", action = "store_true", help = "Print current saved documents in the index.")
    parser.add_argument("--text_size", type = int, help = "Length of the document(s) returned.")
    parser.add_argument("-s", action = "store_true", help = "Search in the document and print the returned result.")
    parser.add_argument("--no_retrain", action = "store_true", help = "Adds data to the index without retraining the index search on it. May produce worse results.")
    parser.add_argument("--save", action = "store_true", help = "Save the latest documents displayed into a file at Documents")
    parser.add_argument("--save_file", type = str, help = "The name of the file to be saved.")
    args = parser.parse_args()
    global current_file

    if args.file:
        if args.file not in loaded_files:
            loaded_files.append(args.file)
        current_file = args.file

    global intialized
    global loaded_files

    if args.remove:
        remove_folder(folder_name = args.remove)

    if args.print:
        print_saved_documents()

    if args.search_files:
        if args.filetypes:
            find_files_from_special_folders(filetypes = args.filetypes)
        else:
            find_files_from_special_folders()

    if args.save:
        if args.save_file: save_cached_docs(args.save_file)
        else: save_cached_docs()

    if (not args.init) and args.s:
        if args.query:
            if current_file is None:
                print("No file was given. Please try again with a file")
                return
            else:
                text = get_text(current_file)

                if text is None:
                    print("Unsupported file extension passed. Please use PDF, DOXC, or TXT files.")
                    return
                
                if args.k: inference(query = args.query, text = text, k = args.k)
                else: inference(query = args.query, text = text)

    if args.init:
        if not intialized:
            print("Initalizing the application. This may take some time.")

            if args.file:
                initalize(args.file)
            else:
                print("No file provided for initalization.")

            intialized = True
        else:
            print("The embedding similarity has already been intialized.")


if __name__ == "__main__":
    main()