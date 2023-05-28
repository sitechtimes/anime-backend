from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# import graphene
from graphene_django.views import GraphQLView
from django.contrib import admin
from django.urls import path, include
from .middleware import DRFAuthenticatedGraphQLView
from socialLogin.views import GoogleLogin
from django.contrib.auth.views import LogoutView
from anime.views import AnimeView, GenreView, UpdateAnimeView
# from anime.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("anime/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/', include('dj_rest_auth.urls')),
    path("graphql/", DRFAuthenticatedGraphQLView.as_view(graphiql=True)),
    path('anime/', AnimeView.as_view()),
    path("genres/", GenreView.as_view()),
    path("updateAnime/", UpdateAnimeView.as_view())
    # path('logout/', LogoutView.as_view()),

]
