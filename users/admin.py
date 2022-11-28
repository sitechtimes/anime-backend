from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import UserAnime, CustomUser, UserProfile

admin.site.register(UserAnime)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile)