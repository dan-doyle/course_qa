import requests
from bs4 import BeautifulSoup

def extract_headers_and_text(url, output_file):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.content, 'html.parser')

    headers = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs = soup.find_all('p')

    with open(output_file, 'a', encoding='utf-8') as file:
        for header in headers:
            file.write(f"Header: {header.get_text(strip=True)}\n")
            
            next_elem = header.find_next_sibling()
            while next_elem and next_elem.name not in ['p', 'ul', 'ol']:
                next_elem = next_elem.find_next_sibling()
            
            if next_elem and next_elem.name == 'p':
                file.write(f"Text: {next_elem.get_text(strip=True)}\n")
            
            elif next_elem and next_elem.name in ['ul', 'ol']:
                file.write("List:\n")
                list_items = next_elem.find_all('li')
                for li in list_items:
                    file.write(f" - {li.get_text(strip=True)}\n")
            
            file.write("\n")

def process_urls(url_list, output_file):
    for url in url_list:
        extract_headers_and_text(url, output_file)        

if __name__ == '__main__':
    url_list = ['https://www.tcd.ie/courses/undergraduate/courses/mathematics/', 'https://www.maths.tcd.ie/undergraduate/mod-mathematics/']
    
    output_file = 'Pure Mathematics.txt'
    
    process_urls(url_list, output_file)