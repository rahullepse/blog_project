from django.shortcuts import render,get_object_or_404
from blog.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.form import EmailSendForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import make_password
from django.views.generic.edit import ModelFormMixin

# Create your views here.
def all_blogs(request,tag_slug=None):
    request.session['username'] = request.user.username

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
    return render(request,'blog/blog.html',{'all_post':post,'tag':tag,'username':request.user.username})


def view_blog(request,year,month,day,post):
    username = request.session.get('username')

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

    return render(request,'blog/blog.html',{'post':detail_post,'form':form,'comments':all_comments,'csubmit':csubmit,'username':username})


def emailsend(request,id):
    username = request.session.get('username')

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
            return render(request, 'blog/blog.html', {'sent': sent, 'post': post,'message':confirm_msg,'username':username})
    else:
        form = EmailSendForm()
        return render(request,'blog/blog.html',{'form':form,'sent':sent,'email_post':post,'username':username})


# @login_required(function=LogIn,redirect_field_name='/login/')
class CreatePost(CreateView):
    model = Post
    fields = ('title','author','body','status','tags')
    template_name = 'blog/blog.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context.update({'createpost': 'createpost','username':self.request.session.get('username')})
        return context


class SignUp(CreateView):
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password')
    template_name = 'blog/blog.html'
    success_url = '/login/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.password = make_password('password')
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context.update({'signup': 'signup'})
        return context


class LogIn(auth_views.LoginView):
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LogIn, self).get_context_data(**kwargs)
        context.update({'login': 'login'})
        return context


class LogOut(auth_views.LogoutView):

    def get_context_data(self, **kwargs):
        context = super(LogOut, self).get_context_data(**kwargs)
        del self.request.session['username']
        context.update({'logout': 'logout'})
        return context



