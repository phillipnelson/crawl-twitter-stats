import twitter2
from config.twitter import CREDENTIALS

'''
Here we cycle through twitter credentials whenever we receive an authentication error.
'''

class MyTwitterApi(twitter2.Api):
    
    def __init__(self,**credentials):
        self._current_credentials = credentials
        return super(MyTwitterApi, self).__init__(**credentials)
    
    def GetFriendIDs(self,user=None,cursor=None):
        try:
            return super(MyTwitterApi, self).GetFriendIDs(user=user,cursor=cursor)
        except twitter2.TwitterError as exc:
            print exc
            if not 'Not authorized' in str(exc):
                self._rotateCredentials()
                return self.GetFriendIDs(user=user,cursor=cursor)
            else:
                raise exc
    
    def GetFollowerIDs(self,userid=None,cursor=None):
        try:
            return super(MyTwitterApi, self).GetFollowerIDs(userid=userid,cursor=cursor)
        except twitter2.TwitterError as exc:
            print exc
            if not 'Not authorized' in str(exc):
                self._rotateCredentials()
                return self.GetFollowerIDs(userid=userid,cursor=cursor)
            else:
                raise exc
            
    def GetUser(self,username):
        try:
            return super(MyTwitterApi, self).GetUser(username)
        except:
            self._rotateCredentials()
            return self.GetUser(username)

    def UsersLookup(self,user_id=None,screen_name=None,users=None):
        try:
            return super(MyTwitterApi, self).UsersLookup(user_id=user_id,screen_name=screen_name,users=users)
        except twitter2.TwitterError as exc:
            print exc
            if not 'Not authorized' in str(exc):
                self._rotateCredentials()
                return self.UsersLookup(user_id=user_id,screen_name=screen_name,users=users)
            else:
                raise exc

    def _rotateCredentials(self):
        print "Rotating Credentials."
        self.SetCredentials(**CREDENTIALS.pop())

twitter_api = MyTwitterApi()
