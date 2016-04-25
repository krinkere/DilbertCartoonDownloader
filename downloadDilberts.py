import requests, os, bs4, datetime, sys

# Require the user to provide number of comics to download...
if len(sys.argv) < 2:
    print ('Usage: downloadDilberts.py <number of days>')
    sys.exit()
number_of_days = int(sys.argv[1])
print "About to download {} latest Dilbert comics!".format(number_of_days)

######## Set Up #######
# starting URL
url = 'http://dilbert.com/strip/'

# current time
currtime = datetime.datetime.now()

# Store comics in ./dilbert folder. If does not exists, create it!
directory ='dilbert'
if not os.path.exists(directory):
    os.makedirs(directory)
#######################

for i in range(number_of_days):
    # Construct url for each daily strip. Here we invoke formatter to display date as YYYY-MM-DD
    # So that the url will look something like this: http://dilbert.com/strip/2016-04-25
    downloadurl = url+currtime.strftime('%Y-%m-%d')
    print "Downloading {}".format(downloadurl) 
    # Request the page...
    res = requests.get(downloadurl)
    # Check that we are successful and page was returned (200 status)
    res.raise_for_status()

    # parse returned page into beatifulsoup object for further processing
    soup = bs4.BeautifulSoup(res.text, "lxml")
    
    # Via your favorite tool examine html to figure out where the image is located.
    # I opened Dev tools in Firefox and used Inspect to point at the image to see where it is on the page
    # I noticed that image was inside of img tag with class of img-responsive img-comic
    # Hence I wrote my CSS selector in the following way.
    comicElem = soup.findAll('img', {'class':'img-responsive img-comic'})

    # Check if we were able to find the comic...
    if comicElem == []:
        print "Could not find comic..."
    else:
        # Is so, get the src that points to the location of the comic.
        comicUrl = comicElem[0].get('src')
        # Download the image
        res = requests.get(comicUrl)
        res.raise_for_status()

        # Save the image to ./dilbert. Open file in write binary mode
        # Use file name as name it and dont forget to add jpg extension.
        imageFile = open(os.path.join(directory, os.path.basename(comicUrl)+".jpg"), 'wb')

        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Now retrieve previous day comic until you hit the specified number of comics to download.
    currtime -= datetime.timedelta(days=1)

print "Done..."