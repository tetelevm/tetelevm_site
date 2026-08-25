from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from .sitemaps import sitemaps
from .views import page_meta, robots_txt

urlpatterns = [
    path("robots.txt", robots_txt, name="robots-txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("_api/page-meta/", page_meta, name="page-meta"),
    path("_admin/", admin.site.urls),
    path("_api/auth/", include("apps.core.urls")),
    path("_api/", include("apps.projects.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
