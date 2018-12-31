from django import forms
from app.models import *

class ExamForm(forms.ModelForm):

    new_subject = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder':'Ex: Math'}
    ), label='Add Subject')
    class Meta:
        model = Exam
        fields = ['new_subject', 'passed', 'date_passed', 'grade']
        widgets = {
            'passed': forms.CheckboxInput(attrs={'class': 'ml-2 js-switch'}),
            'date_passed': forms.DateInput(attrs={'class': 'form-control datetimepicker-input', 'placeholder': 'YYYY-MM-DD'}),
            'grade': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Ex: 25'}),
        }

class EditExamForm(forms.Form):
    passed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'form-control js-switch'}))
    date_passed = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control datetimepicker-input'}), required=False)
    grade = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)

class CreatePostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-controlm summernote'}))
    class Meta:

        model = Post
        fields = ['title', 'body']
        widgets= {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control summernote'}))
    class Meta:

        model = Post
        fields = ['body']
