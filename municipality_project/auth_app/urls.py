from django.urls import path

from municipality_project.auth_app.views import RegisterUser, LoginUser, LogoutUser, ActivateAccount, LoginWithQRCode

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register_user'),
    path('login/', LoginUser.as_view(redirect_authenticated_user=True), name='login_user'),
    path('logout/', LogoutUser.as_view(), name='logout_user'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('loginwithqrcode/', LoginWithQRCode.as_view(), name='login_with_qr_code'),
]