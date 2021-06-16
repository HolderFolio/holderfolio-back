
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('api/v1/user/', include('app.user.api.v1.urls')),
    re_path('api/v1/portfolio/', include('app.portfolio.api.v1.urls')),
    re_path('api/v1/exchange/', include('app.exchange.api.v1.urls')),
    re_path('api/v1/asset/', include('app.assets.api.v1.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




