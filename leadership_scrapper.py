import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
from matplotlib.patches import Polygon
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time
import numpy as np
from scipy import stats
import pandas_ta as ta



def get_symbols(url):

	response = requests.get(url)
	doc = BeautifulSoup(response.text, 'html.parser')
	tableETFs = doc.find_all('td',{'class':'eft_or_etn'})
	symbols = []

	for elem in tableETFs:
		symbols.append(elem.text.split(' ')[-1])

	return symbols

def scrape_data(symbols):
	AllData = pd.DataFrame()
	for ticker in symbols:
		req = Request(url='https://finviz.com/quote.ashx?t={}'.format(ticker),headers={'user-agent':'my-app'})
		try:
			response = urlopen(req)
		except:
			continue

		print(ticker)
		html = BeautifulSoup(response, 'html')
		info_table = html.find_all(class_= "snapshot-table2")
	    
		info_tables = dict()
		info_tables[ticker] = info_table

		ticker_data = info_tables[ticker]

		ticker_rows = [result.findAll('tr') for result in ticker_data]
		ticker_rows_content = [result.findAll('b') for result in ticker_data]

		numbers = [item.text for item in ticker_rows_content[0]]
		numbers = [item.replace('%','') if '%' in item else item for item in numbers]

		data = {}
		x = 0
		for index,row in enumerate(ticker_rows[0]):
			onlyString = ''.join([item for item in row.text if not item.isdigit()])

			cleanOnlyString = onlyString.split("\n")[1:-1]
			cleanOnlyString = [i.replace('%','') if '%' in i else i for i in cleanOnlyString]
			cleanOnlyString = [i.replace('.','') if '.' in i else i for i in cleanOnlyString]
			cleanOnlyString = [i.replace('-','') if '-' in i else i for i in cleanOnlyString]

			count = 0

			for i2,value in enumerate(cleanOnlyString):
				count += 1

				data[value] = numbers[x]

				x += 1

				if count== 6:
					break

		AllData[ticker] = [data['Perf Month'],data['Perf Year'],data['W Low'],data['W High'],data['Price']]
	return (AllData)

def visualize_data(df):

	df = pd.DataFrame(df.T)

	df = df.rename(columns={0:'1 Month Returns', 1:'1 Year Returns', 2:'52 Week Low',3:'52 Week High',4:'Price'})

	df.loc[df['1 Year Returns'] == '-', ['1 Month Returns','1 Year Returns']] = np.nan


	# df = df.drop(df[df['1 Year Returns'] == '-'].index)

	df[['1 Month Returns','1 Year Returns','52 Week Low','52 Week High','Price']] = df[['1 Month Returns','1 Year Returns','52 Week Low','52 Week High','Price']].astype(float)

	noNA_df = df[~np.isnan(df['1 Month Returns'])]
	# print(noNA_df)

	fig, ax = plt.subplots(figsize=(10,6))
	ax.scatter(x = df['52 Week Low'], y = df['52 Week High'])
	# plt.ylim(min(df['52 Week High']), max(df['52 Week High']))
	plt.ylim(min(df['52 Week High']), 0)

	x_ticks = [0,100,150,300]
	x_labels = ['1.0','2.0','2.5','4.0']
	plt.xticks(x_ticks,x_labels)


	ax.add_patch(Polygon([[min(df['52 Week Low']),min(df['52 Week High'])],[min(df['52 Week Low']),0],[112.5,min(df['52 Week High'])]], closed=True,fill=False))


	plt.xlabel('Gain Factor 52 Week Low')
	plt.ylabel('(%) from 52 Week High') # CIBR PSJ SOCL PNQI SKYY AIQ

	for i, txt in enumerate(df.index):
	    ax.annotate(txt, (df['52 Week Low'][i], df['52 Week High'][i]))


	plt.show()




if __name__ == '__main__':
	url = 'https://seekingalpha.com/etfs-and-funds/etf-tables/sectors'
	response = requests.get(url)
	doc = BeautifulSoup(response.text, 'html.parser')
	sidebar = doc.find_all('div',{'class':'united_sidebar'})

	sidebar_categories = []
	paths = list()

	for link in sidebar:
	    sidebar_categories.append(link.text)
	    page = link.find_all('a')
	    for i in page:
	        paths.append(i.get('href'))

	sidebar_categories = sidebar_categories[0].split('\n')
	sidebar_categories = sidebar_categories[2:-2]

	mainMenu = list(zip(sidebar_categories, paths))

	for index, value in enumerate(mainMenu):
	    print(f"{index}: {value[0]}")

	numberSelect = int(input("Select ETF performance data you would like to see the leadership of: "))

	while numberSelect not in range(len(mainMenu)):
	    numberSelect = int(input("Select ETF performance data you would like to see the leadership of: "))

	if numberSelect in range(len(mainMenu)):
	    dataSelected, pathSelected = mainMenu[numberSelect][0], mainMenu[numberSelect][1]
	    
	    print("Selected the following data:",dataSelected)

	urlSelected = 'https://seekingalpha.com'+pathSelected

	symbols = get_symbols(urlSelected)
	visualize_data(scrape_data(symbols))
