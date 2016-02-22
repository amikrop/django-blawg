from __future__ import unicode_literals

from django.views.generic import (DetailView, ListView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from blawg.views.mixins import (EntryMixin, PublicRequiredMixin,
                                EntryListMixin, BlogMixin, EntryFormMixin,
                                OwnerRequiredMixin, DeletedMessageMixin)
from blawg.utils import can_comment
from blawg import constants


class EntryDetailView(EntryMixin, PublicRequiredMixin, DetailView):
    """Entry detail page."""
    def get_context_data(self, **kwargs):
        """Pass comments and whether current user
        is allowed to comment.
        """
        context = super(EntryDetailView, self).get_context_data(**kwargs)
        context['nodes'] = self.entry.comments.all()
        context['can_comment'] = can_comment(self.request, self.entry)
        context['guest_name_max_length'] = constants.GUEST_NAME_MAX_LENGTH
        return context


class EntryListView(EntryListMixin, ListView):
    """Entry list page."""


class EntryCreateView(BlogMixin, EntryFormMixin,
                      LoginRequiredMixin, CreateView):
    """Create an entry."""
    template_name_suffix = '_create'

    def form_valid(self, form):
        """Set entry's blog."""
        entry = form.save(commit=False)
        entry.blog = self.blog
        entry.save()
        return HttpResponseRedirect(entry.get_absolute_url())


class EntryUpdateView(EntryMixin, EntryFormMixin,
                      OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an entry."""
    template_name_suffix = '_update'
    success_message = _('Entry updated successfully')


class EntryDeleteView(EntryMixin, OwnerRequiredMixin,
                      DeletedMessageMixin, DeleteView):
    """Delete an entry."""
    success_message = _('Entry deleted successfully')

    def get_success_url(self):
        """Blog's entry list URL."""
        return reverse('blawg:entry_list',
                       kwargs={'user': self.request.user.username,
                               'blog': self.kwargs['blog']})
