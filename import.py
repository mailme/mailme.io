from mailme.collector.importer import FeedImporter


links = [
    'http://feeds.feedburner.com/alistapart/main',
    'http://feeds.feedburner.com/thechangelog',
    'http://tirania.org/blog/miguel.rss2',
    'https://github.com/blog.atom',
    'http://feeds.feedburner.com/nettuts',
    'http://feeds.feedburner.com/blogspot/MKuf',
    'http://xkcd.com/rss.xml',
    'http://peter.sh/feed/',
    'https://blog.dropbox.com/feed/',
    'http://feeds.feedburner.com/37signals/beMH',
    'http://planet.postgresql.org/rss20.xml',
    'http://planet.python.org/rss10.xml',
    'http://torvalds-family.blogspot.com/feeds/posts/default',
    'http://feeds.feedburner.com/tweetagewasteland',
    'http://feeds.dashes.com/AnilDash',
    'http://www.reddit.com/r/programming/.rss',
    'http://www.osnews.com/files/recent.xml',
    'http://feeds.feedburner.com/TimeToBleed',
    'http://feeds.feedburner.com/FunctioningForm',
    'http://feeds.feedburner.com/LincolnLoop',
    'https://www.djangoproject.com/rss/community/blogs/',
    'https://www.djangoproject.com/rss/weblog/',
    'http://www.notebookcheck.net/RSS-Feed-Notebook-Reviews.8156.0.html',
    'http://lucumr.pocoo.org/feed.atom',
    'http://rss1.smashingmagazine.com/feed/',
    'http://feeds.feedburner.com/RdioBlog',
    'http://feeds.feedburner.com/colossal',
    'http://feeds.fastcompany.com/fastcoexist/feed',
    'http://feeds.feedburner.com/WebDesignerWall',
    'http://feeds.feedburner.com/jQueryHowto',
    'http://feeds.feedburner.com/gnucitizen',
    'http://blog.fefe.de/rss.xml?html',
    'http://www.pro-linux.de/backend/pro-linux.rdf',
    'http://feeds.feedburner.com/GeekAndPoke',
    'http://blog.iso50.com/feed/',
    'http://feeds.feedburner.com/Octocats',
    'http://feeds.gawker.com/io9/full',
    'http://feeds2.feedburner.com/ProgrammableWeb',
    'http://feeds.howtogeek.com/HowToGeek',
    'http://feeds.feedburner.com/designmodo',
    'http://planet.ubuntu.com/rss20.xml',
    'http://feed.500px.com/500px-editors',
    'http://planetkde.org/rss20.xml',
    'http://firefoxnightly.tumblr.com/rss',
    'http://www.squarefree.com/burningedge/feed/',
    'http://planet.centos.org/atom.xml',
    'http://feed.500px.com/500px-blog',
    'http://blog.evernote.com/feed/',
    'http://feeds.feedburner.com/ffffound/everyone',
    'http://highscalability.com/rss.xml',
    'http://feeds.feedburner.com/heroku',
    'http://feeds.nationalgeographic.com/ng/News/News_Main',
    'http://blog.xfce.org/feed/',
    'http://feeds.feedburner.com/LostGarden',
    'http://blog.rememberthemilk.com/feed/atom/',
    'http://feeds.feedburner.com/shoeboxdwelling/PzFM',
    'http://feeds.feedburner.com/AndroidNewsGoogleAndroidForums',
    'http://feeds.feedburner.com/universetoday/pYdq',
    'http://feeds.feedburner.com/amixdk',
    'http://blog.dscpl.com.au/feeds/posts/default',
    'https://planet.archlinux.org/atom.xml',
    'http://www.fubiz.net/feed/',
    'http://feeds.feedburner.com/metajack',
    'http://www.artima.com/buzz/feeds/python.rss',
    'http://djangosnippets.org/feeds/latest/',
    'http://www.reddit.com/r/Python/.rss',
    'http://code.activestate.com/feeds/recipes/langs/python/',
    'http://www.linux-magazin.de/rss/feed/news',
    'http://ikhaya.ubuntuusers.de/feeds/full/20/',
    'http://feeds.feedburner.com/neuerdings1/',
    'http://www.go-mono.com/monologue/index.rss',
    'https://planet.gnome.org/atom.xml',
    'http://feeds.feedburner.com/Pixelsoup',
    'http://www.heise.de/open/news/news-atom.xml',
    'http://feeds.mobileread.com/mr/front',
    'http://scalingexperts.wordpress.com/feed/',
    'http://feeds.feedburner.com/hgtip/',
    'http://www.tuxradar.com/frontpage/feed',
    'http://feeds.feedburner.com/cssglobe',
    'http://www.heise.de/security/news/news-atom.xml',
    'http://feeds.feedburner.com/PythonInsider',
    'http://www.deimeke.net/dirk/blog/index.php?/feeds/index.rss2',
    'http://feeds.feedburner.com/UxArray',
    'http://betalabs.nokia.com/blog/rss',
    'http://www.heise.de/developer/rss/news-atom.xml',
    'http://feeds.fastcompany.com/fastcocreate/feed',
    'http://feeds2.feedburner.com/RandomGoodStuff',
    'http://dev.opera.com/feeds/atom/articles',
    'https://aur.archlinux.org/rss.php',
    'http://www.heise.de/tr/news-atom.xml',
    'http://feeds2.feedburner.com/webkrauts/iXSU',
    'http://www.laurentluce.com/feed/',
    'http://feeds.feedburner.com/voidspace',
    'http://theagileadmin.com/feed/',
    'http://pythonic.pocoo.org/feed.atom',
    'https://www.digitalocean.com/blog/feed.atom',
    'http://feeds.feedburner.com/asktheponyblog',
    'http://www.bonjourmadame.fr/rss',
    'http://www.androidlounge.at/lounge/?feed=rss2',
    'http://www.hoerspielprojekt.de/?feed=rss2',
    'http://rss.feedsportal.com/c/32509/f/480599/index.rss',
    'http://devnews.spotify.com/feed/',
    'http://mylinux.suzansworld.com/?feed=rss2',
    'http://feeds2.feedburner.com/Phoronix',
    'http://stefan.sofa-rockers.org/feeds/latest/',
    'http://labs.spotify.com/feed/',
    'https://blog.mozilla.org/labs/feed/',
    'http://www.shiningpanda.com/blog/feeds/latest/',
    'http://www.heise.de/mobil/newsticker/heise-atom.xml',
    'http://www.blendernation.com/feed/',
    'http://blogs.gnome.org/otte/feed/',
    'http://xapian.wordpress.com/feed/',
    'http://feeds.feedburner.com/nokiausers/AcCj',
    'http://feeds.feedburner.com/LinuxHatersBlog?format=xml',
    'http://tuxmobil.org/tuxmobil_rss.rdf',
    'http://blogs.gnome.org/sragavan/feed/',
    'http://feeds.feedburner.com/JamendoBlogEnglish',
    'http://feeds.feedburner.com/gidsy',
    'http://blog.golang.org/feed.atom',
    'https://pypi.python.org/pypi?:action=rss',
    'http://feeds.feedburner.com/campino2k_linux',
    'http://codeworkx.de/wordpress/feed/',
    'http://www.davidrevoy.com/feed.php?atom',
    'http://feeds.feedburner.com/erbenux/ErfahrungsberichteLinuxPlanet',
    'http://www.freiszene.de/backend.php?op=all',
    'https://code.djangoproject.com/timeline?changeset=on&max=50&authors=&daysback=90&format=rss',
    'https://code.djangoproject.com/timeline?ticket=on&milestone=on&changeset=on&wiki=on&max=50&authors=&daysback=90&format=rss',
    'http://www.hoerspiel-labor.de/rss.html',
    'http://www.hoerspielprojekt.de/?feed=atom',
    'http://feeds2.feedburner.com/LifeIsATechnicalGame?format=xml',
    'http://www.kde4.de/feed/',
    'http://netz10.de/tag/linux/feed/',
    'http://offenerdesktop.wordpress.com/tag/ubuntuusers-de/feed/',
    'http://www.onli-blogging.de/index.php?/feeds/categories/9-Linux.rss',
    'http://pythonforfunandprofit.blogspot.com/feeds/posts/default',
    'http://www.knetfeder.de/linux/index.php?rss=1',
    'http://rorschachstagebuch.wordpress.com/feed/',
    'http://beyondserenity.wordpress.com/category/kde-oss-it/feed/',
    'http://suzannahaworth.com/feed/',
    'http://feeds.feedburner.com/Venturevillage?format=xml',
    'http://feeds.feedburner.com/WebDesignerNotebook?format=xml',
    'http://triggeredupdates.wordpress.com/category/linux/feed/',
    'http://www.virgiliovasconcelos.com/rss.php',
    'http://feeds.feedburner.com/young-programmers',
    'http://www.ausminternet.de/category/planet/feed/',
    'http://www.graphicsplanet.org/rss20.xml',
    'http://planet.ubuntuusers.de/feeds/short/20/',
    'http://feeds.feedburner.com/symbian60/JMCb',
    'http://blog.abourget.net/feed.atom',
    'http://www.notebookcheck.net/News.152.100.html',
    'http://blogs.gnome.org/uraeus/feed/atom/',
    'http://blogs.gnome.org/cneumair/feed/atom/',
    'http://blog.stefan-betz.net/feed.atom',
    'http://www.mymuesli.com/blog/feed/atom/',
    'http://gloobus.wordpress.com/feed/atom/',
    'http://mark.doffman.com/feed/atom/',
    'http://paddy3118.blogspot.com/feeds/posts/default',
    'http://popolon.org/gblog2/feed/atom',
    'http://feeds2.feedburner.com/JqueryStyleTutorials',
    'http://blogs.gnome.org/gianmt/feed/',
    'http://30dbs.blogspot.com/feeds/posts/default',
    'http://www.blogger.com/feeds/3971202189709462152/posts/default?v=2&redirect=false',
    'http://blog.martin-graesslin.com/blog/feed/atom/',
    'http://blogs.gnome.org/hughsie/feed/atom/',
    'http://feeds2.feedburner.com/virtualpixel',
    'http://blogs.gnome.org/metacity/feed/',
    'http://www.wine-reviews.net/feed.atom',
    'http://animalnewyork.com/feed/',
    'http://www.yugatech.com/feed/',
    'http://techualization.blogspot.com/feeds/posts/default',
    'http://googleblog.blogspot.com/feeds/posts/default',
    'http://skipperkongen.dk/feed/',
    'http://250bpm.com/feed/pages/pagename/blog/category/blog/t/250bpm-blogs/h/http%3A%2F%2Fwww.250bpm.com%2Fblog',
    'http://www.elasticsearch.org/blog/feed/',
    'http://blog.rdio.com/developers/atom.xml',
    'https://www.twilio.com/blog/feed'
]


importer = FeedImporter()

print('Starting import for {} feeds'.format(len(links)))

for link in links:
    feed = importer.import_feed(link)
    print('Imported {}'.format(feed))

print(feed)
