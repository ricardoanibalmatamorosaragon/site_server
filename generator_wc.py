import sys
import subprocess

# implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'lxml'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PySimpleGUI'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'wordcloud'])
#https://my.customscoop.com/reports/viewclips/reportview.cfm?clipReportTemplateId=24&savedNewsletterName=&savedNewsletterDescription=&start=06%2F01%2F20&daySpan=&end=07%2F01%2F20&hourSpan=&kwid=363205&kwid=361303&kwid=363976&kwid=363975&kwid=361298&kwid=361299&kwid=361300&kwid=361301&ClipRatingList=182055&HeadlineText=&OrderBy=time&maxResults=&CompeteGreater=&CompeteLess=&alexaGreater=&alexaLess=&clipSearchCirculationSelect=-1&circulationGreater=&circulationLess=&autotaguserfolderid=&nowait=1
import requests
import lxml.html as lh
import pandas as pd
import time
import lxml.etree as etree
import re
import glob, os, os.path
from bs4 import BeautifulSoup
from collections import Counter
import numpy as np
import itertools
import ast
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from bs4 import BeautifulSoup

def read_stop_words():
  with open("./temp/stop_word.txt", encoding="utf-8") as f:
    stop_words = list(set([line.rstrip('\n') for line in f]))

  file = open('./temp/stop_word_en.txt',mode='r')
  
  # read all lines at once
  list_stop_words = file.read()
  
  # close the file
  file.close()
  stop_words_en = ast.literal_eval(list_stop_words)
  stop_words += stop_words_en
  return stop_words

def preprocessing(text, stop_words):
  text = text.lower()
  text = re.sub(r'\d+', '', text)
  text = text.replace(',' , ' ')
  text = text.replace('-' , ' ')
  text = text.replace("'" , ' ')
  text = text.translate(str.maketrans('', '', string.punctuation))
  text = text.strip()
  tokenizer = RegexpTokenizer('\w+|\$[\d]+|\w+')
  tokenization = tokenizer.tokenize(text)
  text = [i for i in tokenization if not i in stop_words]
  #return " ".join(text)
  return text


def scrapper_page(url):
  # Start the session
  login_url = 'https://my.customscoop.com/'
  session = requests.Session()

  # Create the payload
  payload = {'Username':'info@davidegreco.it', 
            'Password':'Stracchino53444'
          }

  # Post the payload to the site to log in
  login_session = session.post(login_url, data=payload)
  s = session.get(url)
  soup = BeautifulSoup(s.text, 'html.parser')
  #page = open(url)
  #soup = BeautifulSoup(page.read())
  links = soup.find('ul', {"id": "allResults"})
  rate_values = []
  href_list = []
  dict_links = {}
  for li in links.findAll('li'):
    rate = [item.get_text() for item in li.select("span.currentRatingText")]
    if rate != []:
      rate_value = " ".join(rate[0].split())
      rate_values.append(rate_value)
      dict_links[rate_value] = []

    else:
      rate_values.append("")
    div = li.findAll("div", {"class": "hideExtraIfTooBig headlineContainer"})
    if div != []:
      link = div[0].findAll('a')[0].get('href')
      href_list.append(link)
    else:
      href_list.append("")

  rate_values = rate_values[2:]
  href_list = href_list[1:-1]
  dict_frame = {}
  for index in range(len(rate_values)):
    if rate_values[index] != "":
      dict_links[rate_values[index]].append(href_list[index])
      dict_frame[href_list[index]] = rate_values[index]
  #data = pd.DataFrame(dict_frame.items(), columns=['link', 'rate'])
  #data.to_csv(url+".csv")
  if 'Unrated' in dict_links.keys():
    del dict_links['Unrated']
  return dict_links
  
def save_file(file, current_url):
	#print("ok")
	name = re.sub(r"[^a-zA-Z0-9]+", '', str(file[0]))

	with open(current_url+"/"+name+'.txt', 'w', encoding="utf-8") as f:
		for item in file:
			try:
				f.write(item+"\n")
			except IOError:
				print("line not allowed") 
	f.close()
  
