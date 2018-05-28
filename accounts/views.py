from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, Http404

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	update_session_auth_hash
)
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404

from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
	next = ""

	if request.GET:  
		next = request.GET['next']

	dbug = settings.DEBUG
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request,user)
		if next == "":
			return HttpResponseRedirect("/")
			# return HttpResponseRedirect(reverse('user:home'))
		else:
			return HttpResponseRedirect(next)

	context = {
		"name_nav" : 'login',
		"nbar" : "login",
		"form" : form,
		"dbug" : dbug,
		'page' : 'full-page',

	}
	return render(request, 'accounts/login.html', context)

def register_view(request):
	next = ""

	if request.GET:
		next = request.GET['next']

	dbug = settings.DEBUG
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)

		login(request, new_user)
		# change redirect to edit bio page
		# return HttpResponseRedirect("/")
		return HttpResponseRedirect(reverse('core:home'))
	context = {
		"name_nav" : 'register',	
		"nbar" : "register",
		"form" : form,
		'dbug' : dbug,
		'page' : 'full-page',
	}
	return render(request, 'accounts/login.html', context)

@login_required
def logout_view(request):
	logout(request)
	return redirect('/')