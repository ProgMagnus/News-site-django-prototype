from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

class HomeNews(ListView):
	model = News
	template_name= 'news/home.html'
	context_object_name = 'news'
	paginate_by = 2

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Main page'
		return context

	def get_queryset(self):
		return News.objects.filter(is_published=True).select_related('category')

class NewsByCaregory(ListView):
	model = News
	template_name = 'news/home.html'
	context_object_name = 'news'
	allow_empty = False
	paginate_by = 2

	def get_queryset(self):
		return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
		return context

class ViewNews(DetailView):
	model = News
	template_name = 'news/view_news.html'
	context_object_name = 'news_item'

class AddNews(LoginRequiredMixin, CreateView):
	form_class = NewsForm
	template_name = 'news/add_news.html'
	raise_exception = True

def register(request):
	if request.method=='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Your registration was successful')
			return redirect('home')
		else:
			messages.error(request, 'Registration error')
	else:
		form = UserRegisterForm()
	return render(request, 'news/register.html',{'form': form})

def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('home')
	else:
		form = UserLoginForm()

	return render(request, 'news/login.html', {'form': form})

def user_logout(request):
	logout(request)
	return redirect('login')

def email_func(request):
	if request.method=='POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'djangolord@ukr.net', ['nanadar164@5ubo.com'], fail_silently=True)
			if mail:
				messages.success(request, 'email sent')
				return redirect('email')
			else:
				messages.error(request, 'fail')
		else:
			messages.error(request, 'fail')
	else:
		form = ContactForm()
	return render(request, 'news/email.html',{'form': form})