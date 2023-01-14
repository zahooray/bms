from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated



schema_view = get_schema_view(
    openapi.Info(
        title="project_name API",
        default_version="v1",
    ),
    public=True,
    url=settings.API_BASE_URL,
    permission_classes=(IsAuthenticated,),
    authentication_classes=(BasicAuthentication,),
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("admin/", admin.site.urls),
]

if settings.ENABLE_DEBUG_TOOLS:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("silk/", include("silk.urls", namespace="silk")),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
