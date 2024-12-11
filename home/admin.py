from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Resume, Project, Application, Review, Notification
from django.contrib.auth import get_user_model
from django.conf import settings


print(settings.AUTH_USER_MODEL)
CustomUser=get_user_model
print(CustomUser)

# ثبت مدل سفارشی User
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'profile_picture', 'date_joined', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture', 'role', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# ثبت مدل Resume در پنل ادمین
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'parent')
    search_fields = ('title', 'user__username')
    list_filter = ('parent',)

# ثبت مدل Project در پنل ادمین
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'budget', 'status', 'created_at', 'deadline')
    search_fields = ('title', 'user__username')
    list_filter = ('status', 'user')

# ثبت مدل Application در پنل ادمین
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'amount', 'status', 'created_at')
    search_fields = ('project__title', 'freelancer__username')
    list_filter = ('status',)

# ثبت مدل Review در پنل ادمین
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'target_user', 'rating', 'created_at')
    search_fields = ('project__title', 'user__username', 'target_user__username')
    list_filter = ('rating',)

# ثبت مدل Notification در پنل ادمین
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_filter = ('is_read',)


