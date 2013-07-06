TITLE = 'Red Letter Media'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
NS = {'blip':'http://blip.tv/dtd/blip/1.0',
            'media':'http://search.yahoo.com/mrss/'}

RSS_FEED = 'http://redlettermedia.blip.tv/rss'
PLINKETT = 'http://redlettermedia.com/plinkett'
BOW = 'http://redlettermedia.com/best-of-the-worst'
HITB = 'http://redlettermedia.com/half-in-the-bag'

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
    oc = ObjectContainer(title2=title)

	#Log('figure out the show stuff. any RSS feeds?')
    #html = HTML.ElementFromURL(PLINKETT)
    for video in HTML.ElementFromURL(PLINKETT).xpath('//*[@id="post-main-37"]/div/p'):
        url = video.xpath('./a')[0].get('href') #Do I need to (PLINKETT + url) some place?
        if url[0:4] != 'http': url = PLINKETT + url # Some URLs have http and some don't. Add it to those that don't.
	thumb = video.xpath('./a/img')[0].get('src')

	oc.add(VideoClipObject(
		url = url,
		thumb = thumb))

    return oc


###################################################################################################
@route('/video/redlettermedia/halfbag')
def HalfBag(title):
    oc = ObjectContainer(title2=title)

	#Log('some more figuring')
    #html = HTML.ElementFromUrl(HITB)
    for video in HTML.ElementFromURL(HITB).xpath('//*[@id="post-main-515"]/div/p'):
	url = video.xpath('./a')[0].get('href') #Pages are broken into 2013, 2012, 2011. How do I make a single list?
	thumb = video.xpath('./a/img')[0].get('src')
		
	oc.add(VideoClipObject(
		url = url,
		thumb = thumb))

    return oc

###################################################################################################
@route('/video/redlettermedia/bestworst')
def BestWorst(title):
    oc = ObjectContainer(title2=title)
    Log('Some more figuring')

    return oc

###################################################################################################
@route('/video/redlettermedia/allshows')
def AllShows(title):
    oc = ObjectContainer(title2=title)

    for video in XML.ElementFromURL(RSS_FEED).xpath('//item'):
        url = video.xpath('./link')[0].text
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
