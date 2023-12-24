from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import messages
from core.roomtype import forms
from core import models

# [room-type:index]
class IndexView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.RoomType
    template_name = 'room-type.html'
    extra_context = {'title': 'RoomType'}

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(department=self.request.user.department)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

# [room-type:create]
class CreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = models.RoomType
    form_class = forms.RoomTypeForm
    success_url = urls.reverse_lazy('room-type:index')
    template_name = 'form.html'
    extra_context = {'title': 'Create Room type'}

    def dispatch(self, request, *args, **kwargs):
        if not request.user.department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save(commit=False)
        object.department = self.request.user.department
        object.save()
        messages.success(self.request, f'Room type created successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [room-type:update]
class UpdateView(mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.RoomType
    form_class = forms.RoomTypeForm
    success_url = urls.reverse_lazy('room-type:index')
    template_name = 'form.html'
    extra_context = {'title': 'Update Room type'}
    query_pk_and_slug = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.department != self.get_object().department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        object = form.save()
        messages.success(self.request, f'Room type updated successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})

# [room-type:delete]
class DeleteView(mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.RoomType
    success_url = urls.reverse_lazy('room-type:index')
    template_name = 'delete.html'
    extra_context = {'title': 'Delete Room type'}
    query_pk_and_slug = True

    def dispatch(self, *args, **kwargs):
        if self.request.user.department != self.get_object().department and not self.request.user.is_superuser:
            return self.handle_no_permission()
        self.extra_context['action'] = self.request.build_absolute_uri()
        return super().dispatch(self.request, *args, **kwargs)
    
    def form_valid(self, form):
        object = self.get_object()
        object.delete()
        messages.success(self.request, f'Room type deleted successfully.')
        return http.HttpResponse(status=204, headers={'HX-Trigger': 'form'})