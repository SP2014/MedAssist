import os
from icrawler.builtin import GoogleImageCrawler
path = 'D:\\Internship\\Image Dataset\\'
with open('skin_diseases.txt','r') as fp:
    for name in fp:
        os.mkdir(path+name.strip())
        google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4,
                                    storage={'root_dir': path+name.strip()+'\\'})
        google_crawler.crawl(keyword=name.strip(), max_num=1000,
                     date_min=None, date_max=None,
                     min_size=(200,200), max_size=None)
