TITLE = 'Red Letter Media'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

FEED =

###################################################################################################

# Set up containers for all possible objects
def Start():

  ObjectContainer.title1 = TITLE

###################################################################################################
@handler('/video/redlettermedia')
def Mainmenu():
    oc = ObjectContainer()
    oc.add(DirectoryObject(key=Callback(Plinkett, title="Mr. Plinkett"), title="Mr. Plinkett"))
    oc.add(DirectoryObject(key=Callback(HalfBag, title="Half in the Bag"), title="Half in the Bag"))
    oc.add(DirectoryObject(key=Callback(BestWorst, title="Best of the Worst"), title="Best of the Worst"))
    return oc

###################################################################################################
@route('/video/redlettermedia/plinkett')
def Plinkett(title):
    oc = ObjectContainer(title2=title)
    Log('figure out the show stuff. any RSS feeds?')

    return oc

###################################################################################################
@route('/video/redlettermedia/halfbag')
def HalfBag(title):
    oc = ObjectContainer(title2=title)
    Log('some more figuring')

    return oc

###################################################################################################
@route('/video/redlettermedia/bestworst')
def BestWorst(title):
    oc = ObjectContainer(title2=title)
    Log('Some more figuring')

    return oc
