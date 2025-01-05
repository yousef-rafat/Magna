![MAGNA](https://github.com/user-attachments/assets/34cd566c-4896-4760-a148-ed54bed67936)

Magna uses Embedding Similarity Search, a technique commonly utilized in large language models (LLMs), to search for text that aligns semantically with the user's query. Unlike traditional text-based search algorithms, embedding similarity search captures the underlying meaning of the text, making it far more effective for retrieving relevant and context-aware results.

Magna can return multiple documents with meanings similar to the query while offering various customization options for tailoring the responses to user needs.

# Features Overview

### 1. Semantic Understanding

Magna understands the meaning behind queries and documents, enabling it to:

- Match semantically similar text, even if the exact words differ.
- Retrieve documents based on intent rather than keyword matches.

### 2. Customizable Responses

Magna allows users to fine-tune responses with options such as:

- Adjusting the number of documents returned.
- Setting the length of the text content
- Chooses to retrieve from a single file or all of the files uploaded

### 3. Multi-Document Retrieval

Magna supports retrieving multiple documents that are semantically relevant to a single query. This is useful for:

- Comprehensive information retrieval.
- Research and knowledge discovery in complex documents.

# Installation

Install using pip:   
   ```sh
   pip install magna-search==1.0.1
  ```
Alternatively, you can use git and run the Python files locally:
  ```sh
  git clone https://github.com/yousef-rafat/Magna.git
  ```
# User Guide

To start using Magna, you need to initialize Magna and the index by using the command --init with a file
This will install all the required packages (if not installed), initialize the encoding model and the index, and create the data folder.

```sh
magna-search --init --file "C:\User\FilePath"
```

After initialization, you can start to query the current file. Adding a new file to Magna using the --file saves the file path so you won't have to reload it again.
So, we can go ahead with searching:

```sh
magna-search -s --query "[QUREY]"
```
To add a new file, you can use this command:
This will query the latest file you passed. In this case, it will be the file after --file.

```sh
magna-search -s -query "[QUREY]" --file "C:\User\FilePath"
```

There are more options to customize the output from Magna:

#### -all
Whether to query all the documents uploaded or the last file uploaded

#### --text_size and --text_overlap
The first lets you control the size of the documents returned. The other says there is an overlap between the split documents.

#### --save
While querying in the files, you can choose to save the results of the query.

#### --save_file
Let's choose the file name that saves the query results.

#### --print
Prints the current files saved in the index

#### --remove
Let's you remove files from the index

#### --search_files
Search for supported files (PDF, DOXC, TXT) in the Download and Documents folders.

#### --filetypes
To specify the file types that can be searched for. It will search for all PDF, DOXC, and TXT files if not used.

#### --no_retrain
To whether to retrain the index on the new data or not. 

#### -k
Determines the number of documents to return from the saved documents (split files)

## License
Magna Search is under MIT License
 
