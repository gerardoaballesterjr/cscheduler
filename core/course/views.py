from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.course import forms
from core import models

# [course:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Course
    template_name = 'course.html'
    extra_context = {'title': 'Course'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [course:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Course
    form_class = forms.CourseForm
    success_url = urls.reverse_lazy('course:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Course'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.department = self.request.user.department
        object.save()
        messages.success(self.request, f'Course created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [course:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    success_url = urls.reverse_lazy('course:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Course'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Course updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [course:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Course
    success_url = urls.reverse_lazy('course:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Course'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Course deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})