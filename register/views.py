from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, dumps, loads
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView, ListView, TemplateView, CreateView, FormView
)

from .forms import (
    LoginForm, UserCreateForm, MyPasswordChangeForm, EmailChangeForm,
    MyPasswordResetForm, MySetPasswordForm
)
from .models import User
from page.models import Shop

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse

User = get_user_model()

class LoginLockView(TemplateView):
    """ ログイン5回連続で失敗したら表示 """
    template_name = 'register/axes_locked.html'

class UserCreate(CreateView):
    """ ユーザー仮登録 """
    template_name = 'register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """ 仮登録と本登録用メールの発行 """
        # is_active= Falseは仮登録か退会
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送信
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        subject = render_to_string('register/mail_template/create/subject.txt', context)
        message = render_to_string('register/mail_template/create/message.txt', context)
        from_email = settings.DEFAULT_FROM_EMAIL
        user.email_user(subject,
        message,
        from_email)
        return redirect('register:user_create_done')

class UserCreateDone(TemplateView):
    """ ユーザー仮登録完了 """
    template_name = 'register/user_create_done.html'

class UserCreateComplete(TemplateView):
    """ アクティベーションURLを開いたあとの処理 """
    template_name = 'register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATE_TIMEOUT_SECONDS', 60*60*24)

    def get(self, request, **kwargs):
        """ tokenが正しければ本登録 """
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # token 間違い
        except BadSignature:
            print('tokenが間違っています')
            return HttpResponseBadRequest()

        # token OK
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 本登録
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

            return HttpResponseBadRequest()


class Login(LoginView):
    """ ログイン """
    # form_class = LoginForm
    authentication_form = LoginForm
    
    template_name = 'registration/login.html'

@login_required
def account_redirect(request):
    """ ログインしたらメール送信してユーザートップページにつなぐ """
    subject = "ログインのお知らせ"

    message = "ログインのお知らせです。"

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [

    from_email

    ]

    # send_mail(subject, message, from_email, recipient_list)
    return redirect('register:usertop', pk=request.user.pk)

class Logout(LoginRequiredMixin, LogoutView):
    """ ログアウト """
    template_name = 'register/logout.html'

class UserTop(LoginRequiredMixin, DetailView):
    """ ユーザートップページ """
    template_name = 'register/usertop.html'
    model = User

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['shop_list'] = Shop.objects.all()
        return context



class PasswordChange(PasswordChangeView):
    """ パスワード変更 """
    form_class = MyPasswordChangeForm
    template_name = 'register/password_change.html'
    success_url = reverse_lazy('register:account-redirect')

    def form_valid(self, form):
        """ メッセージ表示を追加 """
        result = super().form_valid(form)
        messages.success(
            self.request, '「パスワード」を変更しました')
        return result

class EmailChange(LoginRequiredMixin, FormView):
    """ メールアドレスの変更 """
    template_name = 'register/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        """ パスワード変更のためのメール送信 """
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('register/mail_template/email_change/subject.txt', context)
        message = render_to_string('register/mail_template/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('register:email_change_done')

class EmailChangeDone(LoginRequiredMixin, TemplateView):
    """ アドレス変更メール送信完了 """
    template_name = 'register/email_change_done.html'

class EmailChangeComplete(LoginRequiredMixin, TemplateView):
    """ リンクを呼ばれた後に呼ばれる変更ビュー """
    template_name = 'register/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内
    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest

        # token間違い
        except BadSignature:
            return HttpResponseBadRequest
        
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'register/mail_template/password_reset/subject.txt'
    email_template_name = 'register/mail_template/password_reset/message.txt'
    template_name = 'register/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('register:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'register/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('register:password_reset_complete')
    template_name = 'register/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'register/password_reset_complete.html'
        

