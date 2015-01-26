from bs4 import BeautifulSoup
import requests
import csv

class Essay: 
	def __init__(self, essay):
		self.name = essay.text
		self.url = 'http://paulgraham.com/' + essay.attrs['href']
		self.set_content()
		self.set_date()
		self.set_thanks()


	def set_content(self):
		soup = get_html(self.url)
		text = soup.find('font').text.split('\n\n')
		self.content = [l.replace('\n',' ') for l in text]

		for script in soup("script"):
			script.extract()

		stuff = soup.findAll(text=True)
		self.clean_content = filter(lambda x: x not in [u' ', u'\n'], stuff)
		self.clean_content = ''.join(self.clean_content).strip()

	def set_date(self):
		string = self.clean_content
		new_line_ind = string.index('\n')
		date_ind = string[0:new_line_ind].rfind('>') + 2
		if string[date_ind] == 'W':
			date_ind += 55
			string = string[date_ind:].strip()
			new_line_ind = string.index('\n')
			date_ind = 0
		self.date = string[date_ind:new_line_ind]

	def set_thanks(self):
		thx = "Thanks to "
		try:
			thanks_ind = self.clean_content.rindex(thx) + len(thx)
			thanks_string = self.clean_content[thanks_ind:].replace('\n', ' ')
			self.thanks_string = thanks_string.encode('utf-8')
		except:
			self.thanks_string = 'failed'

def get_html(url):
	r     = requests.get(url)
	html  = r.content
	html = html.replace('</br>','\n')
	html = html.replace('<br>','\n')
	html = html.replace('</br>','\n')
	soup  = BeautifulSoup(html)
	return soup


def get_essay_links():
	url   = 'http://paulgraham.com/articles.html'
	soup  = get_html(url)
	main  = soup.find_all('td')[2]
	l_tab = main.find_all('table')[1]
	links = l_tab.find_all('a')
	links = [link for link in links if not link.attrs['href'].startswith('http')]
	return links

def main():
	links = get_essay_links()
	with open('essays.csv', "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		for link in links:
			e = Essay(link)
			print e.name
			line = [e.name, e.url, e.date, e.thanks_string]
			writer.writerow(line)
		

if __name__ == '__main__':
	main()