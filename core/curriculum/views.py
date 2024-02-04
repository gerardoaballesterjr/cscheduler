from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.curriculum import forms
from core import models

# [curriculum:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Curriculum
    template_name = 'curriculum.html'
    extra_context = {'title': 'Curriculum'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(course__department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [curriculum:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Curriculum
    form_class = forms.CurriculumForm
    success_url = urls.reverse_lazy('curriculum:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Curriculum'}

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
        messages.success(self.request, f'Curriculum created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [curriculum:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Curriculum
    form_class = forms.CurriculumForm
    success_url = urls.reverse_lazy('curriculum:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Curriculum'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().course.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Curriculum updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [curriculum:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Curriculum
    success_url = urls.reverse_lazy('curriculum:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Curriculum'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Curriculum deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})