#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2011-2014 Martijn Kaijser
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#

#import modules
import lib.common
import xbmcgui
from lib.utils import log

### get addon info
__addonname__    = lib.common.__addonname__
__addonpath__    = lib.common.__addonpath__
__localize__     = lib.common.__localize__
__icon__         = lib.common.__icon__

### set button actions for GUI
ACTION_PREVIOUS_MENU = (9, 10, 92, 216, 247, 257, 275, 61467, 61448)

pDialog = xbmcgui.DialogProgress()
pDialogBG = xbmcgui.DialogProgressBG()

# Define dialogs
def dialog_msg(action,
               percentage = 0,
               heading = '',
               message = '',
               background = False,
               nolabel = __localize__(32026),
               yeslabel = __localize__(32025),
               cancelled = False):
    # Fix possible unicode errors 
    heading = heading.encode('utf-8', 'ignore')
    message = message.encode('utf-8', 'ignore')
    # Dialog logic
    if not heading == '':
        heading = __addonname__
    if not background:
        try:
            if action == 'create':
                pDialog.create(__addonname__)
            elif action == 'update':
                pDialog.update(percentage,
                               message = "\n")
                pDialog.update(percentage,
                               message)
            elif action == 'close':
                pDialog.close()
            elif action == 'iscanceled':
                if pDialog.iscanceled():
                    return True
                else:
                    return False
            elif action == 'createBG':
                pDialogBG.create(heading = __addonname__,
                                 message = message)
            elif action == 'updateBG':
                pDialogBG.update(percent = percentage,
                                 heading = __addonname__,
                                 message = "\n")
                pDialogBG.update(percent = percentage,
                                 heading = __addonname__,
                                 message = message)
            elif action == 'closeBG':
                pDialogBG.close()
            elif action == 'iscanceledBG':
                return False
            elif action == 'okdialog':

                xbmcgui.Dialog().ok(heading,
                                    message)
            elif action == 'yesno':
                return xbmcgui.Dialog().yesno(heading,
                                              message,
                                              nolabel,
                                              yeslabel)
        except:
            pass
    else:
        if (action == 'create' or action == 'okdialog'):
            msg = message
            if not cancelled:
                xbmcgui.Dialog().notification(heading,
                                              msg,
                                              __icon__,
                                              7500)

# Return the selected url to the GUI part
def choose_image(imagelist):
    image_item = False
    image_item = dialog_select(imagelist)
    return image_item 

# This creates the art type selection dialog. The string id is the selection constraint for what type has been chosen.
def choice_type(enabled_type_list, startup, artype_list):
    # Send the image type list to the selection dialog
    select = xbmcgui.Dialog().select(__addonname__ + ': ' + __localize__(32015) , enabled_type_list)
    # When nothing is selected from the dialog
    if select == -1:
        log('### Canceled by user')
        return False
    # If some selection was made
    else:
        # Check what artwork type has been chosen and parse the image restraints
        for item in artype_list:
            if enabled_type_list[select] == __localize__(item['gui_string']) and startup['mediatype'] == item['media_type']:
                return item
        else:
            return False

# Pass the imagelist to the dialog and return the selection
def dialog_select(image_list):
    w = dialog_select_UI('DialogSelect.xml', __addonpath__, listing=image_list)
    w.doModal()
    selected_item = False
    try:
        # Go through the image list and match the chooosen image id and return the image url
        for item in image_list:
            if w.selected_id == item['id']:
                selected_item = item
        return selected_item
    except: 
        print_exc()
        return selected_item
    del w

### Retrieves imagelist for GUI solo mode
def gui_imagelist(image_list, art_type):
    log('- Retrieving image list for GUI')
    filteredlist = []
    #retrieve list
    for artwork in image_list:
        if  art_type in artwork['art_type']:
            filteredlist.append(artwork)
    return filteredlist

### Checks imagelist if it has that type of artwork has got images
def hasimages(image_list, art_type):
    found = False
    for artwork in image_list:
        if art_type in artwork['art_type']:
            found = True
            break
        else: pass
    return found
    
class dialog_select_UI(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.selected_id = ''

    def onInit(self):
        try :
            self.img_list = self.getControl(6)
            self.img_list.controlLeft(self.img_list)
            self.img_list.controlRight(self.img_list)
            self.getControl(3).setVisible(False)
        except :
            print_exc()
            self.img_list = self.getControl(3)

        self.getControl(5).setVisible(False)
        self.getControl(1).setLabel(__localize__(32015))

        for image in self.listing:
            listitem = xbmcgui.ListItem('%s' %(image['generalinfo']))
            listitem.setArt({'icon': image['preview']})
            listitem.setLabel2(image['preview'])
            self.img_list.addItem(listitem)
        self.setFocus(self.img_list)

    def onAction(self, action):
        if action in ACTION_PREVIOUS_MENU:
            self.close()

    def onClick(self, controlID):
        log('# GUI control: %s' % controlID)
        if controlID == 6 or controlID == 3: 
            num = self.img_list.getSelectedPosition()
            log('# GUI position: %s' % num)
            self.selected_id = self.img_list.getSelectedItem().getLabel2()
            log('# GUI selected image ID: %s' % self.selected_id)
            self.close()

    def onFocus(self, controlID):
        pass