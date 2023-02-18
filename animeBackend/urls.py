from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# import graphene
from graphene_django.views import GraphQLView
from django.contrib import admin
from django.urls import path, include
from .middleware import DRFAuthenticatedGraphQLView
from socialLogin.views import GoogleLogin
# from anime.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("anime/", GraphQLView.as_view(graphiql=True)),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    path('auth/', include('dj_rest_auth.urls')),
    path("graphql/", DRFAuthenticatedGraphQLView.as_view(graphiql=True)),

]
