
import vk, sys, json, time

APP_ID = '4841859'

# TODO: add quequ adding


class VkMessenger:
    def __init__(self, vkapi):
        self.api = vkapi

    def get_friends_by_id(self, userid=0):
        if userid != 0:
            friends = self.api('friends.get', user_id=userid)['items']
            return friends

    def comment_every_post(self, public_id, message, interval=1):
        posts_list = self.api.wall.get(owner_id=-self.public_id, extended=1)
        time.sleep(1)
        for i in range(1, len(posts_list['items']) + 1):
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


def init(json):
  for entry in json:
    vkapi = vk.API(APP_ID, entry["login"], entry["password"])
    vkapi.access_token = entry["access_token"]





if __name__ == '__main__':
  path = 'credentials.json'
  if len(sys.argv) > 1:
    path = sys.argv[1]
  text = open(path, 'r').read()
  json = json.loads(text)
  init(json)