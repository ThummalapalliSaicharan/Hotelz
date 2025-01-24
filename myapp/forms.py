from django import forms
from .models import Feedback  # Adjust import according to your structure

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['location','comments', 'rating']  # Include all fields

        # You can customize widgets if necessary, but not required for this case
