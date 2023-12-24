from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.department import forms
from core import models

# [department:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Department
    template_name = 'department.html'
    extra_context = {'title': 'Department'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [department:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Department
    form_class = forms.DepartmentForm
    success_url = urls.reverse_lazy('department:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Department'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Department created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [department:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Department
    form_class = forms.DepartmentForm
    success_url = urls.reverse_lazy('department:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Department'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Department updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [department:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Department
    success_url = urls.reverse_lazy('department:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Department'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Department deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})