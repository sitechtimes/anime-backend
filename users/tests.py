from django.test import TestCase
from .models import UserProfile, CustomUser, User

# Create your tests here.

class test_userProfile(TestCase):
    def setUp(self):
        self.custom_user = CustomUser(
            email = "test@d.com"
        )
        self.custom_user.save()
        self.user = UserProfile.objects.create(user = self.custom_user)
        self.user.save()
        
    def test(self):
        self.user1 = UserProfile.objects.get(id=1)
        print(self.user1.__dict__["_state"].__dict__)
