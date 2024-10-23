def retrieve_similar(query_embedding, database_name, conn):
    with conn.cursor() as cur:
        cur.execute("SELECT content FROM {0} ORDER BY embedding <=> %s LIMIT 1".format(database_name), (query_embedding.tolist(),))
        most_relevant_doc = cur.fetchall()
    
    return most_relevant_doc