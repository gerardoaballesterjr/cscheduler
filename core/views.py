from django.contrib.auth import mixins
from django.views import generic
from django import urls, http
from django.contrib import auth
from core import forms

# [login]
class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm
    success_url = urls.reverse_lazy('core:index')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return http.HttpResponseRedirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return http.HttpResponse(status=204, headers={'Hx-Redirect': self.success_url})

# [logout]
class LogoutView(generic.View):
    def get(self, request):
        auth.logout(request)
        return http.HttpResponseRedirect(urls.reverse_lazy('core:index'))


# [index]
class IndexView(mixins.LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'
    extra_context = {'title': 'Dashboard'}
