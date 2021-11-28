from django.db import models

from django.contrib.auth import get_user_model
from ..core.models import BaseModel


User = get_user_model()


class Post(BaseModel):
    title = models.CharField(
        "Title",
        max_length=255,
        help_text="Title of the post.")
    body = models.TextField("body", help_text="Content of the post.")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='author',
        related_name='created_posts')

    def __str__(self) -> str:
        return self.title


class Comment(BaseModel):
    """Base models for comments."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss')
    body = models.TextField('body', help_text="Contents of the comment.")

    class Meta:
        abstract = True


class PostComment(Comment):
    """Model for comments on posts."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')

    class Meta:
        db_table = 'post_comment'

    def __str__(self) -> str:
        return f"{self.post}: {self.pk}"


class Like(BaseModel):
    """Base model for likes"""
    id = models.BigAutoField('Unique ID', primary_key=True, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss")

    class Meta:
        abstract = True


class PostLike(Like):
    """Likes on the post"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes")

    class Meta:
        db_table = 'post_like'


class PostCommentLike(Like):
    """Likes on the comment"""
    comment = models.ForeignKey(
        PostComment, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        db_table = 'postcomment_like'
