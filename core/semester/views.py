from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.semester import forms
from core import models

# [semester:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Semester
    template_name = 'semester.html'
    extra_context = {'title': 'Semester'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not self.request.user.department:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [semester:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Semester
    form_class = forms.SemesterForm
    success_url = urls.reverse_lazy('semester:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Semester'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Semester created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [semester:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Semester
    form_class = forms.SemesterForm
    success_url = urls.reverse_lazy('semester:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Semester'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Semester updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [semester:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Semester
    success_url = urls.reverse_lazy('semester:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Semester'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Semester deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})
    
# [semester:generate]
class GenerateView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Semester
    success_url = urls.reverse_lazy('semester:index')
    template_name = 'generate.html'
    extra_context = {'title': 'Generate Semester'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if not self.request.user.department:
            return self.handle_no_permission()
        self.extra_context['websocket'] = self.request.build_absolute_uri().replace('http', 'ws')
        return super().dispatch(self.request, *args, **kwargs)