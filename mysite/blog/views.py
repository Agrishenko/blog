from django.shortcuts import render
from django.utils import timezone
from django .shortcuts import render, get_object_or_404
from .models import Post, Tag
from .forms import PostForm, TagsForm
from django.shortcuts import redirect
from .utils import ObjectDetai, ObjectCreate, ObjectEdit, ObjectDelete
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', {'tags': tags})


def post_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query))
    else:
        posts = Post.objects.all()

   # posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_pagination = page.has_other_pages()

    return render(request, 'blog/post_list.html', {'posts': page, 'is_pagination': is_pagination})


class PostDetail(ObjectDetai, View):
    model = Post
    templete = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreate, View):
    form_model = PostForm
    template = 'blog/post_create.html'
    templeteReturn = 'post_list'


class TagDetail(ObjectDetai, View):
    model = Tag
    templete = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, ObjectCreate, View):
    form_model = TagsForm
    template = 'blog/tag_create.html'
    templeteReturn = 'tags_list_url'


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(data=request.POST or None, files=request.FILES or None, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)


    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


class TagEdit(LoginRequiredMixin, ObjectEdit, View):
    model = Tag
    model_form = TagsForm
    template = 'blog/tag_edit.html'



class PostDelete(ObjectDelete, View):
    model = Post
    templete = 'blog/post_delete.html'
    templeteReturn = 'post_list'


class TagDelete(LoginRequiredMixin, ObjectDelete, View):
    model = Tag
    templete = 'blog/tag_delete.html'
    templeteReturn = 'tags_list_url'
