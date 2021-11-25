import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
from lxml import etree
from lxml import html
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium import *
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt


def main():
	url = 'https://seekingalpha.com/etfs-and-funds/etf-tables/sectors'
	driver = webdriver.Chrome('')
	driver.get(url)
	driver.minimize_window()
	etf_sector = driver.find_elements_by_class_name('theme_sub_links')
	print(etf_sector[0].text)
	answer = str(input("Select ETF performance data you would like to see the leadership of: ")).lower().replace(" ","")
	
	if answer in ('1', 'keymarketetfs','key'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/key_markets',driver))

	elif answer in ('2', 'bondetfs','bond'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/bonds',driver))

	elif answer in ('3', 'commodityetfs','commodity'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/commodities',driver))

	elif answer in ('4','countryetfs','country'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/countries',driver))

	elif answer in ('5','currencyetfs','currency'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/currencies',driver))

	elif answer in ('6', 'dividendetfs','dividend'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/dividends',driver))

	elif answer in ('7','emergingmarketsetfs','emerging'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/emerging_markets',driver))

	elif answer in ('8', 'globalregionaletfs','globalregional'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/global_and_regions',driver))

	elif answer in ('9', 'growthvsvalueetfs','growthvalue'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/growth_vs_value',driver))

	elif answer in ('10', 'marketcapetfs','marketcap'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/market_cap',driver))

	elif answer in ('11', 'realestateetfs','realestate'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/real_estate',driver))

	elif answer in ('12', 'sectoretfs','sector'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/sectors',driver))

	elif answer in ('13', 'etfsstrategies','etfstrats'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/strategies',driver))

	elif answer in ('14', 'smartbetaetfs','smartbeta'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/smart_beta',driver))

	elif answer in ('15', 'themesubsectoretfs','theme'):
		visualize_data(scrape_finviz('https://seekingalpha.com/etfs-and-funds/etf-tables/themes_and_subsectors',driver))
	
	else:
		print("Invalid input, try again later")


def data_select(data):
	result = []

	count = 0
	rule = 3
	for i in range(len(data)-1): 

		count += 1
		

		if rule > 4:
			rule = 4

		if count == rule:
			result.append(data[i-1])
			result.append(data[i])
			count = 0
			rule +=1

	return(result)



def scrape_finviz(url, wb):
	search_url = url
	driver = wb

	driver.get(search_url)
	driver.minimize_window()
	time.sleep(1)

	etfs = driver.find_elements_by_class_name('data_lists_pages_cont_and_ads')
	etfs_names = driver.find_elements_by_class_name('eft_or_etn')
	
	etfs_names = [x.text for x in etfs_names]

	etfs_names_clean = [x for x in etfs_names if 'ETF or ETN' not in x]


	etfs = etfs[0].text.replace("\n"," ")

	clean = [i for i in etfs.split(' ') if '%' in i]

	return_data = data_select([i.replace('%','') for i in clean])


	d = {'ETF': etfs_names_clean, '1 Month': return_data[::2], '1 Year':return_data[1::2]}
	ReturnsDf = pd.DataFrame(data=d)
	ReturnsDf[['1 Month','1 Year']] = ReturnsDf[['1 Month','1 Year']].astype(float)
	ReturnsDf['ETF'] = ReturnsDf['ETF'].astype('string')


	return(ReturnsDf)


def visualize_data(df):
	fig, ax = plt.subplots(figsize=(10,6))
	ax.scatter(x = df['1 Year'], y = df['1 Month'])
	# plt.xlim(min(ReturnsDf['1 Year']), max(ReturnsDf['1 Year']))
	plt.ylim(min(df['1 Month']), max(df['1 Month']))

	plt.xlabel('1 Year Returns (%)')
	plt.ylabel('4 Week Returns (%)')

	for i, txt in enumerate(df['ETF']):
		ax.annotate(txt, (df['1 Year'][i], df['1 Month'][i]))

	plt.show()

	answer = str(input("Would you like to analyze leadership of other ETF data?: ")).lower()

	while answer not in ('y','yes','n','no'):
		answer = str(input("Would you like to analyze leadership of other ETF data?: ")).lower()
	if answer in ('y','yes'):
		main()
	elif answer in ('n','no'):
		exit()



main()
