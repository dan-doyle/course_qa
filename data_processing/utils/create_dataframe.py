from data_processing.utils.db_chunk_logic import ChunkProcessor, KeywordStrategy
from data_processing.utils.db_clean_logic import CleanFile
import pandas as pd
import os

keyword_dict = {
    'UCD': '[BREAK]',
    'TCD': 'Header:'
}

def create_dataframe(dir_path, url_list, university, get_token_length):
    df = pd.DataFrame(columns=['URL', 'content', 'embedding', 'token_count'])

    for index, url in enumerate(url_list):
        with open(os.path.join(dir_path, '{}.txt'.format(index)), 'r') as file:
            unclean_content = file.read()
            content = CleanFile(unclean_content).clean()

            chunk_iterator = ChunkProcessor(content, KeywordStrategy(get_token_length, keyword_dict[university])).process()

            for chunk in chunk_iterator:
                token_count = get_token_length(chunk)
                new_row = {'URL': url, 'chunk': chunk, 'embedding': None, 'token_count': token_count}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


    return df

if __name__ == '__main__':
    import json
    from llm.embed.embed import get_token_length

    with open('../../config.json', 'r') as f:
        config = json.load(f)

    resource_catalog = [
        {
            'university': 'UCD',
            'courses': {
                    'Applied & Computational Mathematics': [
                        'https://hub.ucd.ie/usis/!W_HU_MENU.P_PUBLISH?p_tag=COURSE&MAJR=APS1',
                    ]
                }
        }
    ]

    df = create_dataframe(os.path.join(config.project_path, '/scraping/scraped_data/UCD/Applied & Computational Mathematics'), resource_catalog[0]['courses']['Applied & Computational Mathematics'], resource_catalog[0]['university'], get_token_length)
    print(df.head(1))