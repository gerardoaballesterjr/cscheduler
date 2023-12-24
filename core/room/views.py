from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.room import forms
from core import models

# [room:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Room
    template_name = 'room.html'
    extra_context = {'title': 'Room'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type__department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [room:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Room
    form_class = forms.RoomForm
    success_url = urls.reverse_lazy('room:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Room'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department and not self.request.user.is_superuser:
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
        messages.success(self.request, f'Room created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [room:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    success_url = urls.reverse_lazy('room:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Room'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().type.department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['department'] = self.request.user.department
        return kwargs

    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Room updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [room:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Room
    success_url = urls.reverse_lazy('room:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Room'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().type.department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Room deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})