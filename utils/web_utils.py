import requests
from bs4 import BeautifulSoup
#import ai_utils
import timeit

import warnings
from urllib3.exceptions import InsecureRequestWarning

# tokens are about 2.5 times longer than the average word

# Suppress InsecureRequestWarning .. this is not recommended. might just use chrome driver instead
warnings.simplefilter('ignore', InsecureRequestWarning)
def count_words(text):
    return len(text.split())

def get_general_content_information(url):
    # Send a GET request to the URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers, verify=False)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get the page title
        page_title = soup.title.text        
        # Get the page's body content
        body = soup.body

        paragraphs = body.find_all(['p', 'div'], recursive=False)

        page_body = "\n".join([p.get_text(strip=True) for p in paragraphs])

        

        
        #split text by word
        words = page_body.split()
        word_count = len(words)

        # Calculate the desired group size
        group_size = int((word_count * 3) / 4000)

        if group_size == 0:
            group_size = 1
        
        words_per_group = word_count // group_size

        grouped_words = [" ".join(words[i * words_per_group:(i + 1) * words_per_group]) for i in range(group_size)]

        print(group_size,len(grouped_words))

        with open('scrape_result.txt', 'w', encoding='utf-8') as file:
            file.write(grouped_words[0])
        
        #print(f"Word count: {}")

        return f'Title: {page_title} : Body: {grouped_words[0]}'
    else:
        return(f"Failed to fetch the URL. Status code: {response.status_code}. I probably cant read it because im scraping it and it might not allow scrapers.")


