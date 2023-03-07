from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Profile
from .forms import ProfileForm
from blog.views import PageTitleViewMixin



class ProfileHomeView(PageTitleViewMixin, LoginRequiredMixin, TemplateView):
    model = Profile
    title = "Profile"
    template_name = 'profile.html'
    user_check_failure_path = reverse_lazy("account_signup")

    def check_user(self, user):
        if user.is_active:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(ProfileHomeView, self).get_context_data(**kwargs)
        profile = Profile.objects.get_or_create(user=self.request.user)[0]
        context['profile'] = profile
        return context

class ProfileUpdateView(PageTitleViewMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    title = "Update Profile"
    form_class = ProfileForm
    template_name = 'profile_update.html'

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def test_func(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return self.request.user == profile.user

    def form_valid(self, form):
        form.instance.status = 0
        self.object = form.save()
        messages.success(self.request, 'Profile updated successfully')
        return redirect(reverse('home'))