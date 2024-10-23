import json
import psycopg

with open('../config.json', 'r') as f:
    config = json.load(f)

try:
    with psycopg.connect(dbname=config['dbname'], user=config['user'], password=config['password'], host=config['host'], port=config['port']) as conn:
        print('Connected to the database')
        
        with conn.cursor() as cur:            
            cur.execute("SELECT version();")
            db_version = cur.fetchone()

            print(f"Connection successful: {db_version[0]}")

except Exception as e:
    print(f"Failed to connect to the database: {e}")
