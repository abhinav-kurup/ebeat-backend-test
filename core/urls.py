from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('authentication.urls')),
    # path('api/', include('app.urls')),
    # path('api/', include('articles.urls')),
    # path('api/', include('contract.urls')),
    # path('api/', include('mails.urls')),
    # path('api/', include('portfolio.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
