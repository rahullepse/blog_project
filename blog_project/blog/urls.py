from django.urls import path
from blog.views import all_blogs,view_blog,emailsend,CreatePost,SignUp,LogIn,LogOut
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',all_blogs,name='all_blogs'),
    path('allpost/<tag_slug>/',all_blogs,name='post_by_tags'),
    path('detailpost/<int:year>/<int:month>/<int:day>/<post>', view_blog,name='post_details'),
    path('sendmail/<int:id>/', emailsend),
    path('createblog/',login_required(CreatePost.as_view(template_name='blog/blog.html')),name='create'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/',LogIn.as_view(),name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
]
