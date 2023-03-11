from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Profile
from .forms import ProfileForm
from blog.views import PageTitleViewMixin


class ProfileHomeView(PageTitleViewMixin, LoginRequiredMixin, TemplateView):
    """
    Display profile information 
    """
    model = Profile
    title = "Profile"
    template_name = "profile.html"
    user_check_failure_path = reverse_lazy("account_signup")

    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        context["profile"] = profile
        return context


class ProfileUpdateView(
    PageTitleViewMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    """
    Display profile update to allow users to update their profile information
    """
    model = Profile
    title = "Update Profile"
    form_class = ProfileForm
    template_name = "profile_update.html"

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.request.user == profile.user

    def form_valid(self, form):
        form.instance.status = 0
        self.object = form.save()
        messages.success(self.request, "Profile updated successfully")
        return redirect(reverse("home"))


class ProfileDeleteView(
    PageTitleViewMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    """
    Display profile delete to allow users to delete their profile information
    """
    model = Profile
    title = "Profile"
    success_url = reverse_lazy("home")
    user_check_failure_path = reverse_lazy("account_signup")

    def test_func(self):
        profile = self.get_object()
        return (
            self.request.user.is_authenticated
            and self.request.user == profile.user
        )

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object.user
        self.object.delete()
        user.delete()
        messages.success(
            self.request, "Your profile has been deleted successfully."
        )
        self.request.session.flush()
        return redirect(self.success_url)
