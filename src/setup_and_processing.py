from text_processing import get_text_from_docx, get_pdf_text, read_text_file
from embedding_training import docs_cache
import subprocess
import shutil
import sys
import os

def install_required_packages():
    """Installs required packages using pip."""
    packages = [
        "PyMuPDF",
        "requests",
        "faiss-cpu",
        "sentence_transformers",
        "python-docx"
    ]

    # Create the pip install command
    command = [sys.executable, "-m", "pip", "install", "--user", *packages]

    try:
        # Execute the pip install command
        subprocess.check_call(command)
        print("All required packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing packages: {e}")


def check_file_type(file_path):
    """Checks the file type based on its extension and returns the type."""
    # Get the file extension (lowercased for case-insensitivity)
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    
    # Check the file extension and return the corresponding file type
    if file_extension == ".txt":
        return "Text file"
    elif file_extension == ".pdf":
        return "PDF file"
    elif file_extension == ".docx":
        return "DOCX file"
    else:
        print("Unknown File Type. Please choose a file with: .pdf, .doxc, .txt\n")
        return "Unknown file type"

def get_text(file_path):
    file_type = check_file_type(file_path)
    
    match file_type:
        case "DOCX file":
            text = get_text_from_docx(file_path)
        case "PDF file":
            text = get_pdf_text(file_path)
        case "Text file":
            text = read_text_file(file_path)
        case "Unknown file type":
            print("File type not supported.")
            return None  # Return None if the file type is unsupported
        case _:
            print("Unexpected file type.")
            return None 

    return text

def remove_folder(folder_name: str):

    folder_path = os.path.join(os.getcwd().split("src")[0], "data", folder_name)

    if not os.path.exists(folder_path):
        print(f"Incorrect folder name: '{folder_path}'")
        return

    shutil.rmtree(folder_path)
    print(f"Removed '{folder_path}' from index data.")

def print_saved_documents():
    current_dir = os.path.join(os.getcwd().split("src")[0], "data")

    if os.path.exists(current_dir):

        for folder in os.listdir(current_dir):            
            print(folder)

def save_cached_docs(file_name = "cache.txt"):
    """ Function to save the latest retrived documents """

    folder_path = os.path.join(os.path.expanduser('~'), "Documents")

    if not os.path.exists(folder_path):
        print(f"Folder path doesn't exist: {folder_path}")
        return
    
    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for doc in docs_cache:
                f.write(doc + "\n")
        print(f"Cache successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the cache: {e}")