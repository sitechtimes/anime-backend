from django.test import TestCase
from .models import UserProfile, CustomUser, User
from snapshottest.django import TestCase
from animeBackend.schema import schema
from graphene.test import Client

# Create your tests here.

# class test_userProfile(TestCase):
#     def setUp(self):
#         self.custom_user = CustomUser(
#             email = "test@d.com"
#         )
#         self.custom_user.save()
#         self.user = UserProfile.objects.create(user = self.custom_user)
#         self.user.save()
        
#     def test(self):
#         self.user1 = UserProfile.objects.get(email="test@d.com")
#         print(self.user1.__dict__["_state"].__dict__)

class UserAnimeTestCase(TestCase):
    def test_update_user_anime(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
     mutation{
   updateUserAnime(userData: {userId: "2"}, userAnimeData: {animeName: "One Piece", watchStatus: "NOT_WATCHING"}){
       user{
           user{
               username,
               email,
            
           },
           userAnime {
             edges{
                 node{
                     anime{
                         id,
                         animeName,
                         episodes
                     },
                     rating,
                     watchingStatus
                 }
             }
           }
       }
    
   }
  
}
        '''))

