from rest_framework.routers import DefaultRouter
from .views import AdminViewSet

router = DefaultRouter()
router.register('admins', AdminViewSet, basename='admins')
#router.register('auth', AdminAuthView, basename='auth')


urlpatterns = router.urls
