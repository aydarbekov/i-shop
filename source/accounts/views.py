from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.template.loader import get_template
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserCreationForm, UserInfoChangeForm, CompanyInfoChangeForm, UserPasswordChangeForm, \
    StaffCreationForm, UserPasswordResetForm
from main.settings import HOST_NAME
from accounts.models import Token, Profile
from django.http import HttpResponseRedirect
from webapp.views.product_views import SearchView
from django.core.mail import send_mail
from django.conf import settings


# def send_token(user, subject, message, redirect_url):
#     token = Token.objects.create(user=user)
#     url = HOST_NAME + reverse(redirect_url, kwargs={'token': token})
#     print(url)
#     try:
#         user.email_user(subject, message.format(url=url))
#     except ConnectionRefusedError:
#         print('Could not send email. Server error.')


def register_view(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                # phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email'],
                is_active=False  # user не активный до подтверждения email
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile(
                user=user,
                mobile_phone=form.cleaned_data['phone_number'],
                type=form.cleaned_data['type']
            )
            user.save()
            profile.save()
            # user.profile.mobile_phone = form.cleaned_data['phone_number']
            # user.profile.save()

            # токен для активации, его сложнее угадать, чем pk user-а.
            token = Token.objects.create(user=user)
            activation_url = HOST_NAME + reverse('accounts:user_activate') + '?token={}'.format(token)
            context = {
                'user': user.first_name,
                'url': activation_url,
                'h1': 'Поздравляем с регистрацией на нашем сайте!',
                'text': 'Для подтверждения регистрации просто нажмите на кнопку.',
                'text_2': 'Проще не бывает!',
                'btn_text': 'Подтвердить регистрацию'
            }
            send_mail('Регистрация Kanctorg', 'Регистрация Kanctorg', settings.EMAIL_HOST_USER,
                      [user.email],
                      html_message=get_template('password_reset_emailing.html').render(context),
                      fail_silently=False)
            # отправка письма на email пользователя
            # user.email_user('Регистрация на сайте localhost',
            #                 'Для активации перейдите по ссылке: {}'.format(activation_url))

            return redirect("webapp:index")
        else:
            return render(request, 'register.html', {'form': form})


def user_activate(request):
    token_value = request.GET.get('token')
    try:
        # найти токен
        token = Token.objects.get(token=token_value)

        # активировать пользователя
        user = token.user
        user.is_active = True
        user.save()

        # удалить токен, он больше не нужен
        token.delete()

        # войти
        login(request, user)

        # редирект на главную
        # return redirect('webapp:index')
        # return redirect('accounts:user_update')
        if user.profile.type == 'client':
            return HttpResponseRedirect(reverse('accounts:user_update', kwargs={"pk": user.pk}))
        else:
            return HttpResponseRedirect(reverse('accounts:company_update', kwargs={"pk": user.pk}))
    except Token.DoesNotExist:
        # если токена нет - сразу редирект
        return redirect('webapp:index')


def password_reset_email_view(request):
    if request.method == 'GET':
        return render(request, 'password_reset_email.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)
        if len(users) > 0:
            user = users[0]
            token = Token.objects.create(user=user)
            redirect_url = 'accounts:password_reset_form'
            url = HOST_NAME + reverse(redirect_url, kwargs={'token': token})
            # send_token(user,
            #            'Вы запросили восстановление пароля на сайте localhost:8000.',
            #            'Для ввода нового пароля перейдите по ссылке: {url}',
            #            redirect_url='accounts:password_reset_form')
            context = {
                'user': user.first_name,
                'url': url,
                'h1': 'Забыли пароль?',
                'text': 'Не волнуйтесь - такое случается!',
                'text_2': 'Просто нажмите на кнопку ниже и создайте новый пароль. Проще не бывает!',
                'btn_text': 'Восстановить пароль'
            }
            send_mail('Восстановление пароля Kanctorg', 'Восстановление пароля Kanctorg', settings.EMAIL_HOST_USER, [user.email],
                      html_message=get_template('password_reset_emailing.html').render(context),
                      fail_silently=False)
        return render(request, 'password_reset_confirm.html')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'


class UserInfoChangeView(UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_object'
    form_class = UserInfoChangeForm

    # def test_func(self):
    #     return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.pk})


class CompanyInfoChangeView(UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_object'
    form_class = CompanyInfoChangeForm

    # def test_func(self):
    #     return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={"pk": self.object.pk})


class UserPasswordChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_password_change.html'
    form_class = UserPasswordChangeForm
    context_object_name = 'user_object'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:login')


class UserListView(ListView, SearchView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    # paginate_by = 5
    # paginate_orphans = 1

    def get_url(self):
        global site
        site = self.request.path
        return site

    # def test_func(self):
    #     user = self.request.user
    #     print(user)
    #     return user.is_staff


def register_staff_view(request):
    if request.method == 'GET':
        form = StaffCreationForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = StaffCreationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                # phone_number=form.cleaned_data['phone_number'],
                email=form.cleaned_data['email'],
                is_active=True  # user не активный до подтверждения email
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile(
                user=user,
                mobile_phone=form.cleaned_data['phone_number'],
                type=form.cleaned_data['type']
            )
            user.save()
            profile.save()

            return reverse('accounts:user_detail', kwargs={"pk": user.pk})
        else:
            return render(request, 'register.html', {'form': form})


class PasswordResetFormView(UpdateView):
    model = User
    template_name = 'password_reset_form.html'
    form_class = UserPasswordResetForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        token = self.get_token()
        return token.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['token'] = self.kwargs.get('token')
        return context

    def form_valid(self, form):
        token = self.get_token()
        token.delete()
        return super().form_valid(form)

    def get_token(self):
        token_value = self.kwargs.get('token')
        return get_object_or_404(Token, token=token_value)

    def get_success_url(self):
        return reverse('accounts:login')