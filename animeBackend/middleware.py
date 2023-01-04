import rest_framework
from graphene_django.views import GraphQLView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.settings import api_settings


class DRFAuthenticatedGraphQLView(GraphQLView):
    # graphene expects .body attr but drf attaches to .data
    def parse_body(self, request):
        if type(request) is rest_framework.request.Request:
            return request.data
        return super().parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        #print(DRFAuthenticatedGraphQLView.__mro__)
        view = super(DRFAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((IsAuthenticated,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(['GET', 'POST'])(view)
        return view