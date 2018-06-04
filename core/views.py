from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count, Q

from .models import questions, answers

from .forms import QuestionForm, AnswerForm

def lander(request):
	context = {
		'message' : "welcome to QnAPPs"
	}
	return render(request, 'landing.html', context)

# POPULAR
def index(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect(reverse('core:browse_popular'))
		pass
	else:
		return HttpResponseRedirect(reverse('core:lander'))

def browse_popular(request):
	# q_s = questions.objects.order_by('-app_answer__timestamp')

	"""
	This line needs to filter out these things in sequence.
	1. questions which are qc_pass==True
	2. answers to those each questions which are qc_pass==True
	3. order these questions by the onces with most answers to questions with least answers

	steps  1 and 3 are ok. Step 2 is where I am stuck at.
	"""
	q_s = questions.objects.filter(qc_pass=True).annotate(relevent_answer=Count('app_answer', filter=Q(app_answer__qc_pass=True))).order_by('-relevent_answer').distinct()



	query = request.GET.get("q")
	if query:
		q_s = q_s.filter(
			Q(question__icontains=query)|
			Q(app_answer__app_name__icontains=query)
		).distinct()

	paginator = Paginator(q_s, 10) # show 10 Blogs per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		q_s_sort = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		q_s_sort = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		q_s_sort = paginator.page(paginator.num_pages)



	context = {
		'sort_by' : "browse_popular",
		"page_request_var" : page_request_var,
		"questions" : q_s_sort,
	}
	return render(request, 'index.html', context)

def browse_new(request):
	q_s = questions.objects.filter(qc_pass=True).order_by('-timestamp')

	query = request.GET.get("q")
	if query:
		q_s = q_s.filter(
			Q(question__icontains=query)|
			Q(app_answer__app_name__icontains=query)
		).distinct()

	paginator = Paginator(q_s, 10) # show 10 Blogs per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		q_s_sort = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		q_s_sort = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		q_s_sort = paginator.page(paginator.num_pages)

	context = {
		'sort_by' : "browse_new",
		"page_request_var" : page_request_var,
		"questions" : q_s_sort,
	}
	return render(request, 'index.html', context)

# This has been disabled 
def browse_trend(request):
	"""
	This needs to filter new quetions and apps with qc_pass=True.
	it should load all 
	"""
	q_s = questions.objects.filter(qc_pass=True).order_by('app_answer').distinct()
	context = {
		'sort_by' : "browse_trend",
		'questions' : q_s,
	}
	return render(request, 'index.html', context)

def browse_favourite(request):
	q_s = questions.objects.filter(qc_pass=True).order_by('timestamp')
	context = {
		'sort_by' : "browse_favourite",
		'questions' : q_s,
	}
	return render(request, 'index.html', context)

def question_detail(request, id=None):
	question = get_object_or_404(questions, id=id)

	if question.qc_pass == False:
		if request.user != question.user:		
			raise Http404

	context = {
		'question' : question
	}

	return render(request, 'question_detail.html', context)

@login_required
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

@login_required
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

@user_passes_test(lambda u: u.is_superuser)
def superuser_index(request, username=None):
	q_s = questions.objects.all().count()
	q_s_pending = questions.objects.filter(qc_pass=False).count()

	a_s = answers.objects.all().count()
	a_s_pending = answers.objects.filter(qc_pass=False).count()

	if not request.user.is_authenticated:
		raise Http404

	context = {
		'questions' : q_s,
		'questions_pending' : q_s_pending,

		'answers' : a_s,
		'answers_pending' : a_s_pending,
	}
	return render(request, 'superuser_index.html', context)

@user_passes_test(lambda u: u.is_superuser)
def superuser_qc(request, username=None):
	if not request.user.is_authenticated:
		raise Http404

	context = {
	}
	return render(request, 'superuser_index.html', context)