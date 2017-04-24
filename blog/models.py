import os

import re

import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
from unidecode import unidecode

from markdown2 import markdown


def get_path(instance, filename):
    path = os.path.join('blog_md', str(instance.publish.year), str(instance.publish.month), str(instance.publish.day))
    file_path = os.path.join(settings.MEDIA_ROOT, path, filename.replace(' ', '_'))
    if os.path.exists(file_path):
        os.remove(file_path)
    return file_path


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    author = models.ForeignKey(User, related_name='article', default='1')

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish', blank=True)
    body = models.TextField(blank=True)  # Markdown format
    html_body = models.TextField(blank=True)
    snippet = models.TextField(blank=True)  # HTML format
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    objects = models.Manager()  # The default manager
    published = PublishedManager()

    tags = TaggableManager(blank=True)

    md_file = models.FileField(upload_to=get_path, blank=True)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.publish.year,
                                                    self.publish.strftime('%m'),
                                                    self.publish.strftime('%d'),
                                                    self.slug])

    def save(self, *args, **kwargs):
        '''
        slug: slugified title (Chinese to Pinyin) 
        body: read from md_file 
        html_body: transformed from Markdown file
        snippet: above the <!-- more --> tag 
        '''

        # slug: slugified title (Chinese to Pinyin)
        self.slug = slugify(unidecode(self.title))

        # body: read from md_file (Markdown format)
        if self.md_file:
            self.body = self.md_file.read()

        # snippet: FROM BODY(Markdown) => HTML
        # body should be utf-8 encoding or unicode because we use regex
        if type(self.body) == bytes:
            body = self.body.decode('utf-8')
        elif type(self.body) == str:
            body = self.body

        # find <!-- more --> tag to get the snippet
        # if no this tag, snippet would be full text
        res = re.search('(.*?)<!-- more -->', body, re.S)
        if res:
            snippet = res.group(1)
        else:
            snippet = body

        # snippet encoding go back to utf-8 to render into html format

        snippet = snippet.encode('utf-8')

        self.snippet = markdown(snippet, extras=['fenced-code-blocks'])

        # body
        if type(self.body) == str:
            self.body = self.body.encode('utf-8')

        self.html_body = markdown(self.body, extras=['fenced-code-blocks'])


        super(Article, self).save(*args, **kwargs)


