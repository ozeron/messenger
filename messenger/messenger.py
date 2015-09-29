
import time, vk
from vk_api_patch import api
import requests
from controllers.get_captcha import GetCapthca

from messenger import logger


class VkMessenger:
    def __init__(self, config):
        self.logger = logger.get(__name__)
        self.api = self.get_vkapi(config)

    def get_vkapi(self, dict):
        app_id = dict['app_id']
        login = dict['login']
        passw = dict['pass']
        token = dict['token']

        self.logger.debug("Creating vkapi instance")
        vkapi = vk.API(app_id, login, passw, token)
        self.logger.debug('Created vkapi instance setting token')
        vkapi.access_token = dict["token"]
        self.logger.debug('Token set!')
        return vkapi

    def get_friends_by_id(self, userid=0):
        if userid == 0:
            userid = int(self.api.users.get()[0]['id'])
        friends = self.api('friends.get', user_id=userid)['items']
        return friends

    def comment_every_post(self, public_id, message, interval=15, photo=None):
        posts_list = self.api.wall.get(owner_id=-public_id, count=50)
        time.sleep(1)
        for i in posts_list['items']:
            post_id = i['id']
            try:
                self.api.wall.addComment(owner_id=-public_id, post_id=post_id, text=message, attachments=photo)
                self.logger.debug("Commented post id: %s" % post_id)
            except vk.api.VkAPIMethodError as e:
                sid = e.get_capthca_sid()
                result = self.get_capthca(e.get_capthca_sid(), e.get_capthca_url())
                if(result == False):
                    break
                try:
                    self.api.wall.addComment(owner_id=-public_id,
                                             post_id=post_id,
                                             text=message,
                                             attachments=photo,
                                             captcha_sid=sid,
                                             captcha_key=result)
                    continue
                except vk.api.VkAPIMethodError as q:
                    self.logger.debug('Error. Incorrect captcha!')
                    continue
            time.sleep(interval)

    def comment_post(self, public_id, post_id, message):
        try:
            self.api.wall.addComment(owner_id=-public_id, post_id=post_id, text=message)
        except vk.api.VkAPIMethodError as e:
            sid = e.get_capthca_sid()
            result = self.get_capthca(e.get_capthca_sid(), e.get_capthca_url())
            if(result == False):
                return
            try:
                self.api.wall.addComment(owner_id=-public_id,
                                         post_id=post_id,
                                         text=message,
                                         captcha_sid=sid,
                                         captcha_key=result)
            except vk.api.VkAPIMethodError as q:
                self.logger.debug('Error. Incorrect capthca!')


    def get_capthca(self, sid, url):
        dialog = GetCapthca(sid, url)
        dialog.exec_()
        return dialog.get_result()

    def find_group_by_id(self,g_id):
        self.logger.debug("Trying to get groupById: %s" % g_id)
        return self.api.groups.getById(group_ids=[g_id])

    def group_exists(self, g_id):
        groups = self.find_group_by_id(g_id)
        if isinstance(groups, dict):
            return False, None
        else:
            return True, groups[0]

    def get_group_name(self, group_id):
        status, group = self.group_exists(group_id)
        if status and "name" in group.keys():
            return group["name"]
        return ""

    def get_top_n_cities_by_country_and_name_with_offset(self, country, name = "", n = 20, off = 0):
        cities = self.api.database.getCities(country_id = country, q = name, count = n, offset = off);
        return cities;

    def get_top_n_groups_by_location(self, city_id, n, search_text, _offset = 0):
        count_groups = n
        groups = self.api.groups.search(q=search_text, city_id=city_id, offset = _offset)
        rgroups = []
        return groups['items'][:count_groups]

    def get_albumData(self):
        return self.api.photos.getAlbums(need_covers = 1,need_system=1)

    def get_photo(self,album,photo):
        if isinstance(album,str):
            all_photos = self.api.photos.get(album_id=album)['items']
            for item in all_photos:
                if item['id'] == photo:
                   return item
        return self.api.photos.get(album_id=album,photo_ids=photo)['items'][0]

    def get_photos(self, album):
        return self.api.photos.get(owner_id=int(self.api.users.get()[0]['id']), album_id=album)

    def get_allPhotos(self):
        return self.api.photos.getAll()

    def get_userId(self):
        return self.api.users.get()[0]['id']