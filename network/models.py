from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    user = models.ForeignKey(
    User,
    on_delete = models.CASCADE,
    related_name = "posts"
    )
    post = models.CharField(max_length= 200)
    created_at = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(
    Posts,
    on_delete = models.CASCADE,
    related_name = "comments"
    )
    author = models.ForeignKey(
    User,
    on_delete = models.CASCADE,
    related_name = "commented"
    )
class Likes(models.Model):
    post = models.ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    liker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["liker", "post"],
                name="unique_user_post_like",
            )
        ]

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow",
            )
        ]
