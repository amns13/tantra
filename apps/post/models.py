from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..core.models import BaseModel

User = get_user_model()


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_active=True, status=Post.PostStatusChoices.PUBLISHED).select_related('author')


class Post(BaseModel):
    class PostStatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        UNPUBLISHED = 'UNPUBLISHED', _('Unpublished')

    title = models.CharField(
        _("title"),
        max_length=255,
        help_text=_("Title of the post."))
    body = RichTextField(_("body"), help_text=_("Content of the post."))
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('author'),
        related_name='created_posts',
        to_field=settings.DEFAULT_FK_REFERENCE_FIELD)
    status = models.CharField(
        _("status"),
        max_length=31,
        choices=PostStatusChoices.choices,
        help_text=_("Current status of the post."),
        default=PostStatusChoices.PUBLISHED)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ('-pkid',)

    def __str__(self) -> str:
        return self.title


class Comment(BaseModel):
    """Base models for comments."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("author"),
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
