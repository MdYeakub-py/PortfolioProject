from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .decorators import *

from .models import Post, PostComment, Skills, OtherSkill
from .forms import PostForm, CustomUserCreationForm, ProfileForm, UserForm, SkillsForm, OtherSkillsForm
from .filters import PostFilter

# Create your views here.


def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]
    my_data = Skills.objects.all()
    otherskill = OtherSkill.objects.all()
    context = {'posts': posts,'skills': my_data,'otherskill': otherskill}
    
    return render(request, 'base/index.html', context)


def posts(request):
    posts = Post.objects.filter(active=True)

    # Search or filter
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    # pagination
    page = request.GET.get('page')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # posts = Post.objects.all()
    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, 'base/posts.html', context)


def all_posts(request):
    return render(request, 'base/all_posts.html')


def post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect('post', slug=post.slug)

    context = {'post': post}
    return render(request, 'base/post.html', context)


def profile(request):
    return render(request, 'base/profile.html')


# CRUD VIEWs

@login_required(login_url="home")
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('account')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="home")
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
# def updatePost(request, pk):
#     post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="home")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item': post}
    return render(request, 'base/delete.html', context)

    # Email


def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('base/email.html', {
            'name': request.POST['name'],
            'subject': request.POST['subject'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['yeakub161736@gmail.com']
        )
        email.fail_silently = False
        email.send()
    return render(request, 'base/email_sent.html')


# login information

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Little Hack to work around re-building the usermodel
        try:
            user = User.objects.get(email=email)
            user = authenticate(
                request, username=user.username, password=password)
        except:
            messages.error(request, 'User with this email does not exists')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email OR password is incorrect')

    context = {}
    return render(request, 'base/login.html', context)


def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account successfuly created!')

            user = authenticate(request, username=user.username,
                                password=request.POST['password1'])

            if user is not None:
                login(request, user)

            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'An error has occured with registration')
    context = {'form': form}
    return render(request, 'base/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url="home")
def userAccount(request):
    profile = request.user.profile

    context = {'profile': profile}
    return render(request, 'base/account.html', context)


@login_required(login_url="home")
def updateProfile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'base/profile_form.html', context)


# For Skills add

def skills(request):
    skill = SkillsForm()

    if request.method == 'POST':
        skill = SkillsForm(request.POST, request.FILES)
        if skill.is_valid():
            skill.save()
            messages.success(request, 'Successfuly add Skill!')
            return redirect('skill')
        else:
            messages.error(request, 'An error has occured with Add Skill')
    my_data = Skills.objects.all()
        
    context = {'skill': skill, 'skills': my_data}
    return render(request, 'base/add_skills.html', context)


# For Other Skills add
def otherskills(request):
    otherskill = OtherSkillsForm()

    if request.method == 'POST':
        otherskill = OtherSkillsForm(request.POST, request.FILES)
        if otherskill.is_valid():
            otherskill.save()
            messages.success(request, 'Successfuly add Skill!')
            return redirect('otherskill')
        else:
            messages.error(request, 'An error has occured with Add Skill')
    my_data = OtherSkill.objects.all()
        
    context = {'otherskill': otherskill, 'otherskills': my_data}
    return render(request, 'base/other_skill.html', context)

