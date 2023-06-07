from django import forms
from .models import BookedRoom, TimeSlot

class BookingForm(forms.ModelForm):
    Booked_By = forms.CharField(max_length=100, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
    Time = forms.ModelChoiceField(queryset=TimeSlot.objects.all(), widget=forms.RadioSelect)
    class Meta:
        model = BookedRoom
        fields = ('Room','Booked_By','Date','Time_From')