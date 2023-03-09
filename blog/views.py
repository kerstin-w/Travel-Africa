from django.contrib import messages
from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
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


class PostFeaturedList(PageTitleViewMixin, generic.ListView):
    model = Post
    title = "Home"
    queryset = Post.objects.filter(featured=True, status=1).order_by(
        "-created_on"
    )
    template_name = "index.html"


class PostCreateView(
    PageTitleViewMixin, SuperuserFieldsMixin, UserPassesTestMixin, CreateView
):
    model = Post
    title = "Create Post"
    form_class = PostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("account_login")

    def test_func(self):
        return self.request.user.is_authenticated

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)
