TITLE = 'Red Letter Media'
ART = 'art-default.jpg'
ICON = 'icon-default.png'
PREFIX = '/video/redlettermedia'
NS = {'blip':'http://blip.tv/dtd/blip/1.0',
            'media':'http://search.yahoo.com/mrss/'}

RSS_FEED = 'http://redlettermedia.blip.tv/rss'
PLINKETT = BASEURL + '/plinkett/'
PLINKETTCATS = 'star-trek', 'star-wars', 'other-movies', 'commentary-tracks', 'plinkett-review-trailers', 'plinkett-review-extras', 'mr-plinkett-the-animated-series'
BOTW = BASEURL + '/best-of-the-worst/'
HITB = BASEURL + '/half-in-the-bag/'
BASEURL = 'http://redlettermedia.com'
#HITBMORE = '2011-episodes', '2012-episodes', '2013-episodes', '2014-episodes'
MAX_EPISODES_PER_PAGE = 10

###################################################################################################

# Set up containers for all possible objects
def Start():

  ObjectContainer.title1 = TITLE

###################################################################################################
@handler('/video/redlettermedia', TITLE, art=ART, thumb=ICON)
def Mainmenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(PlinkMenu, title="Mr. Plinkett"), title="Mr. Plinkett", thumb = R('plinkett.png')))
    oc.add(DirectoryObject(key=Callback(HITBMenu, title="Half in the Bag"), title="Half in the Bag", thumb = R('hitb.png')))
    oc.add(DirectoryObject(key=Callback(BestWorst, title="Best of the Worst"), title="Best of the Worst", thumb = R('BOTW.png')))
    oc.add(DirectoryObject(key=Callback(AllShows, title="All Shows"), title="All Shows", thumb = R(ICON)))
    return oc

###################################################################################################
# Submenu for Plinkett
@route(PREFIX + '/plinkett/plinkmenu')
def PlinkMenu(title):
    oc = ObjectContainer(title2=title)
    oc.add(DirectoryObject(key=Callback(StarTrek, title='Star Trek'), title='Star Trek', thumb = R(ICON)))
    oc.add(DirectoryObject(key=Callback(StarWars, title='Star Wars'), title='Star Wars', thumb = R(ICON)))
    oc.add(DirectoryObject(key=Callback(OtherMovies, title='Other Movies'), title='Other Movies', thumb = R(ICON)))
    #oc.add(DirectoryObject(key=Callback(Commentary, title='Commentary', sort_type='commentary'), title='Commentary', thumb = R(ICON)))
    #oc.add(DirectoryObject(key=Callback(Trailers, title='Trailers', sort_type='Trailers'), title='Trailers', thumb = R(ICON)))
    #oc.add(DirectoryObject(key=Callback(Extras, title='Extras', sort_type='extras'), title='Extras', thumb = R(ICON)))
    return oc
###################################################################################################
# Submenu for Half in the Bag
@route(PREFIX + '/hitb/hitbmenu')
def HITBMenu(title):
    oc = ObjectContainer(title2=title)
    # Dynamically generate the menu based on the site drop downs.
    dropdown = HTML.ElementFromURL(BASEURL).xpath('//*[@id="menu-item-527"]/ul/li/a/@href')
    for ent in dropdown:
        # Must remove the hyphens in the function names.
        oc.add(DirectoryObject(key=Callback(ent[47:].strip('/"').replace('-',''), title=ent[47:].strip('/"')), title=ent[47:].strip('/"'), thumb = R(ICON)))
    return oc
###################################################################################################
# Star Trek Section of Plinkett reviews.
@route(PREFIX + '/startrek')
def StarTrek(title):
    oc = ObjectContainer(title2=title)

    thumblist = HTML.ElementFromURL(PLINKETT + 'star-trek').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(PLINKETT + 'star-trek').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = PLINKETT + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb, title = title))
    return oc
###################################################################################################
# Star Wars Section of Plinkett reviews.
@route(PREFIX + '/starwars')
def StarWars(title):
    oc = ObjectContainer(title2=title)

    thumblist = HTML.ElementFromURL(PLINKETT + 'star-wars').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(PLINKETT + 'star-wars').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = PLINKETT + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb))
    return oc
###################################################################################################
# Other Movies Section of Plinkett reviews.
@route(PREFIX + '/othermovies')
def OtherMovies(title):
    oc = ObjectContainer(title2=title)

    thumblist = HTML.ElementFromURL(PLINKETT + 'other-movies').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(PLINKETT + 'other-movies').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = PLINKETT + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb))
    return oc
###################################################################################################
@route(PREFIX + '/fourteen', offset = int)
#cant hyphenate
def 2014episodes(title, offset = 0):
    oc = ObjectContainer(title2=title)

    counter = 0
    thumblist = HTML.ElementFromURL(HITB + '2014-episodes').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(HITB + '2014-episodes').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        counter = counter + 1
        if counter <= offset:
            continue
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = HITB + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb, title = title))
        if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(Fourteen, title = '2014 Episodes', offset = counter), title = 'Next'))
            return oc
        elif len(oc) == 0:
            ObjectContainer(header="Error", message="This section does not contain any video")
            return oc
    return oc

