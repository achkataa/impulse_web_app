from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from municipality_project.auth_app.deep_link import base64UrlEncode
from municipality_project.auth_app.forms import RegisterUserForm, LoginUserForm

# class RegisterUser(CreateView):
#     form_class = RegisterUserForm
#     template_name = 'auth/register.html'
#     success_url = reverse_lazy('dashboard')
#
#     def form_valid(self, form):
#         result = super().form_valid(form)
#         login(self.request, self.object)
#         return result
# from municipality_project.auth_app.tokens import account_activation_token
from municipality_project.auth_app.models import UserProfile
from municipality_project.auth_app.qr_code import parse_json_to_strings, generate_qr_code
from municipality_project.auth_app.tokens import account_activation_token


class RegisterUser(View):
    form_class = RegisterUserForm
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            user_profile = UserProfile(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                user=user,
            )
            user_profile.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('auth/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login_user')

        return render(request, self.template_name, {'form': form})


from django.utils.encoding import force_str


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model()
            user = user.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login_user')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


# def signup(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             # save form in the memory not in database
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             # to get the domain of the current site
#             current_site = get_current_site(request)
#             mail_subject = 'Activation link has been sent to your email id'
#             message = render_to_string('auth/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'auth/register.html', {'form': form})
#
# from django.utils.encoding import force_bytes, force_text
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')


class LoginUser(LoginView):
    template_name = 'auth/login.html'
    form_class = LoginUserForm

    def get_success_url(self):
        return reverse_lazy('dashboard')

class LoginWithQRCode(TemplateView):
    template_name = 'auth/login_with_qr_code.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        json_example = '{ "sessionId":"c2b3e0f5-89b8-4d8f-8325-20228af1b8b5", "presentationRequest":"openid://?response_type=id_token&client_id=did%3Aebsi%3AzkqSHiqQSH1jk6U6846ebmu&scope=openid+did_authn&request=eyJraWQiOiI5NjA2MDZhYjA0NjQ0ZDhlYmY3MWZiYTkzYzlhYjBlZSIsInR5cCI6IkpXVCIsImFsZyI6IkVkRFNBIn0.eyJhdXRoZW50aWNhdGlvblJlcXVlc3RKd3QiOnsiYXV0aEhlYWRlciI6eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSIsImp3ayI6eyJrdHkiOiJPS1AiLCJjcnYiOiJFZDI1NTE5IiwidXNlIjoic2lnIiwia2lkIjoiOTYwNjA2YWIwNDY0NGQ4ZWJmNzFmYmE5M2M5YWIwZWUiLCJ4IjoiZHliaDgtYTZxY2l0bjJwQzhFSE44V1hpbUJJcmJSM1JfanczQ1RvWXVvMCIsImFsZyI6IkVkRFNBIn19LCJhdXRoUmVxdWVzdFBheWxvYWQiOnsic2NvcGUiOiJvcGVuaWQgZGlkX2F1dGhuIiwiY2xhaW1zIjp7ImlkVG9rZW4iOnsidmVyaWZpZWRDbGFpbXMiOnsidmVyaWZpY2F0aW9uIjp7ImV2aWRlbmNlIjp7ImRvY3VtZW50Ijp7ImNyZWRlbnRpYWxTY2hlbWEiOnsiaWQiOnsidmFsdWUiOiJodHRwczpcL1wvYXBpLnByZXByb2QuZWJzaS5ldVwvdHJ1c3RlZC1zY2hlbWFzLXJlZ2lzdHJ5XC92MVwvc2NoZW1hc1wvMHg2MDllMmNhMjIzMzI1M2U3NGUwZGNhOGRjOTUyNjAwYjYxZDQ2YWZmYzMxOGFhNGE3MGEyOGViNzE4OTUyZTNlIiwiZXNzZW50aWFsIjp0cnVlfX0sInR5cGUiOnsidmFsdWUiOlsiVmVyaWZpYWJsZUNyZWRlbnRpYWwiLCJWZXJpZmlhYmxlSWQiXSwiZXNzZW50aWFsIjp0cnVlfX0sInR5cGUiOnsidmFsdWUiOiJ2ZXJpZmlhYmxlX2NyZWRlbnRpYWwiLCJlc3NlbnRpYWwiOm51bGx9fSwidHJ1c3RfZnJhbWV3b3JrIjoiRUJTSSJ9fX19LCJpc3MiOiJkaWQ6ZWJzaTp6a3FTSGlxUVNIMWprNlU2ODQ2ZWJtdSIsInJlc3BvbnNlX3R5cGUiOiJpZF90b2tlbiIsInJlZ2lzdHJhdGlvbiI6eyJhY2Nlc3NfdG9rZW5fZW5jcnlwdGlvbl9lbmNfdmFsdWVzX3N1cHBvcnRlZCI6WyJBMTI4R0NNIiwiQTI1NkdDTSJdLCJqd2tzX3VyaSI6IiIsInJlZGlyZWN0X3VyaXMiOlsiIl0sInJlcXVlc3Rfb2JqZWN0X3NpZ25pbmdfYWxnIjpbIkVTMjU2SyIsIkVkRFNBIl0sImFjY2Vzc190b2tlbl9zaWduaW5nX2FsZyI6WyJFUzI1NksiLCJFZERTQSJdLCJhY2Nlc3NfdG9rZW5fZW5jcnlwdGlvbl9hbGdfdmFsdWVzX3N1cHBvcnRlZCI6WyJFQ0RILUVTIl0sImlkX3Rva2VuX3NpZ25lZF9yZXNwb25zZV9hbGciOlsiRVMyNTZLIiwiRWREU0EiXSwicmVzcG9uc2VfdHlwZXMiOiJpZF90b2tlbiJ9LCJub25jZSI6ImMyYjNlMGY1LTg5YjgtNGQ4Zi04MzI1LTIwMjI4YWYxYjhiNSIsImNsaWVudF9pZCI6ImRpZDplYnNpOnprcVNIaXFRU0gxams2VTY4NDZlYm11In19LCJzY29wZSI6Im9wZW5pZCBkaWRfYXV0aG4iLCJjYWxsYmFjayI6Imh0dHA6XC9cLzQwLjcxLjU3Ljk4OjgwODBcL3ZlcmlmaWNhdGlvblwvdjFcL2F1dGhlbnRpY2F0aW9uLXJlc3BvbnNlcyIsInJlc3BvbnNlX3R5cGUiOiJpZF90b2tlbiIsIm5vbmNlIjoiYzJiM2UwZjUtODliOC00ZDhmLTgzMjUtMjAyMjhhZjFiOGI1IiwiY2xpZW50X2lkIjoiZGlkOmVic2k6emtxU0hpcVFTSDFqazZVNjg0NmVibXUifQ.HXiTSArbXm-6YCxFTAJuBx17xRAG6GVLKbp7UFbiYsk2PiOdwq2p8YNS9aSLAtv3ouY3OJzBOu7oLMn5O8cKCQ&nonce=c2b3e0f5-89b8-4d8f-8325-20228af1b8b5"}'
        presentationRequest_string = parse_json_to_strings(json_example)
        qr_code_img = generate_qr_code(presentationRequest_string)
        deep_link_string = base64UrlEncode(presentationRequest_string)
        context['qr_code_img'] = qr_code_img
        context['qr_data'] = presentationRequest_string
        context['deep_link_string'] = deep_link_string
        qr_code_img.save("sample.png")
        return context


class LogoutUser(LogoutView):
    template_name = 'main/home.html'
    next_page = reverse_lazy('home')




