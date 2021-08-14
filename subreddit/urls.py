from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index_page'),
    path('signup/',views.signup,name='signup_page'),
    path('login/',views.login,name='login_page'),
    path('logout/',views.logout,name='logout_page'),
    path('subreddit/new',views.subreddit_create,name='subreddit_create_page'),
    path('r/<str:pk>',views.subreddit,name='subreddit'),
    path('r/<str:pk>/submit',views.post,name='subreddit_post')
]