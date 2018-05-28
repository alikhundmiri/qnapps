from django import forms

from .models import questions, answers

class QuestionForm(forms.ModelForm):
	class Meta:
		model = questions
		fields = [
		"question",
			]

	def __init__(self, user, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.fields["question"].help_text = "Your Question Here, in less then 180 characters"
		self.fields['question'].widget.attrs.update({
			'maxlength': "179"
			})

class AnswerForm(forms.ModelForm):
	class Meta:
		model = answers
		fields = [
		# 'question_ref',
		'app_name',
		'app_url',
			]

	def __init__(self, user, *args, **kwargs):
		super(AnswerForm, self).__init__(*args, **kwargs)
		# self.fields["question_ref"].help_text = ""
		self.fields["app_name"].help_text = "App Name"
		self.fields["app_url"].help_text = "URL to the app/Website"

class GeneralAnswerForm(forms.ModelForm):
	class Meta:
		model = answers
		fields = [
		'question_ref',
		'app_name',
		'app_url',
			]

	def __init__(self, user, *args, **kwargs):
		super(AnswerForm, self).__init__(*args, **kwargs)
		self.fields["question_ref"].help_text = ""
		self.fields["app_name"].help_text = "App Name"
		self.fields["app_url"].help_text = "URL to the app/Website"
