from django import forms
from quizzes.models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'subject', 'duration_minutes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quiz Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Quiz Description'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'topic', 'marks', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter question text'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topic'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Marks'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Question order'}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'order']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter answer text'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Answer order'}),
        }


class QuizAttemptForm(forms.Form):
    """Dynamic form for quiz attempt - answers are added dynamically"""
    def __init__(self, *args, quiz=None, **kwargs):
        super().__init__(*args, **kwargs)
        if quiz:
            for question in quiz.questions.all():
                field = forms.ModelChoiceField(
                    queryset=question.answers.all(),
                    widget=forms.RadioSelect,
                    label=question.text,
                    required=False
                )
                self.fields[f'question_{question.id}'] = field
