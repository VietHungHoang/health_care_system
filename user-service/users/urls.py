from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'manage', views.UserViewSet, basename='user-manage')

urlpatterns = [
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Profile endpoints
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('sessions/', views.UserSessionView.as_view(), name='user-sessions'),
    path('dashboard/', views.user_dashboard, name='user-dashboard'),
    
    # Admin endpoints
    path('', include(router.urls)),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
]