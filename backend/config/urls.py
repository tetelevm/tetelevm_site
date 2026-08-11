from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path("_admin/", admin.site.urls),
    path("_graphql/", csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG))),
]
