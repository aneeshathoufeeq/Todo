
        # auth_user :table in sqlite

from django import forms
from .models import Taskmodel ,User # Import your Taskmodel

class TaskForm(forms.ModelForm):
    class Meta:
        model = Taskmodel
        fields = ['task_name', 'task_description'] 
        widgets={
            'task_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter task name'}),
            'task_description':forms.Textarea(attrs={'class':'form-control','column':20,"rows":5,'placeholder':'Enter task description'}) 
        }
         # Specify the fields you want to include in the form

class Register(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","first_name","last_name","email","password"]
        widgets={
    'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username'}),
    'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter firstname'}),
    'last_name':forms.TextInput(attrs={'class':'form-control',"placeholder":"Enter last name"}),
    'email':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter email'}),
    'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'})}

# login form

class Loginform(forms.Form):
    username=forms.CharField()
    password=forms.CharField()
    widgets={
    'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username'}),
    'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'})}
