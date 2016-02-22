from django.contrib import admin

from blawg.models import Entry, Blog, Comment


class EntryInline(admin.StackedInline):
    model = Entry
    readonly_fields = ['slug']
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [EntryInline]
    readonly_fields = ['slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified']
