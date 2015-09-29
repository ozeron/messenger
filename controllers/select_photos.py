from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QUrl
from PyQt5.QtWidgets import QWidget, QListView
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest


class SelectPhotosDialog(QWidget):
    MAX_PHOTOS_IMMEDIATE_LOAD = 20
    def __init__(self, client, sender):
        QWidget.__init__(self)
        self.client = client
        self.sender = sender
        self.ui = loadUi('uis/select_photos.ui', self)
        self.widget_photos = self.ui.wdgPhotos
        self.cache_net_manager = QNetworkAccessManager()
        self.cache_net_manager.finished.connect(self.__load_photo)
        self.widget_albums = self.ui.wdgAlbums
        self.net_manager = QNetworkAccessManager()
        self.net_manager.finished.connect(self.__load_image)

        album_data = self.client.get_albumData()
        album_items = album_data['items']
        self.selected_album = 0
        #self.widget_albums.setViewMode(QListView.ListMode)
        self.icon_size = QSize(100,100)
        self.widget_albums.setGridSize(QSize(150,160))
        self.widget_albums.setMovement(QListView.Static)
        self.widget_albums.setIconSize(self.icon_size)
        self.widget_albums.setFlow(QListView.TopToBottom)
        self.widget_albums.setViewMode(QListView.IconMode)
        self.widget_albums.setSelectionMode(QListView.SingleSelection)
        self.widget_albums.itemClicked.connect(self.__on_album_click)
        self.widget_photos.setGridSize(QSize(110,130))
        self.widget_photos.setMovement(QListView.Static)
        self.widget_photos.setIconSize(self.icon_size)
        self.widget_photos.setFlow(QListView.TopToBottom)
        self.widget_photos.setViewMode(QListView.IconMode)
        self.widget_photos.setSelectionMode(QListView.SingleSelection)
        self.widget_photos.itemDoubleClicked.connect(self.__return_photo)
        self.loading_pix = QPixmap("loading.png").scaled(self.icon_size)
        self.null_pix = QPixmap("nothumb").scaled(self.icon_size)
        self.albums = []
        self.photos = {}
        for item in album_items:
            comment = item["title"]
            if(len(comment) > 15):
                comment = comment[:15] + "..."
            new_item = QListWidgetItem(QIcon(self.loading_pix),comment)
            self.widget_albums.addItem(new_item)
            reply = self.net_manager.get(QNetworkRequest(QUrl(item["thumb_src"])))
            self.albums.append({"listItem":new_item,'reply':reply,'data':item,'pixmap':self.loading_pix})
            new_item.setIcon(QIcon(self.albums[len(self.albums) - 1]['pixmap']))

    def __load_image(self,reply):
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll(), "jpg")
        for item in self.albums:
            if(item['reply'] == reply):
                if(pixmap.isNull()):
                    pixmap = self.null_pix
                item['pixmap'] = pixmap
                
                item['listItem'].setIcon(QIcon(item['pixmap'].scaled(self.icon_size)))
                return

    def __on_album_click(self,item):
        for element in self.albums :
            if element['listItem'] == item :
                album_id = element['data']['id']
                if album_id == self.selected_album:
                    return
                self.selected_album = album_id
                self.widget_photos.clear()
                if not(album_id in self.photos):
                    self.photos[album_id] = self.client.get_photos(album_id)
                    self.photos[album_id]['sorted']={}
                    photos = self.photos[album_id]
                    photo_items = photos['items']
                    for item in photo_items:
                        comment = item["text"]
                        if(len(comment) > 15):
                            comment = comment[:15] + "..."
                        new_item = QListWidgetItem(QIcon(self.loading_pix),comment)
                        self.widget_photos.addItem(new_item)
                        reply = self.cache_net_manager.get(QNetworkRequest(QUrl(item["photo_130"])))
                        self.photos[album_id]['sorted'][reply] = {"listItem":new_item,'data':item,'pixmap':self.loading_pix,'album':album_id}
                    return
                else:
                    photos = self.photos[album_id]['sorted']
                    for item in photos.keys() :
                        comment = photos[item]['data']['text']
                        pix = photos[item]['pixmap']
                        if(len(comment) > 15):
                            comment = comment[:15] + "..."
                        new_item = QListWidgetItem(QIcon(pix.scaled(self.icon_size)),comment)
                        self.widget_photos.addItem(new_item)

                    return
                    

    def __load_photo(self,reply):
        pixmap = QPixmap()
        pixmap.loadFromData(reply.readAll(), "jpg")
        for item in self.photos:
            if(reply in self.photos[item]['sorted']):
                self.photos[item]['sorted'][reply]['pixmap'] = pixmap
                self.photos[item]['sorted'][reply]['listItem'].setIcon(QIcon(self.photos[item]['sorted'][reply]['pixmap'].scaled(self.icon_size)))
                return
    
    def __return_photo(self,item):
        displayed_photos = self.photos[self.selected_album]['sorted']
        for reply in displayed_photos:
            if displayed_photos[reply]['listItem']==item:
                result = {'album_id':self.selected_album, 'photo_id':displayed_photos[reply]['data']['id']}
                self.sender._get_photo(result,self)
                return
        
    