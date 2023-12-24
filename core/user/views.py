from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.user import forms
from core import models

# [user:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.User
    template_name = 'user.html'
    extra_context = {'title': 'User'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_superuser=False)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [user:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.User
    form_class = forms.UserCreationForm
    success_url = urls.reverse_lazy('user:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create User'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.is_staff = True
        object.save()
        messages.success(self.request, f'User created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [user:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.User
    form_class = forms.UserChangeForm
    success_url = urls.reverse_lazy('user:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update User'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'User updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [user:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.User
    success_url = urls.reverse_lazy('user:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete User'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'User deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})