def scrapper_sites(url, current_url):
  links_site = list(scrapper_page(url).values())[0]
  texts = []
  count = 1
  for sito in links_site:
    session = requests.Session()
    s = session.get(sito)
    soup = BeautifulSoup(s.text, 'html.parser')
    title = [soup.title.string]
    titles = title #+ [item.string for item in soup.find_all('h1')]
    text = [item.string for item in soup.find_all('p')]
    #if titles != [] and text != [] and titles[0] != None and text[0] != None :

    if titles != []:
      print("scrapper site "+ str(count))
      count += 1
      element = titles+text
      element = [x for x in element if x is not None]
      texts.append(" ".join(element))
      save_file(element, current_url)
  return texts

def create_word_cloud(texts, name_wc, number_words= 200):
  stop_words = read_stop_words()
  processed_texts = []
  for text in texts:
    processed_texts.append(preprocessing(text, stop_words))

  merge_texts = list(itertools.chain.from_iterable(processed_texts))
  #print(merge_texts)
  
  #save words
  with open('./temp/temp_words.txt', 'w') as f:
    for item in merge_texts:
        f.write("%s\n" % item)
		
		
  wordcloud = WordCloud(width=1600, height=800, background_color ='white', max_words=number_words, prefer_horizontal=1, #mask=image , #colormap=cmap,
                contour_width=2, contour_color='black',min_font_size = 10).generate(' '.join(merge_texts))
  #wordcloud.recolor(color_func = grey_color_func)
  plt.figure(figsize=(20,10), facecolor = None)
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  #plt.show()
  plt.savefig('./wordClouds/'+name_wc+'.png')
  
def update_wc(name_wc):
	with open("delete_words.txt") as f:
		delete_words = list(set([line.rstrip('\n') for line in f]))
	f.close()
	
	with open("./temp/temp_words.txt") as f:
		words_wc = [line.rstrip('\n') for line in f]
	
	print(len(words_wc))
	print(len(delete_words))
	

	for word in delete_words:
		words_wc = list(filter(lambda a: a != word, words_wc))
	print(len(words_wc))
	wordcloud = WordCloud(width=1600, height=800, background_color ='white', max_words=100, prefer_horizontal=1,
				contour_width=2, contour_color='black',min_font_size = 10).generate(' '.join(words_wc))
	plt.figure(figsize=(20,10), facecolor = None)
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	plt.savefig('./wordClouds/'+name_wc+'.png')
	

def scrapper_main(values):
	ticks = time.time()

	path = os.getcwd()
	#print ("The current working directory is %s" % path)
	print(ticks)
	path += "/sites/" + str(ticks)
	try:
		os.mkdir(path)
	except OSError:
		print ("Creation of the directory %s failed" % path)
	else:
		print ("Successfully created the directory %s " % path)
	current_url = path
	
	texts = scrapper_sites(values[0], current_url)
	create_word_cloud(texts,values[1],100)


layout = [[sg.Text('Insert URL:')],
          [sg.Input(do_not_clear=False)],
		  [sg.Text('Name WC:')],
          [sg.Input(do_not_clear=False)],
          [sg.Button('Start'), sg.Button('Update WC'), sg.Exit()]
          #[sg.Text('Alternatives:')],
          #[sg.Listbox(values=('value1', 'value2', 'value3'), size=(30, 2), key='_LISTBOX_')]
		  ]

window = sg.Window('Scrapper Table', layout)

while True:
	event, values = window.Read()
	print(event, values)
	if event is None or event == 'Exit':
		if os.path.isfile('./temp/temp_words.txt'):
			os.remove("./temp/temp_words.txt")
		break
	if event == 'Start':
		if values[0] != '' and values[1] != '':
			#print(values)
			scrapper_main(values)
			print('finish')
	if event == 'Update WC':
		if values[1] != '' and os.path.isfile('./temp/temp_words.txt'):
			update_wc(values[1])
			print("finish")
			
			
window.Close()