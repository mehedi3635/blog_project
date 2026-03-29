from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Comment

def register_view(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# block Crud

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('home')
    return render(request, 'create_post.html')


@login_required
def edit_post(request, id):
    post = Post.objects.get(id=id)
    if post.author == request.user:
        if request.method == "POST":
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.save()
            return redirect('home')
    return render(request, 'edit_post.html', {'post': post})


@login_required
def delete_post(request, id):
    post = Post.objects.get(id=id)
    if post.author == request.user:
        post.delete()
    return redirect('home')

# comment syestem

@login_required
def add_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        content = request.POST['content']
        Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('post_detail', post_id)


# Like Syestem

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', post_id)

# post details

def post_detail(request, id):
    post = Post.objects.get(id=id)
    comments = post.comments.all()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments
    })