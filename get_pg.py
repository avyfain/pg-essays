from bs4 import BeautifulSoup
import requests

def get_essay_links():
	url   = 'http://paulgraham.com/articles.html'
	r     = requests.get(url)
	html  = r.content
	soup  = BeautifulSoup(html)
	main  = soup.find_all('td')[2]
	l_tab = main.find_all('table')[1]
	links = l_tab.find_all('a')

	return links


def main():
	links = get_essay_links()
	for link in links:
		print link

if __name__ == '__main__':
	main()