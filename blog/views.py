from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views import generic
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import CommentForm, PostForm
from .models import Post, Category
from users.models import Profile


class PageTitleViewMixin:
    """
    Create page titel that injects page titel varibale
    into the template
    Code found here:
    https://www.forgepackages.com/guides/page-titles/
    """

    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class SuperuserFieldsMixin:
    """
    Allowes only the Admin to set the Post to featured
    """

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields.pop("featured", None)
        return form


class PostFormInvalidMessageMixin:
    def form_invalid(self, form):
        messages.error(
            self.request,
            "Your post could not be submitted. Please review your inputs!",
        )
        return super().form_invalid(form)


class HomeListView(PageTitleViewMixin, generic.ListView):
    """
    Render featured posts on home page
    """

    model = Post
    title = "Home"
    queryset = Post.objects.filter(featured=True, status=1).order_by(
        "-created_on"
    )
    template_name = "index.html"


class AboutView(PageTitleViewMixin, TemplateView):
    """
    Render About Page
    """

    title = "About"
    template_name = "about.html"


class PostListView(PageTitleViewMixin, ListView):
    """
    Render Post List Page and only displays
    approved posts
    """

    model = Post
    title = "Posts"
    queryset = Post.objects.filter(status=1).annotate(
        num_comments=Count(
            "comments", filter=models.Q(comments__approved=True)
        )
    )
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 8
    ordering = ['-created_on']


class PostCategoryListView(PageTitleViewMixin, ListView):
    """
    Render Post List Page and only displays
    approved posts filtered by category
    """

    model = Post
    title = "Posts"
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 8
    ordering = ['-created_on']

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        queryset = Post.objects.filter(
            status=1, regions=self.category
        ).annotate(
            num_comments=Count(
                "comments", filter=models.Q(comments__approved=True)
            )
        )
        return queryset


class PostDetailView(DetailView):
    """
    Render Post Detail Page
    """

    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title.title()
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(approved=True)
        if self.request.user.is_authenticated:
            context["profile"] = Profile.objects.get(user=self.request.user)
            context["liked"] = self.object.likes.filter(id=self.request.user.id).exists()
        else:
            context["liked"] = False
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.name = self.request.user
            comment.profile = Profile.objects.get(user=self.request.user)
            comment.save()
            messages.success(
                request,
                "Your comment has been successfully created and is waiting for approval..",
            )
            return redirect("post_detail", slug=self.get_object().slug)
        else:
            context = self.get_context_data(**kwargs)
            context["comment_form"] = form
            return self.render_to_response(context)


class PostCreateView(
    PageTitleViewMixin,
    SuperuserFieldsMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    PostFormInvalidMessageMixin,
    CreateView,
):
    """
    Render Post Create Page
    """

    model = Post
    title = "Create Post"
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("account_login")
    success_message = (
        "Your post has been successfully created and is waiting for approval."
    )

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = messages.get_messages(self.request)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


class PostUpdateView(
    PageTitleViewMixin,
    SuperuserFieldsMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    PostFormInvalidMessageMixin,
    UpdateView,
):
    """
    Allow Author of Post or Superuser to update the post
    """

    model = Post
    title = "Update Post"
    form_class = PostForm
    template_name = "post_create.html"
    success_message = (
        "Your post has been successfully updated and is waiting for approval."
    )
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user.is_superuser or self.request.user == post.author
        )

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.status = 0
        self.object = form.save()
        return super().form_valid(form)


class PostDeleteView(
    PageTitleViewMixin,
    SuperuserFieldsMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """
    Allow Author of Post or Superuser to delete the post
    """

    model = Post
    title = "Delete Post"
    template_name = "post_detail.html"
    success_message = "Your post has been successfully deleted."
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        print(self.success_message)
        return (
            self.request.user.is_superuser or self.request.user == post.author
        )

    def delete(self, request, *args, **kwargs):
        profile = self.get_object()
        messages.success(self.request, self.success_message % profile.__dict__)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)


class PostSearchResultsView(PageTitleViewMixin, ListView):
    model = Post
    title = "Your Search"
    template_name = "search_results.html"
    context_object_name = "results"

    def get_queryset(self):
        search = self.request.GET.get("q")
        results = Post.objects.filter(
            Q(title__icontains=search) | Q(country__icontains=search)
        )
        return results

class PostLikeView(View):
    """
    Allow all users to like a post
    """

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        user = self.request.user
        liked = False
        count = post.likes.count()
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
            liked = True
        response = {
            'liked': liked,
            'count': count,
        }
        return JsonResponse(response)
