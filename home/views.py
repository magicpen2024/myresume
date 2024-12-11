from django.contrib.auth import login,logout ,authenticate
from django.shortcuts import render, redirect
from .forms import  ReviewForm ,ResumeForm ,ProfileForm ,ProjectForm ,ApplicationForm
from .models import Resume ,Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm


# ویو برای صفحه اصلی
def home(request):
    return render(request, 'home/home.html')


### 1. ثبت‌نام (Registration View)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'حساب کاربری {username} با موفقیت ساخته شد!')
            return redirect('login')  # بعد از ثبت‌نام به صفحه لاگین می‌رویم
    else:
        form = CustomUserCreationForm()
    return render(request, 'home/register.html', {'form': form})


### 2. ورود (Login View)
# برای صفحه ورود



def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید!')
            return redirect('profile')  # بعد از ورود به پروفایل می‌رویم
    else:
        form = CustomAuthenticationForm()
    return render(request, 'home/login.html', {'form': form})


### 3. خروج (Logout View)

def logout_view(request):
    logout(request)  # خروج از سیستم
    messages.success(request, "با موفقیت از سیستم خارج شدید.")
    return redirect('home')  # بعد از خروج به صفحه خانه منتقل می‌شویم



### 4. پروفایل (Profile View)
@login_required
def profile(request):
    return render(request, 'home/profile.html')  # بعداً محتوای پروفایل اضافه میشود


@login_required
def edit_profile_view(request):
    # گرفتن پروفایل فعلی کاربر
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # بعد از ذخیره پروفایل به صفحه پروفایل میره
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/edit_profile.html', {'form': form})


### 5. رزومه‌ها (Resume Views)
#### ایجاد رزومه (Create Resume)


@login_required
def create_resume_view(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('profile')
    else:
        form = ResumeForm()

    return render(request, 'resumes/create_resume.html', {'form': form})

#### ویرایش رزومه (Edit Resume)

@login_required
def edit_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resumes/edit_resume.html', {'form': form})

#### حذف رزومه (Delete Resume)

@login_required
def delete_resume_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    resume.delete()
    return redirect('profile')

### 6. پروژه‌ها (Project Views)
#### ایجاد پروژه (Create Project)

@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('profile')
    else:
        form = ProjectForm()

    return render(request, 'projects/create_project.html', {'form': form})

### 7. درخواست‌ها (Applications View)

#### ایجاد درخواست

@login_required
def create_application_view(request, project_id):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.freelancer = request.user
            application.project_id = project_id
            application.save()
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, 'applications/create_application.html', {'form': form})

### 8. نظرات (Reviews View)
#### ایجاد نظر
@login_required
def create_review_view(request, project_id, target_user_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.target_user_id = target_user_id
            review.project_id = project_id
            review.save()
            return redirect('profile')
    else:
        form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'form': form})

### 9. اعلان‌ها (Notifications View)
#### مشاهده اعلان‌ها
@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notifications.html', {'notifications': notifications})
