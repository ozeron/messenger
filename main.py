
import vk, sys, json, time

APP_ID = '4841859'

# TODO: add quequ adding
class FriendsList:
  def __init__(self, vkapi, id):
    self.api = vkapi
    self.id = id
  def build_list(self,id = None):
    if id == None:
      id = self.id
    friends = self.api('friends.get', user_id = self.id)['items']
    print(friends)
    return friends
class CommentPublicPosts:
    def __init__(self, vkapi, public_id,interval=1):
        self.api = vkapi
        self.public_id = public_id
        self.interval = interval
    def commentEveryPost(self,text_q):
        PostsList= self.api.wall.get(owner_id=-self.public_id,extended=1)
        time.sleep(1)
        for i in range(1,len(PostsList['items'])+1):
            self.api.wall.addComment(owner_id=-self.public_id,post_id=i,text=text_q)
            time.sleep(self.interval)
        return
    def commentPost(self,post_id,text_q):
        self.api.wall.addComment(owner_id=-self.public_id,post_id=post_id,text=text_q)
class GetTopNGroupsByLocation:
    def __init__(self,vkapi,city,n,search_text):
        self.api = vkapi
        self.cityName=city
        self.N=n
        self.searchText=search_text
    def getGroups(self):
        countries = self.api.database.getCountries(code="UA")
        country=countries['items'][0]
        cities = self.api.database.getCities(country_id=country['id'],q=self.cityName)
        city=cities['items'][0]
        groups=self.api.groups.search(q=self.searchText,city_id=city['id'])
        returnedGroups=[]
        if groups['count']<self.N:
            self.N=groups['count']
        for i in range(0,self.N+1):
            returnedGroups.append(groups['items'][i])
        return returnedGroups




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