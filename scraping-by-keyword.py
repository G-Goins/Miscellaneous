from googlesearch import search
from bs4 import BeautifulSoup
import requests

#Keyword to search for
keyword = "Nintendo Switch"

#Number of search results to scrape
num_results = 5

def scrape_news(keyword):
    search_results = search(keyword, num_results = num_results)

    for url in search_results:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            #Find and extract relevant news articles containing the keyword
            articles = soup.find_all('article')

            for article in articles:
                title = article.find('h2').text
                content = article.find('p').text

                #Check if the keyword is present in the title or content
                if keyword in title or keyword in content:
                    print(f"Title: {title}")
                    print(f"Content: {content}")
                    print(f"Source: {url}\n")
        except requests.exceptions.RequestException as e:
            print(f"Error scraping {url}: {str(e)}")

#if __name__ == "__main__":
scrape_news(keyword)