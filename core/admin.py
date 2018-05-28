from django.contrib import admin
from .models import questions, answers
# Register your models here.

class AnswersAdmin(admin.ModelAdmin):
	list_display = ['user', 'question_ref', 'app_name', "timestamp", 'updated', 'qc_pass']
	list_filter = [ 'qc_pass', 'user', 'app_name', 'app_url', "timestamp", 'updated', 'question_ref']
	search_field = ['user', 'app_name', 'app_url', "timestamp", 'updated', 'question_ref', 'qc_pass']
	list_editable = ['qc_pass']
	class Meta:
		model = answers

class QuestionsAdmin(admin.ModelAdmin):
	list_display = ['user', 'question', 'timestamp', 'updated', 'qc_pass']
	list_filter = [ 'qc_pass', 'user', 'question', 'timestamp', 'updated']
	search_field = ['user', 'question', 'timestamp', 'updated', 'qc_pass']
	list_editable = ['qc_pass']
	class Meta:
		model = questions

admin.site.register(answers, AnswersAdmin)
admin.site.register(questions, QuestionsAdmin)