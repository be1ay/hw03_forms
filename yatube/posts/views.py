from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import Post, Group, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    user_posts = author.posts.all()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts_count': user_posts.count,
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_posts = Post.objects.filter(author__username=post.author)
    context = {
        'post': post,
        'user_posts': user_posts
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
        context = {
            'form': form
        }
        return render(request, 'posts/create_post.html', context)
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    
    if author != request.user:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit,
            'post_id': post_id
        }
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
        return render(request, 'posts/create_post.html', context)
    elif request.method == 'GET':
        form = PostForm(instance=post)
        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit,
            'post_id': post_id
        }
        return render(request, 'posts/create_post.html', context)

    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})