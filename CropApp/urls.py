from django.urls import include, path
from rest_framework import routers
from .views import *
from .models import *

router = routers.DefaultRouter()
router.register(r'crops/category', CropsCategoryViewSet,
                basename='crops_category')
router.register(r'crops', CropsViewSet, basename='crops')
router.register(r'disease', DiseaseViewSet, basename='disease')


urlpatterns = [
    path('user/crops/archive/', ArchiveManagerAPIView.as_view(),
         name='archive_manager'),
] + router.urls
