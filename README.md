# Table of Contents
- [Project Objectives](#Objectives)
- [Set-up](#Set-up)
- [Methodology](#Methodology)
- [Future development](#Future-development)
- [References](#references)

# Objectives

- Question answering chatbot about undergrad courses in UCD, Trinity College Dublin and Dublin City University. MVP version has just Maths courses and all variants of maths but we hope to expand both the number of courses and universities in the knowledge base.
- Usually students are comparing courses within universities, so we want to architect it with this in mind
    - Perform a write-up below on this point where we give an example, like 'what is the focus on applied versus theoretical maths in the courses between UCD and Trinity College?'

## Technical objectives
- Build an information retrieval system leveraging a lightweight LLM separate from the main 'chatbot' acting as an intermediary to retrieve information. This lightweight LLM which can receive conversational context and pose information requests to the information store, the results of which requests can inform the main chatbot's response.
- Balance the development to make its set-up friendly to development locally on an Apple product to leverage the use of Apple Silicon. Due to this limitation the low latency of a response is a factor not a primary aim.

# Set-up

## Requirements
- MAC with Apple Silicon and macOS 12.6 or greater
- Docker
- Python3 installed

## Docker

Download Docker image [here](https://github.com/pgvector/pgvector#docker)

Start container 
```bash
docker run -d -p 5432:5432 --name course_vectordb -e POSTGRES_PASSWORD=<<enter_password>> pgvector/pgvector:pg17
```
This command returns the container_id, we will take this and run 'docker run <<container_id>>

## Embedding model: BERT

Download bert-base-uncased weights to the llm/embed/weights folder

Then run command:
```bash
python convert.py \
    --bert-model bert-base-uncased \
    --mlx-model weights/bert-base-uncased.npz
```
## Lightweight LLM: TinyLlama

- First download weights from HF into the hf_model dir. The weights are accessible here https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Move the files downloaded to llm/llama/hf_model
- From llm/llama run command python3 convert.py --torch-path /hf_model --model-name tiny_llama
This will populate the mlx_model folder with the weights which can be used with mlx

## Config
- Add a `config.json` file to the root folder of the project like as follows, populating the valules as necessary:
```bash
{
    "project_path": "", // to add
    "dbname": "postgres",
    "user": "", // to add
    "password": "", // to add
    "host": "", // to add
    "port": // to add
}
```

# Methodology
- This is an MVP implementation and subject to change in the Roadmap section

1. Scrape information online from source of truth
    - At this early stage of the project we target university websites with fixed HTML formats between pages of different courses. BeautifulSoup is preferred as it is lightweight framework but where interaction is needed we use Selenium
2. Data processing
    - Data is de-duplicated and cleaned of ASCII character
    - Data is chunked using natural breakpoints inherent to the Web text it came from
    - No chunk is greater than 512 tokens - the context of BERT which we use for embeddings
3. Information Store - Vector Database
    - Postgres used with 
4. Information Retrieval LLM
    - TinyLlama used. Same architecture as Llama. 1.1bn parameters and trained on 3 trillion tokens. Context window length of 2048 tokens. Achieved 16/tokens per second on Mac with 8GB RAM.

# Future development
1. Scrape information online from source of truth
- Scrape information from an increasing number of sources
- Scrape data for an increasing number of courses and universities
2. Data processing
- The increased number of sources will require additional chunking techniques
3. Information store
- Add tables for departments as well as courses
4. Information Retrieval LLM
- Fine-tuning of TinyLlama and quantization to improve latency. Implement speculative decoding.

# References
MLX code in `llm/` folder lent from [here](https://github.com/ml-explore/mlx-examples/tree/main)