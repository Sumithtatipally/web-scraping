from bs4 import BeautifulSoup
import pandas as pd
import os
import requests

cityList = []


with open('swig.csv','w') as file:
	page = requests.get("https://www.swiggy.com/hyderabad/offers-near-you-collection")
	print(page.content)
	soup = BeautifulSoup(page.content, 'html.parser')
	seven_day = soup.find(id="city-links")
	forecast_items = seven_day.find_all(class_="_2JILy")
	for eachCity in forecast_items:
		city = eachCity.find(class_="_3TjLz b-Hy9").text
		file.write(city)
		file.write('\n')
		# print(city)