####################################################################################################
@route(PREFIX + '/thirteen', offset = int)
def 2013episodes(title, offset = 0):
    oc = ObjectContainer(title2=title)

    counter = 0
    thumblist = HTML.ElementFromURL(HITB + '2013-episodes').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(HITB + '2013-episodes').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        counter = counter + 1
        if counter <= offset:
            continue
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = HITB + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb, title = title))
        if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(Thirteen, title = '2013 Episodes', offset = counter), title = 'Next'))
            return oc
        elif len(oc) == 0:
            ObjectContainer(header="Error", message="This section does not contain any video")
            return oc
    return oc
###################################################################################################
@route(PREFIX + '/twelve', offset = int)
def 2012episodes(title, offset = 0):
    oc = ObjectContainer(title2=title)

    counter = 0
    thumblist = HTML.ElementFromURL(HITB + '2012-episodes').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(HITB + '2012-episodes').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        counter = counter + 1
        if counter <= offset:
            continue
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = HITB + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
                Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb, title = title))
        if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(Twelve, title = '2012 Episodes', offset = counter), title = 'Next'))
            return oc
        elif len(oc) == 0:
            ObjectContainer(header="Error", message="This section does not contain any video")
        return oc
    return oc
###################################################################################################
@route(PREFIX + '/eleven', offset = int)
def 2011episodes(title, offset = 0):
    oc = ObjectContainer(title2=title)

    counter = 0
    thumblist = HTML.ElementFromURL(HITB + '2011-episodes').xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(HITB + '2011-episodes').xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        counter = counter + 1
        if counter <= offset:
            continue
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = HITB + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
            Log('Video is %s' %url)
            oc.add(VideoClipObject(url = url, thumb = thumb, title = title))
            if len(oc) >= MAX_EPISODES_PER_PAGE:
                oc.add(NextPageObject(key = Callback(Eleven, title = '2011 Episodes', offset = counter), title = 'Next'))
                return oc
            elif len(oc) == 0:
                ObjectContainer(header="Error", message="This section does not contain any video")
            return oc
    return oc
###################################################################################################
@route(PREFIX + '/bestworst', offset = int)
def BestWorst(title, offset = 0):

    oc = ObjectContainer(title2=title)

    counter = 0
    thumblist = HTML.ElementFromURL(BOTW).xpath('//*[@class="post clearfix"]/div/p/a/img/@src')
    nextthumb = 0

    # Get list of videos.
    for link in HTML.ElementFromURL(BOTW).xpath('//*[@class="post clearfix"]/div/p/a/@href'):
        counter = counter + 1
        if counter <= offset:
            continue
        Log('Link is %s' %link)
        thumb = thumblist[nextthumb]
        nextthumb = nextthumb + 1
        Log('Thumbnail is %s' %thumb)
        # Some links need the base URL added.
        if link[0:4] != 'http':
            link = BOTW + link
        Log('Full link is %s' %link)
        try:
            url = HTML.ElementFromURL(link).xpath('//embed')[0].get('src')
            if url.startswith('http://a.'):
                url = 'http://blip.tv/play/%s.html' % (url[25:36])
        except IndexError:
            Log('End of list.')
        Log('Video is %s' %url)
        oc.add(VideoClipObject(url = url, thumb = thumb, title = title))
        if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(BestWorst, title = 'Best of the Worst', offset = counter), title = 'Next'))
            return oc
        elif len(oc) == 0:
            ObjectContainer(header="Error", message="This section does not contain any video")
            return oc
    return oc
############################################################################
@route('/video/redlettermedia/allshows', offset = int)
def AllShows(title, offset = 0):
    oc = ObjectContainer(title2 = title)

    counter = 0

    for video in XML.ElementFromURL(RSS_FEED).xpath('//item'):
        counter = counter + 1
        if counter <= offset:
            continue
        Log('Video is %s' %video)
        url = video.xpath('./link')[0].text
        Log('URL is %s' %url)
        title = video.xpath('./title')[0].text
        date = video.xpath('./pubDate')[0].text
        date = Datetime.ParseDate(date)
        summary = video.xpath('./blip:puredescription', namespaces=NS)[0].text
        thumb = video.xpath('./media:thumbnail', namespaces=NS)[0].get('url')
        if thumb[0:4] != 'http':
            thumb = 'http://a.images.blip.tv' + thumb
        duration_text = video.xpath('./blip:runtime', namespaces=NS)[0].text
        duration = int(duration_text) * 1000

        oc.add(VideoClipObject(url = url, title = title, summary = summary, thumb = thumb, duration = duration, originally_available_at = date))

        if len(oc) >= MAX_EPISODES_PER_PAGE:
            oc.add(NextPageObject(key = Callback(AllShows, title = 'All Shows', offset = counter), title = 'Next'))
            return oc
        elif len(oc) == 0:
            ObjectContainer(header="Error", message="This section does not contain any video")
            return oc

    return oc
