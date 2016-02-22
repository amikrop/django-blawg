from __future__ import unicode_literals

from django.utils.functional import cached_property
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from blawg.models import Blog, Entry, Comment
from blawg.constants import ERRORS as e


class OwnedMixin(object):
    """Provide `owner` to context and `user` property."""
    @cached_property
    def user(self):
        """Get user by URL argument and cache it.
        Raise 404 on failure.
        """
        return get_object_or_404(get_user_model(),
                                 username=self.kwargs['user'])

    def get_context_data(self, **kwargs):
        """Pass whether logged in user is the owner
        of the viewed object(s).
        """
        context = super(OwnedMixin, self).get_context_data(**kwargs)
        context['owner'] = self.user == self.request.user
        return context


class BlogMixin(OwnedMixin):
    """Provide `blog` to context, `blog` property and `get_object`."""
    @cached_property
    def blog(self):
        """Get blog from URL arguments and cache it.
        Raise 404 on failure.
        """
        return get_object_or_404(Blog, user=self.user,
                                 slug=self.kwargs['blog'])

    def get_object(self):
        """Get the `Blog` object."""
        return self.blog

    def get_context_data(self, **kwargs):
        """Pass blog."""
        context = super(BlogMixin, self).get_context_data(**kwargs)
        context['blog'] = self.blog
        return context


class EntryMixin(BlogMixin):
    """Provide `entry` to context,
    `entry` property and `get_object`.
    """
    model = Entry

    @cached_property
    def entry(self):
        """Get entry from URL arguments and cache it.
        Raise 404 in failure.
        """
        return get_object_or_404(Entry, blog=self.blog,
                                 slug=self.kwargs['entry'])

    def get_object(self):
        """Get the `Entry` object."""
        return self.entry

    def get_context_data(self, **kwargs):
        """Pass entry."""
        context = super(EntryMixin, self).get_context_data(**kwargs)
        context['entry'] = self.entry
        return context


class BlogFormMixin(object):
    """Behavior for blog form views."""
    model = Blog
    fields = ['title', 'description', 'public',
              'allow_comments', 'allow_anonymous_comments']

    def get_form(self):
        """Add custom error messages to blog form."""
        form = super(BlogFormMixin, self).get_form()
        form.fields['title'].error_messages = {'required': e[0],
                                               'max_length': e[1]}
        form.fields['description'].error_messages = {'max_length': e[2]}
        return form


class EntryFormMixin(object):
    """Behavior for entry form views."""
    model = Entry
    fields = ['title', 'content', 'public',
              'allow_comments', 'allow_anonymous_comments']

    def get_form(self):
        """Add custom error messages to entry form."""
        form = super(EntryFormMixin, self).get_form()
        form.fields['title'].error_messages = {'required': e[0],
                                               'max_length': e[1]}
        form.fields['content'].error_messages = {'required': e[3]}
        return form


class PublicRequiredMixin(object):
    """If the viewed object is not public,
    ensure that logged in user is the owner of it.
    """
    def get(self, request, **kwargs):
        if not self.get_object().public and self.user != request.user:
            return HttpResponseForbidden()

        return super(PublicRequiredMixin, self).get(request, **kwargs)


class OwnerRequiredMixin(LoginRequiredMixin):
    """Ensure that logged in user is the owner of the viewed object."""
    def dispatch(self, request, **kwargs):
        if self.user != request.user:
            return HttpResponseForbidden()

        return super(OwnerRequiredMixin, self).dispatch(request, **kwargs)


class EntryListMixin(BlogMixin, PublicRequiredMixin):
    """Enlist entries."""
    model = Entry

    def get_queryset(self):
        """Get the entries of the blog, sorted by creation date."""
        filters = {'blog': self.blog}
        if self.user != self.request.user:
            filters['public'] = True

        return super(EntryListMixin, self).get_queryset().filter(**filters)


class DeletedMessageMixin(object):
    """Add success message on delete."""
    def delete(self, request, **kwargs):
        messages.success(request, self.success_message)
        return super(DeletedMessageMixin, self).delete(request, **kwargs)


class DateMixin(EntryListMixin):
    """Behavior for date views."""
    date_field = 'created'
    make_object_list = True


class AjaxBadRequest(Exception):
    """User made an invalid AJAX request."""


class CommentMixin(object):
    """Behavior for comment views."""
    model = Comment

    @method_decorator(require_POST)
    def dispatch(self, request):
        """Only POST allowed. Return failure response if
        request is invalid.
        """
        try:
            return super(CommentMixin, self).dispatch(request)
        except AjaxBadRequest:
            return HttpResponseBadRequest

    def form_invalid(self, form):
        """Raise `AjaxBadRequest` if form is invalid."""
        raise AjaxBadRequest


class CommentObjectMixin(CommentMixin):
    """Behavior for comment object views."""
    def get_object(self):
        """Try to get object through POST data `pk`.
        Raise `AjaxBadRequest` on failure.
        """
        try:
            return Comment.objects.get(pk=self.request.POST.get('pk'))
        except (Comment.DoesNotExist, ValueError):
            raise AjaxBadRequest
