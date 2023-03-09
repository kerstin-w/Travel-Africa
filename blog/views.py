from django.views import generic
from django.views.generic import TemplateView
from .models import Post


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


class PostFeaturedList(PageTitleViewMixin, generic.ListView):
    model = Post
    title = "Home"
    queryset = Post.objects.filter(
        featured=True, status=1).order_by('-created_on')
    template_name = "index.html"


class AboutView(PageTitleViewMixin, TemplateView):
    title = "About"
    template_name = "about.html"

