from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import ArticleForm, CommentForm
# DVDH
from django.views.decorators.http import require_POST
from IPython import embed
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    #embed()
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    # 1은 N을 보장할 수 없기 때문에 querySet(comment_set)형태로 조회해야한다.
    comments=article.comment_set.all()
    context = {
        'article': article,
        'comments':comments,
        'comment_form' : comment_form,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)

@login_required
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == "POST":
        article.delete()
        return redirect('articles:index')
    return redirect('articles:detail', article.pk)

@login_required
@require_POST
def comment_create(request,article_pk):
    #article = Article.objects.get(pk=article_pk)
    article=get_object_or_404(Article, pk=article_pk)

    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article=article
        #comment.article_id(자동으로 만들어줌) = article.pk
        comment.save()
        return redirect('articles:detail', article_pk)
    else:
        context={
            'comment_form' : comment_form,
            'article' : article
        }
    return redirect('articles:detail', context)

@login_required
@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment=get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect('articles:detail',article_pk)


 