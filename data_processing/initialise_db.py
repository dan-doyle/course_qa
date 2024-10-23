from utils.create_dataframe import create_dataframe
import mlx.core as mx
import numpy as np
from llm.embed.model import Bert, load_model
from llm.embed.embed import get_token_length, embed
from data_processing.utils.embed_dataframe import embed_dataframe
import psycopg
import json
import os

if __name__ == '__main__':
    TESTING = True

    if TESTING:
        # Example resource catalog structure
        resource_catalog = {
            'university': 'UCD',
            'courses': {
                    'Applied & Computational Mathematics': [
                        'https://hub.ucd.ie/usis/!W_HU_MENU.P_PUBLISH?p_tag=COURSE&MAJR=APS1',
                    ]
                }
        }
    else:
        with open('resource_catalog.json', 'r') as f:
            resource_catalog = json.load(f)

    base_path = '../' # path to root folder

    with open(os.path.join(base_path, 'config.json'), 'r') as f:
        config = json.load(f)

    try:
        with psycopg.connect(dbname=config['dbname'], user=config['user'], password=config['password'], host=config['host'], port=config['port']) as conn:
            print('Connected to the database')
            psycopg.register_vector(conn)

            for university_obj in resource_catalog:
                university = university_obj['university']
                courses = university_obj.get('courses', {})

                for course_name, links in courses.items():
                    course_path = os.path.join(base_path, university, course_name)
                    df = create_dataframe(course_path, links, university, get_token_length)
                    embed_dataframe(df, embed, 4)
                    with conn.cursor() as cur:
                        db_version = cur.fetchone()
                        table_name = f'{university} - {course_name}'
                        table_create_command = """
                        CREATE TABLE {0} (
                                    id bigserial primary key, 
                                    title text,
                                    url text,
                                    content text,
                                    tokens integer,
                                    embedding vector(768)
                                    );
                                    """.format(table_name)

                        cur.execute(table_create_command)
                        cur.close()
                        conn.commit()

                    with conn.cursor() as cur:
                        data_list = [(row['title'], row['url'], row['content'], int(row['tokens']), np.array(row['embeddings'].tolist())) for index, row in df.iterrows()]
                        cur.executemany("INSERT INTO embeddings (title, url, content, tokens, embedding) VALUES %s", data_list)
                        conn.commit()

    except Exception as e:
        print(f"Failed to connect to the database: {e}")