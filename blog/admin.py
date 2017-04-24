from django.contrib import admin
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    fieldsets =  [
        (None, {'fields': ['slug','body','html_body','snippet'],'classes':['collapse']}),
        ('主要',{'fields':['title','md_file','tags','publish']}),
        ('详细', {'fields':['author','subtitle','status'],'classes':['collapse']}),
    ]

admin.site.register(Article, ArticleAdmin)
