from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (RedirectView, ListView,
                                  CreateView, UpdateView, DeleteView)
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _

from blawg.views.mixins import (OwnedMixin,
                                BlogFormMixin, BlogMixin,
                                OwnerRequiredMixin, DeletedMessageMixin)
from blawg.models import Blog


def _current_user_url(self):
    """Current user's blog list URL."""
    return reverse('blawg:blog_list',
                   kwargs={'user': self.request.user.username})


class IndexView(LoginRequiredMixin, RedirectView):
    """Index page."""
    get_redirect_url = _current_user_url


class BlogListView(OwnedMixin, ListView):
    """Blog list page."""
    model = Blog

    def get_queryset(self):
        """Get the blogs of a user, sorted by last entry date."""
        filters = {'user': self.user}
        if self.user != self.request.user:
            filters['public'] = True

        blogs = super(BlogListView, self).get_queryset().filter(**filters)
        blogs = blogs.annotate(last_entry_date=Max('entries__modified'))
        return blogs.order_by('-last_entry_date')


class BlogCreateView(BlogFormMixin, LoginRequiredMixin, CreateView):
    """Create a blog."""
    template_name_suffix = '_create'

    def form_valid(self, form):
        """Set blog's user."""
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        return HttpResponseRedirect(blog.get_absolute_url())


class BlogUpdateView(BlogMixin, BlogFormMixin,
                     OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update a blog."""
    template_name_suffix = '_update'
    success_message = _('Blog updated successfully')


class BlogDeleteView(BlogMixin, OwnerRequiredMixin,
                     DeletedMessageMixin, DeleteView):
    """Delete a blog."""
    model = Blog
    success_message = _('Blog deleted successfully')
    get_success_url = _current_user_url
