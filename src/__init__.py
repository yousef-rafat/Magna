from setup_and_processing import install_required_packages, get_text, remove_folder, print_saved_documents, save_cached_docs
from text_processing import find_files_from_special_folders
from embedding_training import init_index, inference
import argparse
import os

cwd = os.getcwd().split("src")[0]
rag_dir = os.path.join(cwd, "data")

def initalize(file_path: str):

    document_name = file_path.split("/")[-1].split(".")[0]

    if not os.path.exists(rag_dir):
        os.mkdir(rag_dir)

    install_required_packages()
    text = get_text(file_path)

    if text is None:
        print("Unsupported file extension passed. Please use PDF, DOXC, or TXT files.")
        return

    init_index(text = text, document_name = document_name)

def main():
    parser = argparse.ArgumentParser(description = "AI Embedding Similarity Search For Documents")

    parser.add_argument("--file", type = str, help = "File to read and search")
    parser.add_argument("--init", action = "store_true", help = "Intializes the model, libraries, setup, etc. This command should be ran once")
    parser.add_argument("-k", type = int, default = 1, help = "Amount of returned results")
    parser.add_argument("--query", type = str, help = "The search query for searching in the document.")
    parser.add_argument("--filetypes", nargs = '+', help = "The file types to search for. PDF, DOXC, TXT")
    parser.add_argument("--search_files", action = "store_true", help = "Search for files with either a PDF, TXT, or DOXC file extensions")
    parser.add_argument("--remove", type = str, help = "Folder to remove from the index database.")
    parser.add_argument("--print", action = "store_true", help = "Print current saved documents in the index.")
    parser.add_argument("--text_size", type = int, help = "Length of the document(s) returned.")
    parser.add_argument("-s", action = "store_true", help = "Search in the document and print the returned result.")
    parser.add_argument("--no_retrain", action = "store_true", help = "Skips retraining the index on new data, which may result in suboptimal search results.")
    parser.add_argument("--save", action = "store_true", help = "Save the latest documents displayed into a file at Documents")
    parser.add_argument("--save_file", type = str, help = "The name of the file to be saved.")
    args = parser.parse_args()

    current_file_path = os.path.join(os.getcwd().split("src")[0], "data", "current_file.txt")

    new = False
    if args.file and not args.init: 
        with open(current_file_path, "w", encoding="utf-8") as f:
            f.write(args.file)
            new = True

    elif args.file and args.init: current_file = args.file

    else:
        with open(current_file_path, "r", encoding="utf-8") as f:
            current_file = f.read()

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
                if new:
                    all_text = []
                    for file in os.listdir(current_file):
                        file_path = os.path.join(current_file, file)

                        with open(file_path, "r", encoding = "utf-8") as f:
                            text = [line.strip() for line in f.read()]
                            all_text.extend(text)

                    all_text = "\n".join(all_text)

                else: all_text = None

                document_name = current_file.split("/")[-1].split(".")[0]
                
                inference(query = args.query, text = all_text, document_name = document_name, k = args.k, retrain = not args.no_retrain)

    if args.init:
        if not os.path.exists(rag_dir):
            print("Initalizing the application. This may take some time.")

            if args.file:
                initalize(args.file)
                if current_file.startswith('http'):
                    document_name = current_file.split("/")[-1].split(".")[0]
                    current_file = os.path.join(rag_dir, document_name)

                with open(current_file_path, "w", encoding="utf-8") as f:
                    f.write(current_file)

                    print("Saved the latest file given.")

            else:
                print("No file provided for initalization.")
        else:
            print("The embedding similarity has already been intialized.")


if __name__ == "__main__":
    main()