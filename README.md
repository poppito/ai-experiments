## Prerequisites

- We'll be running our setup on a Mac with HomeBrew installed on your machine
- Python 3.9+
- Ollama installed and Llama3.2 model pulled
- Required Python libraries:
  ```bash
  pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface torch transformers
  ```

## Ollama

Open up your terminal and run:

```
brew install ollama
```

Once installed, start the Ollama service:

```
brew services start ollama
```

## Llama 3.2

**Llama3.2** is Meta’s latest (currently, as of August 2025) and great for general-purpose coding and chat. Handles context well and doesn’t hallucinate as much as earlier versions.


To install Llama3.2:

```
ollama run llama3:2
```

This will pull the model if it doesn't already exist and then run it too.

## Setup

Your setup should look like this:

```markdown
RAG/
├── script.py
├── index_storage/
└── data/
    ├── document1.txt
    └── document2.pdf
```

The top level directory/folder can be whatever you want to call it. As long as you've installed the dependencies above, you can plonk the script below into the root of the folder. The `data` directory is where the script reads any text formatted data from to create the embeddings. Once the script is run, it will create `index_storage` where the embeddings are stored.


## Preview

