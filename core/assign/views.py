from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.assign import forms
from core import models

# [assign:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Assign
    template_name = 'assign.html'
    extra_context = {'title': 'Assign'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(professor__department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [assign:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Assign
    form_class = forms.AssignForm
    success_url = urls.reverse_lazy('assign:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Assign'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def form_valid(self, form):
        object = form.save(commit=False)
        object.save()
        form.save_m2m()
        messages.success(self.request, f'Assign created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [assign:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Assign
    form_class = forms.AssignForm
    success_url = urls.reverse_lazy('assign:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Assign'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().professor.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Assign updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [assign:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Assign
    success_url = urls.reverse_lazy('assign:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Assign'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().professor.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Assign deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})