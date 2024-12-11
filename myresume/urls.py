"""
URL configuration for myresume project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home ,name='home'),#صفحه اصلی
    path('login/', views.login_view, name='login'),  # مسیر لاگین
    path('logout/', views.logout_view, name='logout'),  # مسیر لاگ اوت
    path('register/', views.register, name='register'),  # مسیر ثبت‌نام
    path('profile/', views.profile, name='profile'),  # مسیر پروفایل
    path('profile/edit/',views.edit_profile_view , name='edit_profile'),
    path('resume/create/', views.create_resume_view, name='create_resume'),  # برای ایجاد رزومه
    path('resume/<int:pk>/edit/', views.edit_resume_view, name='edit_resume'),  # برای ویرایش رزومه
    path('resume/<int:pk>/delete/', views.delete_resume_view, name='delete_resume'),  # برای حذف رزومه
    path('prject/create/', views.create_project_view ,name='create_project'),
    path('notifications/',views.notifications_view , name='nitifications'),
    path('project/<int:project_id>/apply/', views.create_application_view ,name='create_application'),
    path('project/<int:project_id>/review/<int:target_user_id>/', views.create_review_view ,name='create_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
