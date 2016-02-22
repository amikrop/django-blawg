from __future__ import unicode_literals

from django.conf.urls import url

from blawg.views import blog, comment, entry, date


urlpatterns = [
    url('^$', blog.IndexView.as_view(), name='index'),

    url('^create-comment/$',
        comment.CommentCreateView.as_view(), name='comment_create'),

    url('^update-comment/$',
        comment.CommentUpdateView.as_view(), name='comment_update'),

    url('^delete-comment/$',
        comment.CommentDeleteView.as_view(), name='comment_delete'),

    url('^create/$', blog.BlogCreateView.as_view(), name='blog_create'),

    url('^(?P<user>[\w\+\._@-]+)/$',
        blog.BlogListView.as_view(), name='blog_list'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/$',
        entry.EntryListView.as_view(), name='entry_list'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/update/$',
        blog.BlogUpdateView.as_view(), name='blog_update'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/delete/$',
        blog.BlogDeleteView.as_view(), name='blog_delete'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/create/$',
        entry.EntryCreateView.as_view(), name='entry_create'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/(?P<year>\d{4})/$',
        date.YearView.as_view(), name='entry_year'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/(?P<year>\d{4})/'
        '(?P<month>\d{2})/$',
        date.MonthView.as_view(month_format='%m'), name='entry_month'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/(?P<year>\d{4})/'
        '(?P<month>\d{2})/(?P<day>\d{2})/$',
        date.DayView.as_view(month_format='%m'), name='entry_day'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/(?P<entry>[\w-]+)/$',
        entry.EntryDetailView.as_view(), name='entry_detail'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/(?P<entry>[\w-]+)/update/$',
        entry.EntryUpdateView.as_view(), name='entry_update'),

    url('^(?P<user>[\w\+\._@-]+)/(?P<blog>[\w-]+)/(?P<entry>[\w-]+)/delete/$',
        entry.EntryDeleteView.as_view(), name='entry_delete'),
]
