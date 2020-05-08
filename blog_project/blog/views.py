from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.form import EmailSendForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.
def all_blogs(request,tag_slug=None):
    '''For Show all blog of codes'''
    post = Post.objects.all()

    #for tagging
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        post = post.filter(tags__in=[tag])

    #for pagination
    paginator = Paginator(post,2)
    page_number = request.GET.get('page')
    try:
        post=paginator.page(page_number)
    except PageNotAnInteger:
        post=paginator.page(1)
    except EmptyPage:
        post=paginator.page(paginator.num_pages)
    return render(request,'blog/blog.html',{'all_post':post,'tag':tag})


def view_blog(request,year,month,day,post):
    # print(year,'--',month,'--',day,'--',post)
    # detail_post = Post.objects.filter(slug=post)
    # print(detail_post)
    detail_post = get_object_or_404(Post,status='published',slug=post,publish__year=year,publish__month=month,publish__day=day)

    # '''For Comments section'''
    all_comments = detail_post.comments.all()
    csubmit = False
    if request.method=='POST':
        form =  CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = detail_post
            new_comment.save()
            csubmit = True
    else:
        form = CommentForm()

    return render(request,'blog/blog.html',{'post':detail_post,'form':form,'comments':all_comments,'csubmit':csubmit})


def emailsend(request,id):
    '''For Email Sending'''
    post = get_object_or_404(Post,status='published',id=id)
    sent = False
    if request.method=='POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommended you to read \'{}\''.format(data['name'],data['email'],post.title)
            message='Read Post At:\n{}\n\n{}\' Comments:\n{}'.format(post_url,data['name'],data['comments'])
            send_mail(subject,message,'bhawanalepse1@gmail.com',[data['to']])
            sent=True
            confirm_msg = 'Email Send Successfully'
            return render(request, 'blog/blog.html', {'sent': sent, 'post': post,'message':confirm_msg})
    else:
        form = EmailSendForm()
        return render(request,'blog/blog.html',{'form':form,'sent':sent,'email_post':post})