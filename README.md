# Table of Contents
- [Project Objectives](#Objectives)
- [Set-up](#Set-up)
- [Methodology](#Methodology)
- [Future development](#Future-development)
- [References](#references)

# Objectives

- Develop a question-answering chatbot focused on undergraduate courses at UCD, Trinity College Dublin, and Dublin City University. The current MVP covers only Maths courses and their variants, but the goal is to expand both the range of courses and universities included in the knowledge base.
- As students often compare courses within and across universities, the system should be designed with these comparative queries in mind. For example, it should excel at answering questions like, "What is the focus on applied versus theoretical maths between UCD and Trinity College courses?".

## Technical objectives
- Build an information retrieval system using a lightweight LLM that acts as an intermediary between the main chatbot and the information store. This lightweight LLM will receive conversational context, retrieve relevant information, and help inform the chatbot's responses.
- Optimize the development process to ensure it can be done efficiently on Apple devices, leveraging Apple Silicon. While low latency is important, it is not the primary goal due to these technical constraints.

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