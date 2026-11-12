from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Posts, Likes, Follow
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Exists, OuterRef, Value, BooleanField, Count
from django.core.paginator import Paginator

def index(request):
    if request.user.is_authenticated:
        posts = Posts.objects.annotate(
            liked_by_user=Exists(
                Likes.objects.filter(
                    post=OuterRef("pk"),
                    liker=request.user
                )
            )
        )
    else:
        posts = Posts.objects.annotate(
            liked_by_user=Value(False, output_field=BooleanField())
        )

    posts = posts.order_by("-created_at")

    p = Paginator(posts, 10)
    page_obj = p.get_page(request.GET.get("page"))
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def post(request):
    if request.method == "POST":
        text = request.POST["post"]
        post = Posts(
            post=text,
            user= request.user
        )
        post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def likes(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Posts, id=post_id)
        liked =Likes.objects.filter(
        post=post,
        liker=request.user
        ).exists()

        if liked:
            Likes.objects.filter(
                post=post,
                liker = request.user
            ).delete()
            liked = False
        else:
            Likes.objects.create(
                post= post,
                liker = request.user
            )
            liked = True

        count = post.likes.count()
        return JsonResponse({
                "liked": liked,
                "count": count
                })
    else:
        response = render(request, "405.html", status=405)
        response["Allow"] = "POST"
        return response



def profile(request, page_id):
    profile_user = get_object_or_404(User, id=page_id)

    posts = Posts.objects.filter(user=profile_user)

    if request.user.is_authenticated:
        posts = posts.annotate(
            liked_by_user=Exists(
                Likes.objects.filter(
                    post=OuterRef("pk"),
                    liker=request.user
                )
            )
        )
    else:
        posts = posts.annotate(
            liked_by_user=Value(False, output_field=BooleanField())
        )

    posts = posts.order_by("-created_at")

    followed = False

    if request.user.is_authenticated:
        followed = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, "network/page.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followed": followed,
    })


@login_required
def follow(request, page_id):
    if request.method == "POST":
        profile_user = get_object_or_404(User, id=page_id)
        followed = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

        if followed:
            Follow.objects.filter(
                follower = request.user,
                following = profile_user
            ).delete()
            followed = False
        else:
            Follow.objects.create(
                follower=request.user,
                following=profile_user
            )
            followed = True

        followers_count = profile_user.followers.count()
        following_count = profile_user.following.count()

        return JsonResponse({
            "followed" : followed,
            "followers_count": followers_count,
            "following_count": following_count
        })
    else:
        response = render(request, "405.html", status=405)
        response["Allow"] = "POST"
        return response


@login_required
def following(request):
    followed_users = Follow.objects.filter(
        follower=request.user
    ).values("following")

    posts = Posts.objects.filter(user__in=followed_users).annotate(
        liked_by_user=Exists(
            Likes.objects.filter(
                post=OuterRef("pk"),
                liker=request.user
            )
        ),
        like_count=Count("likes")
    ).order_by("-created_at")

    return render(request, "network/following.html", {
        "posts": posts
    })


@login_required
def edit(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(
            Posts,
            id=post_id,
            user=request.user
        )

        updated_post = request.POST.get("post")

        post.post = updated_post
        post.save()

        return JsonResponse({"post": post.post})

    else:
        response = render(request, "405.html", status=405)
        response["Allow"] = "POST"
        return response
