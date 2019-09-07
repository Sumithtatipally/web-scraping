import urllib.request
# open a connection to a URL using urllib
for i in range(20):
	webUrl  = urllib.request.urlopen('https://www.swiggy.com/hyderabad?page=(i+1)')
	fileType = "txt"
	data = webUrl.read()
	fileName = str(i)+''+'swig.'+fileType
	f= open(fileName,"wb")
	f.write(data)
	f.close()
#get the result code and print it
print ("result code: " + str(webUrl.getcode()))

# read the data from the URL and print it
data = webUrl.read()
f= open("scrape.txt","wb")
f.write(data)
f.close()
print(data)