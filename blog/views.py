import redis
from collections import defaultdict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Count
from django.conf import settings
from taggit.models import Tag

from .models import Article
from taggit.models import Tag


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def article_list(request, tag_slug=None):
    object_list = Article.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'current_page': page,
                                                   'pages': range(1, paginator.num_pages + 1),
                                                   'posts': posts,
                                                   'tag': tag})


def article_detail(request, year, month, day, post):
    post = get_object_or_404(Article, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def tag_detail(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Article.published.filter(tags__in=[tag])
    return render(request, 'blog/post/tag.html', {'tag': tag, 'posts': posts})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/post/tags.html', {'tags': tags})


def archives(request):
    posts_by_year = defaultdict(list)
    articles = Article.published.all()
    for article in articles:
        year = article.publish.year
        posts_by_year[year].append(article)
    posts_by_year = sorted(posts_by_year.items(), reverse=True)
    return render(request, 'blog/post/archives.html', {'posts':posts_by_year})


def aboutme(request):
    about_article = get_object_or_404(Article, status='draft', title='about')
    like_count= r.get('like')
    return render(request, 'blog/post/about.html', {'post': about_article, 'like_count': like_count})


def like(request):
    total_likes = r.incr('like')
    return JsonResponse({'like_count':total_likes})

