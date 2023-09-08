from django.urls import path
from blog import views


urlpatterns = [
    path('postComment',views.postComment,name='postComment'),
    path('bloghome',views.bloghome,name='bloghome'),
    path('<str:slug>',views.blogpost,name='blogpost'),
]