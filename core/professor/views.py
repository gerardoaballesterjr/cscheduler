from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.professor import forms
from core import models

# [professor:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Professor
    template_name = 'professor.html'
    extra_context = {'title': 'Professor'}

    def get_queryset(self, *args, **kwargs):
        object = super().get_queryset(*args, **kwargs)
        return object if self.request.user.is_superuser else object.filter(department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department and not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [professor:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Professor
    form_class = forms.ProfessorForm
    success_url = urls.reverse_lazy('professor:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Professor'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.department = self.request.user.department
        object.save()
        messages.success(self.request, f'Professor created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [professor:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Professor
    form_class = forms.ProfessorForm
    success_url = urls.reverse_lazy('professor:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Professor'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Professor updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [professor:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Professor
    success_url = urls.reverse_lazy('professor:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Professor'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().department:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Professor deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})
    
# [professor:schedule]
class ScheduleView(mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Professor
    template_name = 'schedule.html'
    extra_context = {}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        semester = models.Semester.objects.last()
        self.extra_context['semester'] = semester
        self.extra_context['title'] = f'Professor Schedule | {self.get_object().first_name[0].capitalize()}. {self.get_object().last_name}'
        self.extra_context['data'] = []
        self.days = list(models.Day.objects.all())
        self.days = self.days[-1:]+self.days[:-1]
        for object in models.Schedule.objects.filter(assign__semester = semester, assign__professor = self.get_object()):
            self.extra_context['data'].append({
                'title': f'{object.assign.subject.name} | {object.section.course.code} {object.section.level}{object.section.block}',
                'daysOfWeek': [self.days.index(day) for day in object.days.all()],
                'startTime': object.stime,
                'endTime': object.etime,
            })
        return super().dispatch(self.request, *args, **kwargs)