from django.forms import ModelForm
from .models import Discussion

class DiscussionForm(ModelForm):
    class Meta:
        model=Discussion
        fields = '__all__'
        exclude=['host','participants']
