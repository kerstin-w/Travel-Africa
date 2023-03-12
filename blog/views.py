from django.contrib import messages
from django.views import generic
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Post
from .forms import PostForm, CommentForm
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
        return self.render_to_response(self.get_context_data(form=form))


class AboutView(PageTitleViewMixin, TemplateView):
    """
    Render About Page
    """

    title = "About"
    template_name = "about.html"


class PostListView(ListView):
    """
    Render Post List Page and only displays
    approved posts
    """

    model = Post
    title = "Posts"
    queryset = Post.objects.filter(status=1)
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 6


class PostFeaturedList(PageTitleViewMixin, generic.ListView):
    """
    Render featured posts on home page
    """

    model = Post
    title = "Home"
    queryset = Post.objects.filter(featured=True, status=1).order_by(
        "-created_on"
    )
    template_name = "index.html"


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
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
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
