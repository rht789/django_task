from django import forms
# from tasks.models import *

class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')
    
    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees",[])
        super().__init__(*args,**kwargs)
        print(args,kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id,emp.name) for emp in employees
        ]