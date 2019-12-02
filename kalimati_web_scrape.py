# Import Libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime
import urllib.request
import pandas as pd
from selenium.webdriver.support.select import Select
import csv
import utils
import numpy as np
import time
## Variable Assign
price_type = "R" # R = Retail, W = Wholesale
start_date = "12/01/2018"
end_date = "12/31/2018"
urlpage = "http://kalimatimarket.gov.np/daily-price-information"

# Initialization
date_list = []

# Date Generator
start = datetime.datetime.strptime(start_date, "%m/%d/%Y")
end = datetime.datetime.strptime(end_date, "%m/%d/%Y")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    date_list.append(date.strftime("%m/%d/%Y"))
date_list.append(end_date)


# Query the website and run the html to the variable "page"
page = urllib.request.urlopen(urlpage)

# Parse the html using Beautiful Soup and Store in variable Soup
soup = BeautifulSoup(page, 'html.parser')

# Find the DatePicker Input
date = soup.find("input", id="datepicker", attrs={'name': "date"})
viewButton = soup.find("input", attrs={'type': 'button', "name":"view"})

# Run Chromium Browser
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
# Get webpage
driver.get("http://kalimatimarket.gov.np/home/language/EN")
driver.get(urlpage)

def extractData():
	# Extract from the HTML Table data.
	table_rows = driver.find_elements_by_xpath("//div[contains(@id, 'pricelist')]/center/table/tbody/tr/td/table/tbody/tr")
	
	row_array = np.array(table_rows)

	data = []
	for each_row in row_array:
		data.append(each_row.text)
	data_array = np.array(data[3:])
	
	data_splited = []
	for j in range(len(data_array)):
		data_splited.append(data_array[j].split(' '))

	def correct_data(table_row):
		""" 
			This function Concatenates the Product Name into Single String.
			THis is done, so that product name is aligned in a single column.
		"""
		table_with_name = ''
		table_with_price = []
		first_element_array = []
		if len(data_splited[1]) > 5:
		#     table_with_price = table_row[:-4] + table_row[-4:]
			for i in range(len(table_row) - len(table_row[-4:])):
		    		table_with_name += table_row[i] + " "
			first_element_array.insert(0, table_with_name)
			table_with_price = first_element_array + table_row[-4:]
		else:
			table_with_price = table_row
		return table_with_price

	final_data = []
	for k in range(len(data_splited)):
		final_data.append(correct_data(data_splited[k]))

	return final_data



for i in range(len(date_list)):

	# Insert the Custom date to Date Picker INPUT
	datepicker = driver.find_element_by_xpath("//input[contains(@id, 'datepicker')]")
	driver.execute_script("arguments[0].value = '"+date_list[i]+"';", datepicker)

	# Select pricetype
	select = Select(driver.find_element_by_id("pricetype"))
	select.select_by_value(price_type)

	# Click the View option after inserting Date
	view_button = driver.find_element_by_xpath("//input[contains(@name, 'view')]")
	driver.execute_script("arguments[0].click();",view_button)

	time.sleep(5)

	final_data = extractData()

	time.sleep(3)
	# Create Pandas Dataframe
	df = pd.DataFrame(final_data, columns =["Product", "Unit", "Minimum", "Maximum", "Average"])
	export_df = df.to_csv("./source/kalimati/retail/2018/Dec/"+date_list[i].replace('/', '-')+".csv", index = None, header=True)
	time.sleep(3)



