import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings

user_model=settings.AUTH_USER_MODEL
print(user_model)


# User class remains unchanged, no need for MPTT in this case.
# -----------------------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required.")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        creat and  return a superuser with is staff and is_superuser set to True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        #if extra_fields.get('is_staff') is not True:
         #   raise ValueError('Superuser must have is_staff=True.')
        #if extra_fields.get('is_Superuser') is not True:
        #    raise ValueError('Superuser must have is_Superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # تغییر نام مرتبط به گروه‌ها
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # تغییر نام مرتبط به مجوزها
        blank=True
    )

    def __str__(self):
        return self.username
    
#profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

# -----------------------------------------
# Resume class with MPTTModel
# -----------------------------------------
class Resume(MPTTModel):
    parent = TreeForeignKey(
        "self", 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True, 
        related_name="children"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="resumes"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

# -----------------------------------------
# Other models
# -----------------------------------------

class Project(MPTTModel):
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_projects"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="projects"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']
    def __str__(self):
        return f"{self.title} - {self.user.username}"

# Repeat similarly for Application, Review, and Notification if they also require a parent field.
    
#class applications

class Application(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        'Project',  # ارتباط با جدول پروژه‌ها
        on_delete=models.CASCADE,
        related_name='applications'
    )
    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ارتباط با جدول کاربران
        on_delete=models.CASCADE,
        related_name='applications'
    )
    proposal = models.TextField()  # توضیح پیشنهاد فریلنسر
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # مبلغ پیشنهادی
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد درخواست

    def __str__(self):
        return f"Application for {self.project.title} by {self.freelancer.username}"
    
#class reviews

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="reviews_given"
    )
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="reviews_received"
    )
    project = models.ForeignKey(
        'Project', 
        on_delete=models.CASCADE, 
        related_name="reviews"
    )
    rating = models.PositiveIntegerField()  # امتیاز از 1 تا 5
    comment = models.TextField(blank=True, null=True)  # متن نظر
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد نظر

    def __str__(self):
        return f"Review by {self.user.username} for {self.target_user.username} on {self.project.title}"
    
#class notification

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="notifications"
    )
    message = models.TextField()  # متن اعلان
    is_read = models.BooleanField(default=False)  # وضعیت خوانده شدن
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد اعلان

    def __str__(self):
        return f"Notification for {self.user.username}: {'Read' if self.is_read else 'Unread'}"