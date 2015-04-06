
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
class CommendPublicPosts:
    def __init__(self, vkapi, public_id):
        self.api = vkapi
        self.public_id = public_id
    def commentEveryPost(self,text_q):
        PostsList= self.api.wall.get(owner_id=-self.public_id,extended=1)
        time.sleep(1)
        for i in range(1,len(PostsList['items'])+1):
            self.api.wall.addComment(owner_id=-self.public_id,post_id=i,text=text_q+"#"+str(i))
            time.sleep(1)
        return
    def commentPost(self,post_id,text_q):
        self.api.wall.addComment(owner_id=-self.public_id,post_id=post_id,text=text_q)
class GetTopNGroupsByLocation: #will be finalized!!!!
    def __init__(self,vkapi):
        self.api = vkapi
    def getGroups(self,city,n):
        countries = self.api.database.getCountries(code="UA")
        print(countries['items'][0]['id'])





def init(json):
  for entry in json:
    vkapi = vk.API(APP_ID, entry["login"], entry["password"])
    vkapi.access_token = ""
    #a= CommendPublicPosts(vkapi,90318286).commendEveryPost("comment")
    #a= CommendPublicPosts(vkapi,90318286)
    #for i in range(1,50):
       # a.commentPost(2,"Morning test_comment for capthca #"+str(i))
       # time.sleep(1)
    a=GetTopNGroupsByLocation(vkapi)
    a.getGroups('Kiev', 1)
    #vkapi.wall.addComment(owner_id=-90318286,post_id=1,text="test comment")
    #vkapi.wall.post(message="Hello")
    #id = vkapi("users.get")[0]['id']
    #friendlist = FriendsList(vkapi, id).build_list()
    #for friend in friendlist:
        #FriendsList(vkapi,friend).build_list()
        #time.sleep(1)





if __name__ == '__main__':
  path = 'credentials.json'
  if len(sys.argv) > 1:
    path = sys.argv[1]
  text = open(path, 'r').read()
  json = json.loads(text)
  init(json)