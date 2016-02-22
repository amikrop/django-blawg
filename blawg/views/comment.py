from django.views.generic import CreateView, UpdateView, View
from django.http import JsonResponse, HttpResponse

from blawg.views.mixins import CommentMixin, AjaxBadRequest, CommentObjectMixin
from blawg.utils import can_comment


class CommentCreateView(CommentMixin, CreateView):
    """Create a comment."""
    fields = ['entry', 'parent', 'guest_name', 'content']

    def form_valid(self, form):
        """Make sure entry allows commenting for current user and
        parent comment belongs to entry. If current user is logged in
        set them as owner of the comment. Else, make sure `guest_name`
        is not empty. Return success page with newly created comment's
        primary key and creation datetime.
        """
        entry = form.cleaned_data['entry']
        parent = form.cleaned_data['parent']

        if not can_comment(self.request, entry) or \
           parent is not None and parent.entry != entry:
            raise AjaxBadRequest

        comment = form.save(commit=False)
        if self.request.user.is_authenticated():
            comment.user = self.request.user

        comment.save()
        return JsonResponse(
            {'pk': comment.pk,
             'created': comment.created.strftime('%d %b %Y, %H:%M')})


class CommentUpdateView(CommentObjectMixin, UpdateView):
    """Update a comment."""
    fields = ['content']

    def form_valid(self, form):
        """Make sure current user is owner of the comment.
        Save form and return success page with comment's
        last-modified datetime.
        """
        comment = form.instance
        if self.request.user != comment.user:
            raise AjaxBadRequest
        form.save()
        return JsonResponse(
            {'modified': comment.modified.strftime('%d %b %Y, %H:%M')})


class CommentDeleteView(CommentObjectMixin, View):
    """Delete a comment."""
    def post(self, request):
        """Make sure current user is owner if the comment or
        owner of the entry the comment belongs to. Delete comment
        and return empty success page.
        """
        comment = self.get_object()
        if request.user not in (comment.user, comment.entry.blog.user):
            raise AjaxBadRequest
        comment.delete()
        return HttpResponse()
