import feedparser
from pymongo import MongoClient
from BeautifulSoup import BeautifulSoup as bs

# set up the mongo client
client = MongoClient()

# get the editors collection
db = client.newosm
collection = db.editors

# import the feed
feed = feedparser.parse('http://resultmaps.neis-one.org/newestosmfeed.php?lon=-111.86427&lat=40.53804&deg=1&user=mvexel')

# upsert the found entries
for entry in feed.entries:
	del entry['updated_parsed']
	result = collection.update({}, entry, True)
	if not result['updatedExisting'] and 'upserted' in result:
		print 'new record added'
	else:
		print 'updated existing record'


for doc in collection.find():
	soup = bs(doc['summary'])
	print soup.a.string

print 'we have %i records now' % (collection.count())
