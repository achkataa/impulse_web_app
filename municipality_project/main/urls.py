from django.urls import path

from municipality_project.main.views import HomeView, Dashboard, show_pdf, MyFile, UploadDocument, show_user_pdf, \
    UpdateDocument, DeleteDocument

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('pdf/', show_pdf, name='show_pdf'),
    path('myfile/', MyFile.as_view(), name='my_file'),
    path('uploadfile/', UploadDocument.as_view(), name='upload_document'),
    path('userpdf/', show_user_pdf, name='show_user_pdf'),
    path('updatefile/<int:pk>/', UpdateDocument.as_view(), name='update_document'),
    path('deletefile/<int:pk>/', DeleteDocument.as_view(), name='delete_document'),
]