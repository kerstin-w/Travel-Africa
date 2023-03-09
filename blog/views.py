from django.contrib import messages
from django.core.paginator import Paginator
from django.views import generic
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Post
from .forms import PostForm


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


class AboutView(PageTitleViewMixin, TemplateView):
    title = "About"
    template_name = "about.html"


class PostListView(ListView):
    model = Post
    title = "Posts"
    template_name = "post_list.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        return context


class PostFeaturedList(PageTitleViewMixin, generic.ListView):
    model = Post
    title = "Home"
    queryset = Post.objects.filter(featured=True, status=1).order_by(
        "-created_on"
    )
    template_name = "index.html"


class PostCreateView(
    PageTitleViewMixin,
    SuperuserFieldsMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    CreateView,
):
    model = Post
    title = "Create Post"
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("account_login")
    success_message = "Your post has been successfully saved."

    def test_func(self):
        return self.request.user.is_authenticated

    def get_context_data(self, **kwargs):
        print("context")
        context = super().get_context_data(**kwargs)
        context["messages"] = messages.get_messages(self.request)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Form submission is not valid!")
        return self.render_to_response(self.get_context_data(form=form))
