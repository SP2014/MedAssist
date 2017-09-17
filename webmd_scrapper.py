import requests
from bs4 import BeautifulSoup

pages = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
for p in pages:
	with open('D:\\Internship\\Dataset\\webmd_crawl\\'+p+'.txt',r) as fp:
		for links in fp:
			link = links.split('\t')[1]
			page = requests.get(link)
			soup = BeautifulSoup(page.content, 'html.parser')
			try:
				div = soup.find('div',class_='lh_links')
				btn = soup.find('a',class_='button')
				page2 = requests.get(btn.get('href'))
				soup2 = BeautifulSoup(page2.content, 'html.parser')
			except Exception as e:
				pass

			
			
			
			


	''' Download script
	page = requests.get("http://www.webmd.com/a-to-z-guides/health-topics?pg="+p)
	soup = BeautifulSoup(page.content, 'html.parser')
	med_list = soup.find('ul',class_='az-index-results-group-list')
	aa = med_list.find_all('a')
	with open(p+'.txt','w+') as fp:
		for links in aa:
			fp.write(''.join(str(e) for e in links.contents)+'\t'+links.get('href')+'\n')'''
    
