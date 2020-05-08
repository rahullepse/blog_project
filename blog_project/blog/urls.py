from django.urls import path
from blog.views import all_blogs,view_blog,emailsend

urlpatterns = [
    path('allpost/',all_blogs),
    path('allpost/<tag_slug>/',all_blogs,name='post_by_tags'),
    path('detailpost/<int:year>/<int:month>/<int:day>/<post>/', view_blog,name='post_details'),
    path('sendmail/<int:id>/', emailsend),
]
