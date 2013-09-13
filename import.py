from mailme.collector.importer import FeedImporter

importer = FeedImporter()
feed = importer.import_feed('http://ikhaya.ubuntuusers.de/feeds/title/20/')

print(feed)
