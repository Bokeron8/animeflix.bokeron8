# import the kodi python modules we are going to use
# see the kodi api docs to find out what functionality each module provides
import xbmc
import xbmcgui
import xbmcaddon
import requests

# create a class for your addon, we need this to get info about your addon
ADDON = xbmcaddon.Addon()
# get the full path to your addon, decode it to unicode to handle special (non-ascii) characters in the path
CWD = ADDON.getAddonInfo('path')

# add a class to create your xml based window
class GUI(xbmcgui.WindowXML):
    # [optional] this function is only needed of you are passing optional data to your window
    def __init__(self, *args, **kwargs):
        # get the optional data and add it to a variable you can use elsewhere in your script
        self.data = kwargs['optional1']

    # until now we have a blank window, the onInit function will parse your xml file
    def onInit(self):
        # select a view mode, '50' in our case, as defined in the skin file
        xbmc.executebuiltin('Container.SetViewMode(50)')
        # define a temporary list where we are going to add all the listitems to
        listitems = []
        try:
            response = requests.get("https://animeflix-next.vercel.app/api/getVideoServers?title=spy-x-family&episode_number=1")
            response.raise_for_status()  # Raise an exception for HTTP errors
            items = response.json()
        except requests.RequestException as e:
            xbmc.log(f"Failed to fetch data: {e}", level=xbmc.LOGERROR)
            items = [{"server": "xd", "url": "https://moodle1.playmudos.com/aTJ1WXJScHdVTzVjMjluYmhCeDY0NzdGRnZxQ0pwY1Zsb01pMEVmTlFDRT0.m3u8"}]

        # Add items to the list
        for item in items:
            listitem = xbmcgui.ListItem(label=item['server'])
            # Pass URL as an argument when an item is clicked
            listitem.setProperty('url', item['url'])
            listitems.append(listitem)
        
        #xbmc.Player().play()
        self.clearList()
        # now we are going to add all the items we have defined to the (built-in) container
        # Add items to the container
        self.getControl(50).addItems(listitems)
        # give kodi a bit of (processing) time to add all items to the container
        xbmc.sleep(100)
        # this puts the focus on the top item of the container
        self.setFocusId(self.getCurrentContainerId())        

    def onClick(self, controlId):
        if controlId == 50:  # Assuming controlId 1 is your list
            selectedItem = self.getControl(controlId).getSelectedItem()
            url = selectedItem.getProperty('url')
            if url:
                xbmc.Player().play(url)

# this is the entry point of your addon, execution of your script will start here
if (__name__ == '__main__'):
    # define your xml window and pass these five arguments (more optional items can be passed as well):
    # 1 'the name of the xml file for this window', 
    # 2 'the path to your addon',
    # 3 'the name of the folder that contains the skin',
    # 4 'the name of the folder that contains the skin xml files'
    # 5 set to True for a media window (a window that will list music / videos / pictures), set to False otherwise
    # 6 [optional] if you need to pass additional data to your window, simply add them to the list
    # you'll have to add them as key=value pairs: key1=value1, key2=value2, etc...
    ui = GUI('script-testwindow.xml', CWD, 'default', '1080i', True, optional1='some data')
    # now open your window. the window will be shown until you close your addon
    ui.doModal()
    # window closed, now cleanup a bit: delete your window before the script fully exits
    del ui

# the end!
