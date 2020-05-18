
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserCreationForm, UserInfoChangeForm, CompanyInfoChangeForm, UserPasswordChangeForm
from main.settings import HOST_NAME
from accounts.models import Token, Profile
from django.http import HttpResponseRedirect




# def register_view(request):
#     if request.method == 'POST':
#         form = UserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = User(
#                 username=form.cleaned_data['username'],
#                 # first_name=form.cleaned_data['first_name'],
#                 # last_name=form.cleaned_data['last_name'],
#                 email=form.cleaned_data['email']
#             )
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             # Profile.objects.create(user=user)
#             login(request, user)
#             return redirect('webapp:index')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register.html', context={'form': form})


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

            # отправка письма на email пользователя
            user.email_user('Регистрация на сайте localhost',
                            'Для активации перейдите по ссылке: {}'.format(activation_url))

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
        print(user.profile.type)
        if user.profile.type == 'client':
            return HttpResponseRedirect(reverse('accounts:user_update', kwargs={"pk": user.pk}))
        else:
            return HttpResponseRedirect(reverse('accounts:company_update', kwargs={"pk": user.pk}))
    except Token.DoesNotExist:
        # если токена нет - сразу редирект
        return redirect('webapp:index')


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

    # def form_valid(self, form):
    #     pk = self.kwargs.get('pk')
    #     profile = get_object_or_404(Profile, user=pk)
    #     user = get_object_or_404(User, pk=pk)
    #     user.first_name = form.cleaned_data['first_name']
    #     user.last_name = form.cleaned_data['last_name']
    #     user.email = form.cleaned_data['email']
    #     profile.sex = form.cleaned_data['sex']
    #     profile.birth_date = form.cleaned_data['birth_date']
    #     profile.mobile_phone = form.cleaned_data['mobile_phone']
    #     profile.company_name = form.cleaned_data['company_name']
    #     print(profile.company_name)
    #     profile.inn = form.cleaned_data['inn']
    #     profile.okpo = form.cleaned_data['okpo']
    #     profile.phone = form.cleaned_data['phone']
    #     profile.save()
    #     user.save()
    #     return self.get_success_url()

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


class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'
    paginate_by = 5
    paginate_orphans = 1

    def get_url(self):
        global site
        site = self.request.path
        return site

    # def test_func(self):
    #     user = self.request.user
    #     print(user)
    #     return user.is_staff

