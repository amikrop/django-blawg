def can_comment(request, entry):
    """Check if current user is allowed to comment on that entry."""
    return entry.allow_comments and \
        (entry.allow_anonymous_comments or
         request.user.is_authenticated())
