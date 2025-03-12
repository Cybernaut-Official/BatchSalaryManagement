from django import forms
from .models import Course, Batch, ExtraCourse, MONTH_CHOICES, YEAR_CHOICES


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']


class BatchForm(forms.ModelForm):
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    month = forms.ChoiceField(choices=MONTH_CHOICES)

    class Meta:
        model = Batch
        fields = ['course', 'batch_number', 'year', 'month']


class ExtraCourseForm(forms.ModelForm):
    payment_status = forms.ChoiceField(
        choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Partial', 'Partial')]
    )

    class Meta:
        model = ExtraCourse
        fields = ['batch', 'course_name', 'lecture_name', 'salary_paid', 'pending_amount', 'payment_status']
