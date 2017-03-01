from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect


class Main(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        context = dict()
        context['generic'] = True
        if request.user.is_authenticated:
            context['user_name'] = request.user.username
            self.template_name = 'user.html'
        else:
            self.template_name = 'main.html'

        return self.render_to_response(context)


class Login(generic.View):

    def post(self, request, *args, **kwargs):
        login_ = request.POST['login']
        pass_ = request.POST['password']
        url_ = request.POST['url']
        user = authenticate(username=login_, password=pass_)
        if user:
            login(request, user)
        return redirect(url_)

    def get(self, request, *args, **kvargs):
        return redirect('/login')


class Logout(generic.View):

    def post(self, request):
        logout(request)
        url_ = request.POST['url']
        return redirect(url_)

