from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
from autoslug.settings import slugify
from mptt.models import MPTTModel, TreeForeignKey

from blawg import constants


class TimestampedModel(models.Model):
    """Stores creation datetime and last-modified datetime."""
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_('creation datetime'))
    modified = models.DateTimeField(auto_now=True,
                                    verbose_name=_('last-modified datetime'))

    class Meta:
        abstract = True


@python_2_unicode_compatible
class PostedModel(models.Model):
    """Stores title, whether public, whether allow comments
    and whether allow anonymous comments.
    """
    title = models.CharField(max_length=constants.TITLE_MAX_LENGTH,
                             verbose_name=_('title'))
    public = models.BooleanField(default=True, verbose_name=_('public'))
    allow_comments = models.BooleanField(default=True,
                                         verbose_name=_('allow comments'))
    allow_anonymous_comments = models.BooleanField(
        default=True,
        verbose_name=_('allow anonymous comments'))

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """If `public` is `False`, `allow_comments` must be `False` too.
        If `allow_comments` is `False`, `allow_anonymous_comments`
        must be `False` too.
        """
        if not self.public:
            self.allow_comments = False
        if not self.allow_comments:
            self.allow_anonymous_comments = False
        return super(PostedModel, self).save(*args, **kwargs)


def _four_digit(string):
    """Check if string is a four-digit integer."""
    try:
        return len(string) == 4 and int(string) == float(string)
    except ValueError:
        return False


def _make_slug(title):
    """Make a slug, avoiding to use a "forbidden slug" title
    and a four-digit integer (to avoid clashing with years).
    """
    if title in constants.FORBIDDEN_SLUGS or _four_digit(title):
        title += constants.SLUG_MODIFIER
    return slugify(title)


class Blog(TimestampedModel, PostedModel):
    """Blog, belonging to a user."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='blogs', verbose_name=_('user'))
    slug = AutoSlugField(populate_from='title', unique_with='user',
                         slugify=_make_slug, verbose_name=_('slug'))
    description = models.CharField(
        max_length=constants.DESCRIPTION_MAX_LENGTH,
        blank=True, verbose_name=_('description'))

    class Meta:
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def get_absolute_url(self):
        return reverse('blawg:entry_list',
                       kwargs={'user': self.user.username,
                               'blog': self.slug})


class Entry(TimestampedModel, PostedModel):
    """Entry, belonging to a blog."""
    blog = models.ForeignKey('Blog',
                             related_name='entries', verbose_name=_('blog'))
    slug = AutoSlugField(populate_from='title', unique_with='blog',
                         slugify=_make_slug, verbose_name=_('slug'))
    content = models.TextField(verbose_name=_('content'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def get_absolute_url(self):
        return reverse('blawg:entry_detail',
                       kwargs={'user': self.blog.user.username,
                               'blog': self.blog.slug,
                               'entry': self.slug})


@python_2_unicode_compatible
class Comment(MPTTModel, TimestampedModel):
    """Comment, belonging to an entry. Made by a user,
    possibly an anonymous one. May have a parent comment.
    """
    entry = models.ForeignKey('Entry',
                              related_name='comments',
                              verbose_name=_('entry'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments',
                             blank=True, null=True, verbose_name=_('user'))
    parent = TreeForeignKey('self',
                            related_name='children',
                            blank=True, null=True,
                            db_index=True, verbose_name=_('parent comment'))
    guest_name = models.CharField(max_length=constants.GUEST_NAME_MAX_LENGTH,
                                  blank=True,
                                  verbose_name=_('name of anonymous user'))
    content = models.TextField(verbose_name=_('content'))

    class Meta:
        ordering = ['-created']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    class MPTTMeta:
        order_insertion_by = ['-created']

    def __str__(self):
        if len(self.content) > 30:
            return self.content[:27] + '...'
        return self.content

    def save(self, *args, **kwargs):
        """If comment belongs to a registered user,
        empty `guest_name`.
        """
        if self.user is not None:
            self.guest_name = ''
        super(Comment, self).save(*args, **kwargs)
