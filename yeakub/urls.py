from django.urls import path
from .import views


urlpatterns = [
    path('',views.home,name='home'),
    path('posts/',views.posts,name='posts'),
    path('all_posts', views.all_posts, name='all_posts'),
    path('post/<slug:slug>/',views.post,name='post'),
    # path('post/<str:pk>/',views.post,name='post'),
    path('profile/',views.profile,name='profile'),
    path('skill/', views.skills, name='skill'),
    path('otherskill/', views.otherskills, name='otherskill'),
    

    # CRUD PATHS
    path('create_post/', views.createPost, name='create_post'),
    path('update_post/<slug:slug>/', views.updatePost, name='update_post'),
    path('delete_post/<slug:slug>/', views.deletePost, name='delete_post'),


    # Email

    path('send_email/', views.sendEmail,name='send_email'),


    path('login/', views.loginPage, name="login"),
	path('register/', views.registerPage, name="register"),
	path('logout/', views.logoutUser, name="logout"),

	path('account/', views.userAccount, name="account"),
	path('update_profile/', views.updateProfile, name="update_profile"),

]