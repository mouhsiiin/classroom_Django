from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .models import Post, Comment

from django.contrib.auth import get_user_model

from main.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.http import JsonResponse, HttpResponseBadRequest

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def editprofile(request):
    if request.method == 'POST':
        # Récupérer l'utilisateur actuellement connecté
        user = request.user
        
        # Récupérer les données envoyées dans le formulaire
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')
        resume = request.FILES.get('resume')

        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if bio:
            user.bio = bio
        if profile_picture:
            user.profile_picture = profile_picture
        if resume:
            user.resume = resume

        user.save()
        return redirect('socialmedia:profile', username=user.username)
    else:
        return render(request, 'socialmedia/editprofile.html')
        
def landing(request):
    students_counts = User.objects.filter(role='student').count()
    teachers_counts = User.objects.filter(role='teacher').count()
    posts_counts = Post.objects.all().count()

    context = {
        'students_counts': students_counts,
        'teachers_counts': teachers_counts,
        'posts_counts': posts_counts,
    }
    return render(request, 'socialmedia/landing.html', context)



def profile(request, username):
    target_user = get_object_or_404(User, username=username)
    userInformation = {
        "username": target_user.username,
        "email": target_user.email,
        "role": target_user.role,
        "first_name": target_user.first_name,
        "last_name": target_user.last_name,
        "bio": target_user.bio,
        "profile_picture": target_user.profile_picture
    }

    posts = Post.objects.filter(author=target_user).order_by('-created_on')

    context = {
        'curr_profile': userInformation,
        'post_list': posts,
    }
    return render(request, 'socialmedia/profile.html', context)

@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_on')
    paginator = Paginator(posts, 15)  # Set the number of posts per page

    page_number = request.GET.get('page', 1)  # Get the current page number, default to 1

    try:
        page_obj = paginator.page(page_number)
    except:
        pass
    # except PageNotAnInteger:
    #     page_obj = paginator.page(1)
    # except EmptyPage:
    #     page_obj = paginator.page(paginator.num_pages)

    pages = {
        'page_obj': page_obj,
        'page_number': page_number,
        'num_pages': paginator.num_pages,  # Add the total number of pages
    }


    if request.method == 'POST':
        text = request.POST.get('body')
        
        print("===>>", text)
        if text:
            new_post = Post(body=text, author=request.user)
            if request.FILES.get('media'):
                file = request.FILES.get('media')
                print("===>>", file.content_type)
                #check if the file is an image
                if file.content_type.startswith('image'):
                    new_post.image = file
                #check if the file is a video
                elif file.content_type.startswith('video'):
                    new_post.video = file
        try:
            new_post.save()
            print("===>>", "Post Saved")
            
        except Exception as e:
            print(e)
            print("===>>", "Post Not Saved")
    try:
        user = User.objects.get(id=request.session["user_id"])
    except:
        return redirect('logout')
    userInformation = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user.bio,
        "profile_picture": user.profile_picture
    }
    context = {
        'post_list': page_obj,
        'user': userInformation,
        'pages': pages,
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
            return redirect('socialmedia:post-detail', pk=pk)
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
        return redirect('socialmedia:post-list')

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


@login_required
def picture_upload(request):
    user = User.objects.get(id=request.session["user_id"])
    if request.method == 'POST':
        #get the uploaded image from the request body
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        
        return JsonResponse({'profile_picture': user.profile_picture.url})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

#view for getting comments as json
@login_required
def get_comments(request, post_pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_pk)
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        comments_list = list()
        for comment in comments:
            replies = []
            for comet in comments:
                if comet.parent == comment:
                    replies.append({
                        'id': comet.id,
                        'author': comet.author.username,
                        'content': comet.comment,
                        'created_on': comet.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                        'likes': comet.likes.all().count(),
                        'dislikes': comet.dislikes.all().count(),
                        'replies': []
                    })
                comments_list.append({
                    'id': comment.id,
                    'author': comment.author.username,
                    'content': comment.comment,
                    'created_on': comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                    'likes': comment.likes.all().count(),
                    'dislikes': comment.dislikes.all().count(),
                    'replies': replies
                })

                return JsonResponse({'comments': comments_list})
        return JsonResponse({'error' : 'No comments found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

#view for adding comments
@login_required
def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(
                author=request.user,
                post=post,
                content=content
            )
            return JsonResponse({
                'id': comment.id,
                'author': comment.author.username,
                'content': comment.content,
                'created_on': comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                'likes': comment.likes.all().count(),
                'dislikes': comment.dislikes.all().count(),
                'replies': []
            })
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def search(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        print(query)
        if query:
            posts = Post.objects.filter(body__icontains=query)
            profiles = User.objects.filter(username__icontains=query)
        else:
            #getiing the first 10 posts
            posts = Post.objects.all().order_by('-created_on')[:10]
            profiles = User.objects.all()[:10]
        context = {
            'posts': posts,
            'profiles': profiles,
            'query': query,
        }
        return render(request, 'socialmedia/search.html', context)
    else:
        return redirect('post-list')