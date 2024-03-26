from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .models import Post, Comment

from django.contrib.auth import get_user_model

from main.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.http import JsonResponse, HttpResponseBadRequest



@login_required
def editprofile(request):
    return render(request, "socialmedia/editprofile.html", {})


@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_on')
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
        try:
            new_post.save()
            print("===>>", "Post Saved")
            
        except Exception as e:
            print(e)
            print("===>>", "Post Not Saved")

    user = User.objects.get(id=request.session["user_id"])
    userInformation = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "profile_picture": user.profile_picture
    }
    context = {
        'post_list': page_obj,
        'form': form,
        'user': userInformation,
        'page_obj': page_obj
    }
    return render(request, 'socialmedia/post_list.html', context)



@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

    comments = Comment.objects.filter(post=post).order_by('-created_on')

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'socialmedia/post_detail.html', context)

@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post-detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'socialmedia/post_edit.html', context)

@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post-list')

    if request.method == 'POST':
        post.delete()
        return redirect('post-list')

    context = {
        'post': post,
    }
    return render(request, 'socialmedia/post_delete.html', context)


@login_required
def add_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        is_like = request.user in post.likes.all()
        is_dislike = request.user in post.dislikes.all()

        if is_like:
            post.likes.remove(request.user)
            liked = False
        else:
            if is_dislike:
                post.dislikes.remove(request.user)
            post.likes.add(request.user)
            liked = True

        like_count = post.likes.all().count()
        dislike_count = post.dislikes.all().count()

        return JsonResponse({'like_count': like_count, 'dislike_count': dislike_count, 'liked': liked})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_dislike(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        is_like = request.user in post.likes.all()
        is_dislike = request.user in post.dislikes.all()

        if is_dislike:
            post.dislikes.remove(request.user)
            disliked = False
        else:
            if is_like:
                post.likes.remove(request.user)
            post.dislikes.add(request.user)
            disliked = True

        like_count = post.likes.all().count()
        dislike_count = post.dislikes.all().count()

        return JsonResponse({'like_count': like_count, 'dislike_count': dislike_count, 'disliked': disliked})
    else:
        return HttpResponseBadRequest()


@login_required
def add_comment_like(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    is_dislike = False

    for dislike in comment.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break

    if is_dislike:
        comment.dislikes.remove(request.user)

    is_like = False

    for like in comment.likes.all():
        if like == request.user:
            is_like = True
            break

    if not is_like:
        comment.likes.add(request.user)

    if is_like:
        comment.likes.remove(request.user)

    next_url = request.POST.get('next', '/')
    return redirect(next_url)


@login_required
def add_comment_dislike(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    is_like = False

    for like in comment.likes.all():
        if like == request.user:
            is_like = True
            break

    if is_like:
        comment.likes.remove(request.user)

    is_dislike = False

    for dislike in comment.dislikes.all():
        if dislike == request.user:
            is_dislike = True
            break

    if not is_dislike:
        comment.dislikes.add(request.user)

    if is_dislike:
        comment.dislikes.remove(request.user)

    next_url = request.POST.get('next', '/')
    return redirect(next_url)

@login_required
def comment_reply_view(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    parent_comment = get_object_or_404(Comment, pk=pk)
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()
            return redirect('post-detail', pk=post_pk)

    context = {
        'form': form,
        'post': post,
        'parent_comment': parent_comment,
    }
    return render(request, 'social/comment_reply.html', context)