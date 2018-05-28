from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count

from .models import questions, answers

from .forms import QuestionForm, AnswerForm

def lander(request):
	context = {
		'message' : "welcome to QnAPPs"
	}
	return render(request, 'landing.html', context)

def index(request):
	# q_s = questions.objects.order_by('-app_answer__timestamp')

	q_s = questions.objects.annotate(count=Count('app_answer')).order_by('-count')

	context = {
		'sort_by' : "browse_popular",
		"questions" : q_s,
	}
	return render(request, 'index.html', context)

def browse_new(request):
	q_s = questions.objects.order_by('-timestamp', '-app_answer__timestamp')
	context = {
		'sort_by' : "browse_new",
		'questions' : q_s,
	}
	return render(request, 'index.html', context)


def browse_trend(request):
	q_s = questions.objects.order_by('app_answer')
	context = {
		'sort_by' : "browse_trend",
		'questions' : q_s,
	}
	return render(request, 'index.html', context)


def browse_favourite(request):
	q_s = questions.objects.order_by('timestamp')
	context = {
		'sort_by' : "browse_favourite",
		'questions' : q_s,
	}
	return render(request, 'index.html', context)

def question_detail(request, id=None):
	question = get_object_or_404(questions, id=id)

	context = {
		'question' : question
	}

	return render(request, 'question_detail.html', context)


def new_question(request, username=None):
	if not request.user.is_authenticated:
		raise Http404

	user = get_object_or_404(User, username=username)

	if request.method == 'POST':
		form = QuestionForm(user, request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			if 'submit_answer' in request.POST:
				print("New answer")
				return HttpResponseRedirect(reverse('core:new_answer', args=[user, instance.id]))
			elif 'simple_submit' in request.POST:
				print("plain submit")		
				return HttpResponseRedirect(reverse('core:question_detail', args=[instance.id]))
	else:
		form = QuestionForm(user)

	context = {
		'form' : form,
		"tab_text": "Submit",
		"top_text": "New Question",
		"form_text": "Make sure your question is New and Unique.",
	}
	return render(request, 'question_form.html', context)

def new_answer(request, username=None, id=None):
	if not request.user.is_authenticated:
		raise Http404

	user = get_object_or_404(User, username=username)
	question = get_object_or_404(questions, id=id)
	if request.method == 'POST':
		form = AnswerForm(user, request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.question_ref = question
			instance.save()
			return HttpResponseRedirect(reverse('core:question_detail', args=[question.id]))
	else:
		form = AnswerForm(user)

	context = {
		'question' : question,
		'form' : form,
		"tab_text": "Submit Answer!",
		"top_text": "New answer to ",
		"form_text": "New Answer",
	}
	return render(request, 'answer_form.html', context)
