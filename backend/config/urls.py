from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from emissions.views import EmissionViewSet

# REST API
router = DefaultRouter()
router.register(r'api/emissions', EmissionViewSet)

# Views
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
