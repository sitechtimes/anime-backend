from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# import graphene
from graphene_django.views import GraphQLView
from django.contrib import admin
from django.urls import path
# from anime.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
]
