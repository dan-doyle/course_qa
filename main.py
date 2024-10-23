from transformers import AutoTokenizer
from llm.llama.llama import load_model, generate
from llm.embed.embed import embed as create_embeddings
from vectorDb.query import retrieve_similar as queryVectorDb
from prompt.utils import extract_course_request_pairs
import psycopg
import json
import os

"""
This file presents the MVP functionality to pass a user's question to a small llm, in this case TinyLlama, which then sends requests to a vector database for information retrieval
"""

courses_supported = []
with open('resource_catalog.json', 'r') as f:
    resource_catalog = json.load(f)
    for index, university in enumerate(resource_catalog):
        for course in resource_catalog[index].keys():
            courses_supported.append(f'{university} - {course}')

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    project_path = config.get('project_path', '')
    if not project_path:
        raise ValueError("Model path not specified in config file.")
    model_path = os.path.join(project_path, '/llm/llama')

    hfTokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    upstream_user_query = 'Would studying Mathematics at Trinity College offer more pure theory than doing so at University College Dublin?'
    
    messages = [
        {
            "role": "system",
            "content": "You are a diligent career counsellor and must gather information relevant to the user",
        },
        {"role": "user", "content": "{0} \n\n Given the above comment from the user please extract some succinct requests for information in the following format: <course></course> <request></request>. For instance if the comment is 'How many years is the Geography program in UCD versus TCD?' we will query for the following information \n <course>UCD - Geography</course> <request>Number of years</request> \n <course>UCD - Geography</course> <request>Number of years</request>. Please provide no more than 2 requests. Here are the courses we support: {1}".format(upstream_user_query, courses_supported.join('\n'))},
    ]
    prompt = hfTokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    llm, llmTokenizer = load_model(model_path)
    llm_output = generate(llm, prompt)

    dbQueries = extract_course_request_pairs(llm_output) # pairs of (database_name, query)

    embs = create_embeddings([q[1] for q in dbQueries])
    dbResults = []

    try:
        with psycopg.connect(dbname=config['dbname'], user=config['user'], password=config['password'], host=config['host'], port=config['port']) as conn:
            psycopg.register_vector(conn)

            for index, q in enumerate(dbQueries):
                dbResults = queryVectorDb(embs[index], dbQueries[index][0], conn)

    except Exception as e:
        print(f"Failed to connect to the database: {e}")

    print('Our vector database searches and results are as follows:')
    print('\n---------------------------\n')
    for index, (query, result) in enumerate(zip(dbQueries, dbResults)):
        print('Query:\n', query)
        print('Result:\n', result)
        print('\n---------------------------\n')