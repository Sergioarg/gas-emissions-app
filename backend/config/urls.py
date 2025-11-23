from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from emissions.views import EmissionViewSet

# REST API
router = DefaultRouter()
router.register(r'api/emissions', EmissionViewSet)

# Views
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('api/token-auth/', obtain_auth_token, name='api-token-auth'),
]
