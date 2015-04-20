import time, vk
from messenger import logger


class VkMessenger:
    def __init__(self, config):
        self.logger = logger.get(__name__)
        self.api = self.get_vkapi(config)

    def get_vkapi(self, dict):
        app_id = dict['app_id']
        login = dict['login']
        passw = dict['pass']
        self.logger.debug("Creating vkapi instance")
        vkapi = vk.API(app_id, login, passw)
        self.logger.debug('Created vkapi instance setting token')
        vkapi.access_token = dict["token"]
        self.logger.debug('Token set!')
        return vkapi

    def get_friends_by_id(self, userid=0):
        if userid != 0:
            friends = self.api('friends.get', user_id=userid)['items']
            return friends

    def comment_every_post(self, public_id, message, interval=15):
        posts_list = self.api.wall.get(owner_id=-public_id, extended=1)
        time.sleep(1)
        for i in reversed(range(1, len(posts_list['items']) + 1)):
            self.api.wall.addComment(owner_id=-public_id, post_id=i, text=message)
            time.sleep(interval)
        return

    def comment_post(self, public_id, post_id, message):
        self.api.wall.addComment(owner_id=-public_id, post_id=post_id, text=message)

    def get_top_n_groups_by_location(self, city, n, search_text):
        count_groups = n
        countries = self.api.database.getCountries(code="UA")
        country = countries['items'][0]
        cities = self.api.database.getCities(country_id=country['id'], q=city)
        city = cities['items'][0]
        groups = self.api.groups.search(q=search_text, city_id=city['id'])
        rgroups = []
        if groups['count'] < count_groups:
            count_groups = groups['count']
        for i in range(0, count_groups):
            rgroups.append(groups['items'][i])
        return rgroups