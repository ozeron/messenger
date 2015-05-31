
import time, vk
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
        posts_list = self.api.wall.get(owner_id=-public_id, extended=1)
        time.sleep(1)

        for i in reversed(range(1, len(posts_list['items']) + 1)):
            try:
                self.api.wall.addComment(owner_id=-public_id, post_id=i, text=message, attachments=photo)
            except vk.api.VkAPIMethodError as e:
                sid = e.get_capthca_sid()
                result = self.get_capthca(e.get_capthca_sid(), e.get_capthca_url())
                if(result == False):
                    break
                try:
                    self.api.wall.addComment(owner_id=-public_id,
                                             post_id=i,
                                             text=message,
                                             attachments=photo,
                                             captcha_sid=sid,
                                             captcha_key=result)
                    continue
                except vk.api.VkAPIMethodError as q:
                    self.logger.debug('Error. Incorrect capthca!')
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

    def get_pictures(self, album):
        return self.api.photos.get(owner_id=int(self.api.users.get()[0]['id']), album_id=album)

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

    def get_top_n_groups_by_location(self, city, n, search_text):
        count_groups = n
        countries = self.api.database.getCountries(code="UA")
        country = countries['items'][0]
        cities = self.api.database.getCities(country_id=country['id'], q=city)
        city = cities['items'][0]
        groups = self.api.groups.search(q=search_text, city_id=city['id'])
        rgroups = []
        if int(groups['count']) < count_groups:
            count_groups = int(groups['count'])
        for i in range(0, count_groups):
            rgroups.append(groups['items'][i])
        return rgroups
