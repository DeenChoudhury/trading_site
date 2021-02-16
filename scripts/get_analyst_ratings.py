from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from argparse import ArgumentParser
from datetime import date,timedelta
import json
import csv, os,re,requests,time,datetime
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from pytz import timezone


COUNTRY = "USA"
cwd = os.getcwd()
FILE_PATH = os.path.join(cwd,"data","Analyst_Ratings")
WATCHLIST_PATH = os.getcwd() + "/data/watchlist.json"

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

parser = ArgumentParser()
parser.add_argument('-d', '--dates', help='add dates', type=str, action='store')
parser.add_argument('-n', '--num', help='add dates', type=int,default=1, action='store')
args = parser.parse_args()

# Parse stock price through webscraping
def get_yahoo_ticker_price(ticker):
	r = requests.get('https://ca.finance.yahoo.com/quote/'+ticker+'?p='+ticker+'')
	soup = bs4.BeautifulSoup(r.text)
	price=soup.find_all('div',class_='My(6px) Pos(r) smartphone_Mt(6px)')[0].find('span').text
	return price

def get_price_from_cell(s):
	replace = ["$",",","C","€","GBX"]
	for ch in replace:
		s = re.split('\\+|-',s)[0].replace(ch,"")
		
	try:
		return float(s)
	except:
		return ""
# Get percentage change from current price to target price
def get_percentage_diff(s1,s2):
	if not s1 or not s2 or s1 == "" or s2 == "":
		return 0
	n1 = float(s1)
	n2 = float(s2)
	percentage = int(((n2-n1)/n1)*100)
	return percentage

def email_excel(file_paths):
	today = datetime.date.today().strftime("%m-%d-%Y")
	file_path = os.path.join(FILE_PATH,"XLSX",''+today+'_analyst_opinions.xlsx')
	email_abba = "taffikc@traxionsp.com"
	email_deen = "deen.r.choudhury@gmail.com"
	Email.send_email_attachment(email_deen,"Deen's Daily Excel Sheet", "Here's my daily excel sheet :) - Deen",[file_path])
	Email.send_email_attachment(email_abba,"Deen's Daily Excel Sheet", "Here's my daily excel sheet :) - Deen",[file_path])
	return

#Returns a BeautifulSoup object of specified page
def get_table_data(country, date):
	print("Opening driver for " + date)
	COUNTRY = {"USA": "1", "Canada":"2"}

	#Heroku Chrome Driver
	chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', "chromedriver")
	options = webdriver.ChromeOptions()
	options.binary_location = chrome_bin
	options.add_argument("--disable-gpu")
	options.add_argument("--no-sandbox")
	options.add_argument('headless')
	chrome_options.add_argument('--disable-dev-shm-usage') 
	driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
	
	# Local driver to automate webscraping
	# options = Options()	
	# options.add_argument("--headless")
	# options.add_experimental_option('excludeSwitches', ['enable-logging'])
	# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	
		
	driver.get("https://www.marketbeat.com/ratings/")
	wait = WebDriverWait(driver, 20)

	# Choose USA Sector in MarketBeat
	javaScript = "var element = document.getElementsByName('ctl00$cphPrimaryContent$ddlCountry')[0];\
	              element.selectedIndex="+COUNTRY[country]+";                                \
	              var event = new Event('change'); \
	              element.dispatchEvent(event);"
	driver.execute_script(javaScript)
	time.sleep(5)

	inputElement = driver.find_element_by_id('cphPrimaryContent_txtStartDate')
	inputElement.clear()
	inputElement.send_keys(date)
	inputElement.send_keys(Keys.ENTER)

	time.sleep(2)

	# Setup BeautifulSoup object
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	
	driver.quit()

	return soup

#params: soup object
#return: DataFrame object
def table_rows_to_df(rows):
	data = {"date":[],"ticker":[],"company":[],"action":[],"brokerage":[],"current":[],"target_original":[],
			"target_new":[],"rating":[],"impact":[],"percent_upside":[]}
	for r in rows:
		#Add to excel data
		print(r["date"])
		data["date"].append(r["date"])
		data["ticker"].append(r["ticker"])
		data["company"].append(r["company"])
		data["action"].append(r["action"])
		data["brokerage"].append(r["brokerage"])
		data["current"].append(r["current"])
		data["target_original"].append(r["target_original"])
		data["target_new"].append(r["target_new"])
		data["rating"].append(r["rating"])
		data["impact"].append(r["impact"])
		data["percent_upside"].append(r["percent_upside"])
	df =  pd.DataFrame(data=data)
	return df

def get_table_rows(soup):
	ratings = []

	# Get date
	title = soup.find(id="cphPageTitle_pnlTwo").get_text()
	text = re.search('(\d{1,2}\/\d{1,2}\/\d{4})',title)
	date = text.group(1)

	# Parse through html to filter data
	table = soup.find(class_ = "scroll-table")
	rows = table.find_all("tr")
	for row in rows:
		td = row.find_all("td")
		if len(td) > 5:
			target_new,target_orig = 0,0

			ticker = td[0].find(class_ = "ticker-area").get_text()
			company = td[0].find(class_ ="title-area").get_text()
			action = td[1].get_text()
			brokerage = td[2].get_text()
			current_price = get_price_from_cell(td[3].get_text())

			#Get lower bound of price range
			price_target = td[4].get_text()
			if price_target:
				prices = price_target.split("➝")
				if len(prices) == 1:
					target_new = get_price_from_cell(prices[0])
				elif len(prices) == 2:
					target_orig = get_price_from_cell(prices[0])
					target_new = get_price_from_cell(prices[1])

			rating = td[5].get_text()
			impact = td[6].get_text()
			diff = get_percentage_diff(current_price,target_new)
			ratings.append({"date":date,"ticker":ticker,"company":company,"action":action,"brokerage":brokerage,"current":current_price,"target_original":target_orig,
				"target_new":target_new,"rating":rating,"impact":impact,"percent_upside":diff})
	return ratings


def main():
	start_time = datetime.datetime.now()

	num_days = args.num
	rows = []
	for i in range(0,num_days):
		eastern = timezone('US/Eastern')
		date = (datetime.datetime.now(eastern)-timedelta(days=i)).strftime("%m/%d/%Y")
		soup = get_table_data(COUNTRY,date)
		data = get_table_rows(soup)

		
		# rows = rows + data
		rows = data
		df = table_rows_to_df(rows)
		sorted_df = df.sort_values(by=['percent_upside'], ascending=False)
		post_data = json.dumps(sorted_df.to_dict(orient='records'))
		print(post_data)
		# r = requests.post('http://127.0.0.1:8000/api/ratings/', json=post_data)
		r = requests.post('http://www.deentheredonethat.com/api/ratings/', json=post_data)
		print(r.status_code)


	print("Total Elapsed Time: %s" % (datetime.datetime.now() - start_time))

if __name__ == "__main__":
	main()


