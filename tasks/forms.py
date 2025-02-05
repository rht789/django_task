from django import forms
from tasks.models import Task
# from tasks.models import *

# Django Form
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label='Assigned To')
    
    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees",[])
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id,emp.name) for emp in employees
        ]
        
#Django Model Form
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['title', 'description', 'due_date', 'assigned_to']
        # exclude = ['project', 'is_completed', 'created_at','updated_at']
        widgets = {
            'due_date' : forms.SelectDateWidget,
            'assigned_to' : forms.CheckboxSelectMultiple
        }
        