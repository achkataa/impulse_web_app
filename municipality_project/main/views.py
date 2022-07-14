import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponse, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
import static
from municipality_project.auth_app.models import UserProfile, UserDocument
from municipality_project.main.forms import CreateDocumentForm, UpdateDocumentForm


class HomeView(TemplateView):
    template_name = 'main/home.html'



class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard.html'
    login_url = reverse_lazy('home')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     filepath = os.path.join('static', 'sample_pdf.pdf')
    #     context['pdf_doc'] = FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    #     return context

def show_pdf(request):
    filepath = os.path.join('static', 'doc_pdf.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def show_user_pdf(request):
    pdf = str(UserDocument.objects.get(user_id=request.user))
    filepath = os.path.join('media', pdf)
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')




class MyFile(LoginRequiredMixin, TemplateView):
    template_name = 'main/my_file.html'
    login_url = reverse_lazy('login_user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user_file'] = UserDocument.objects.get(user_id=self.request.user.id)
        except Exception:
            context['user_file'] = None
        return context

class UploadDocument(CreateView):
    template_name = 'main/upload_file.html'
    form_class = CreateDocumentForm
    success_url = reverse_lazy('my_file')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UpdateDocument(UpdateView):
    model = UserDocument
    template_name = 'main/update_document.html'
    form_class = UpdateDocumentForm
    success_url = reverse_lazy('my_file')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DeleteDocument(DeleteView):
    model = UserDocument
    template_name = 'main/delete_document.html'
    success_url = reverse_lazy('my_file')
