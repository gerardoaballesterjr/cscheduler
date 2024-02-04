from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.section import forms
from core import models

# [section:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Section
    template_name = 'section.html'
    extra_context = {'title': 'Section'}

    def get_queryset(self, *args, **kwargs):
        object = super().get_queryset(*args, **kwargs)
        return object if self.request.user.is_superuser else object.filter(course__department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [section:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Section
    form_class = forms.SectionForm
    success_url = urls.reverse_lazy('section:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Section'}

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
        messages.success(self.request, f'Section created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [section:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Section
    form_class = forms.SectionForm
    success_url = urls.reverse_lazy('section:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Section'}
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
        messages.success(self.request, f'Section updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [section:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Section
    success_url = urls.reverse_lazy('section:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Section'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().course.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Section deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})
    
# [section:schedule]
class ScheduleView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Section
    template_name = 'schedule.html'
    extra_context = {}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().course.department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        semester = models.Semester.objects.last()
        self.extra_context['semester'] = semester
        self.extra_context['title'] = f'Section Schedule | {self.get_object().course.code} {self.get_object().level}{self.get_object().block}'
        self.extra_context['data'] = []
        self.days = list(models.Day.objects.all())
        self.days = self.days[-1:]+self.days[:-1]
        for object in models.Schedule.objects.filter(assign__semester = semester, section = self.get_object()):
            self.extra_context['data'].append({
                'title': f'{object.assign.subject.name} | {object.assign.professor.first_name[0].capitalize()}. {object.assign.professor.last_name}',
                'daysOfWeek': [self.days.index(day) for day in object.days.all()],
                'startTime': object.stime,
                'endTime': object.etime,
            })
        return super().dispatch(self.request, *args, **kwargs)