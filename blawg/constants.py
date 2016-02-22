from __future__ import unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


TITLE_MAX_LENGTH = getattr(settings, 'BLAWG_TITLE_MAX_LENGTH', 100)

DESCRIPTION_MAX_LENGTH = getattr(settings,
                                 'BLAWG_DESCRIPTION_MAX_LENGTH', 200)

GUEST_NAME_MAX_LENGTH = getattr(settings, 'BLAWG_GUEST_NAME_MAX_LENGTH', 30)

FORBIDDEN_SLUGS = getattr(settings,
                          'BLAWG_FORBIDDEN_SLUGS', ['create',
                                                    'update', 'delete'])

SLUG_MODIFIER = getattr(settings, 'BLAWG_SLUG_MODIFIER', '-')

ERRORS = (
    _('Title is required'),
    _('Title must consist of '
      '{} characters maximum'.format(TITLE_MAX_LENGTH)),
    _('Description must consist of '
      '{} characters maximum'.format(DESCRIPTION_MAX_LENGTH)),
    _('Entry cannot be empty'),
)
