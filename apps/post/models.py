from core.models import BaseModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Post(BaseModel):
    title = models.CharField(
        _("Title"),
        max_length=255,
        help_text=_("Title of the post."))
    body = models.TextField(_("body"), help_text=_("Content of the post."))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='created_posts',
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)

    def __str__(self) -> str:
        return self.title


class Comment(BaseModel):
    """Base models for comments."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)
    body = models.TextField('body', help_text=_("Contents of the comment."))

    class Meta:
        abstract = True


class PostComment(Comment):
    """Model for comments on posts."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)

    class Meta:
        db_table = 'post_comment'

    def __str__(self) -> str:
        return f"{self.post}: {self.pk}"


class Like(BaseModel):
    """Base model for likes"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)

    class Meta:
        abstract = True


class PostLike(Like):
    """Likes on the post"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)

    class Meta:
        db_table = 'post_like'


class PostCommentLike(Like):
    """Likes on the comment"""
    comment = models.ForeignKey(
        PostComment,
        on_delete=models.CASCADE,
        related_name="likes",
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)

    class Meta:
        db_table = 'postcomment_like'
