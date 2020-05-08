from blog.models import Post
from django import template
from django.db.models import Count

register = template.Library()

@register.simple_tag(name='my_tag')
def post_count():
    return Post.objects.count()


@register.inclusion_tag('blog/latest_post123.html')
def view_latest_post(count=3):
    latest_post = Post.objects.order_by('-publish')[:count]
    return {'latest_post':latest_post}

@register.simple_tag
def most_message_post(count=5):
    return Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]