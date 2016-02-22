from __future__ import unicode_literals

from django.views.generic import (YearArchiveView,
                                  MonthArchiveView, DayArchiveView)

from blawg.views.mixins import DateMixin


class YearView(DateMixin, YearArchiveView):
    """Display the entries of a blog, by given year."""


class MonthView(DateMixin, MonthArchiveView):
    """Display the entries of a blog, by given month."""


class DayView(DateMixin, DayArchiveView):
    """Display the entries of a blog, by given day."""
