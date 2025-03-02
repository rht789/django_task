from django import forms
from tasks.models import Task,TaskDetail
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

class StyledFormMixin:
    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
    
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_classes,
                    'placeholder':f"Enter {field.label.lower()}"
                }) 
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 bg-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })   
    
#Django Model Form
class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }
        # exclude = ['project', 'is_completed', 'created_at','updated_at']
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': (
        #             "block w-full px-4 py-2 border border-gray-300 "
        #             "rounded-md shadow-sm focus:outline-none focus:ring-rose-200 focus:border-rose-500"
        #         ),
        #         'placeholder': "Enter Task Title"
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': (
        #             "block w-full px-4 py-2 border border-gray-300 "
        #             "rounded-md shadow-sm focus:ring-rose-200 focus:border-rose-500"
        #         ),
        #         'placeholder': "Describe your task",
        #         'rows': 4  # Makes the textarea a bit taller
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': (
        #             "px-4 py-2 border border-gray-300 "
        #             "rounded-md shadow-sm focus:ring-rose-200 focus:border-rose-500"
        #         )
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         # Tailwind doesn't style checkboxes by default,
        #         # so here we're applying some utility classes.
        #         'class': "form-checkbox h-5 w-5 text-rose-600"
        #     }),
        # }
class TaskDetailModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model=TaskDetail
        fields=['priority','notes']