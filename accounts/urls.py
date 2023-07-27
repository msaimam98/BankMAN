from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register/', views.SignupView.as_view(), name="register"),
    path('admin/', views.admin, name="admin"),
    path('delete/<int:pk>/', views.DeleteUserView.as_view(), name='delete'),
    path('logout/', views.logout, name="logout"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('profile/view/', views.profile, name="profile_view"),
    path('profile/edit/', views.ProfileEditView.as_view(), name="profile_edit"),
    
    
    
  
]
