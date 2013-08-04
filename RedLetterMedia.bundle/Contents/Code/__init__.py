TITLE = 'Red Letter Media'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
NS = {'blip':'http://blip.tv/dtd/blip/1.0',
            'media':'http://search.yahoo.com/mrss/'}

RSS_FEED = 'http://redlettermedia.blip.tv/rss'
PLINKETT = 'http://www.redlettermedia.com/plinkett/'
BOW = 'http://redlettermedia.com/best-of-the-worst/'
HITB = 'http://redlettermedia.com/half-in-the-bag/%s'
HITBMORE = '2011-episodes', '2012-episodes', '2013-episodes'

###################################################################################################

# Set up containers for all possible objects
def Start():

  ObjectContainer.title1 = TITLE

###################################################################################################
@handler('/video/redlettermedia', TITLE, art=ART, thumb=ICON)
def Mainmenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(Plinkett, title="Mr. Plinkett"), title="Mr. Plinkett"))
    oc.add(DirectoryObject(key=Callback(HalfBag, title="Half in the Bag"), title="Half in the Bag"))
    oc.add(DirectoryObject(key=Callback(BestWorst, title="Best of the Worst"), title="Best of the Worst"))
    oc.add(DirectoryObject(key=Callback(AllShows, title="All Shows"), title="All Shows"))
    return oc

###################################################################################################
@route('/video/redlettermedia/plinkett')
def Plinkett(title):
    oc = ObjectContainer(title2=title) #, user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4')

# First we find the list of videos.
    for link in HTML.ElementFromURL(PLINKETT).xpath('//*[@id="post-main-37"]/div/p/a/@href'):
# Some links don't start with the base URL, so we have to add it to them.
        Log('link is')
	Log(link)
	url = link#.xpath('/@href')[0]
        if link[0:4] != 'http': url = PLINKETT + link
        Log('URL is')
	Log(url)
# Now we need to go to each URL for the actual video links. Turns out that some videos are in embed tags, others in iframe tags, some from youtube and some from blip.
        video = HTML.ElementFromURL(url).xpath('//embed')[0].get('src')
        Log('video is')
	Log(video)
        thumb = HTML.ElementFromURL(PLINKETT).xpath('./a/img')#.get('src')
        Log(thumb)
	Log(url)

	oc.add(VideoClipObject(
		url = url,
		thumb = thumb))

    return oc


###################################################################################################
@route('/video/redlettermedia/halfbag')
def HalfBag(title):
    oc = ObjectContainer(title2=title)

# Pages are split up by year. Get list of videos from each page.
    for page in HITBMORE:
        page = HITB % (page)
        for video in HTML.ElementFromURL(page).xpath('//*[@id="post-main-515"]/div/p'):
               url = video.xpath('./a')[0].get('href')
               thumb = video.xpath('./a/img')[0].get('src')
               Log(url)
	
	oc.add(VideoClipObject(
		url = url,
		thumb = thumb))

    return oc

###################################################################################################
@route('/video/redlettermedia/bestworst')
def BestWorst(title):
    oc = ObjectContainer(title2=title)

    for video in HTML.ElementFromURL(BOW).xpath('//*[@id="post-main-3857"]/div/p/a/@href'):
       	Log(video)
       	url = video
       	thumb = video #.xpath('./@src')[0]
       	Log(url)
       	Log(thumb)

       	oc.add(VideoClipObject(
               	url = url,
               	thumb = thumb))

    return oc

###################################################################################################
@route('/video/redlettermedia/allshows')
def AllShows(title):
    oc = ObjectContainer(title2=title)

    for video in XML.ElementFromURL(RSS_FEED).xpath('//item'):
        Log(video)
	url = video.xpath('./link')[0].text
        Log(url)
	title = video.xpath('./title')[0].text
        date = video.xpath('./pubDate')[0].text
        date = Datetime.ParseDate(date)
        summary = video.xpath('./blip:puredescription', namespaces=NS)[0].text
        thumb = video.xpath('./media:thumbnail', namespaces=NS)[0].get('url')
        if thumb[0:4] != 'http': thumb = 'http://a.images.blip.tv' + thumb
        duration_text = video.xpath('./blip:runtime', namespaces=NS)[0].text
        duration = int(duration_text) * 1000

        oc.add(VideoClipObject(
              url = url,
              title = title,
              summary = summary,
              #thumb = Callback(Thumb, url=thumb),
              duration = duration,
              originally_available_at = date))

    return oc
