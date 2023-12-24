from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.subject import forms
from core import models

# [subject:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Subject
    template_name = 'subject.html'
    extra_context = {'title': 'Subject'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [subject:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Subject
    form_class = forms.SubjectForm
    success_url = urls.reverse_lazy('subject:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Subject'}

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
        object.department = self.request.user.department
        object.save()
        messages.success(self.request, f'Subject created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [subject:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Subject
    form_class = forms.SubjectForm
    success_url = urls.reverse_lazy('subject:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Subject'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Subject updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [subject:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Subject
    success_url = urls.reverse_lazy('subject:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Subject'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Subject deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})