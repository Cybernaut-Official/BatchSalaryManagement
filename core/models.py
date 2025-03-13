from django.db import models

# Month choices
MONTH_CHOICES = [
    ('January', 'January'), ('February', 'February'), ('March', 'March'),
    ('April', 'April'), ('May', 'May'), ('June', 'June'),
    ('July', 'July'), ('August', 'August'), ('September', 'September'),
    ('October', 'October'), ('November', 'November'), ('December', 'December')
]

# Year choices (Dynamic range from 2020 to 2035)
YEAR_CHOICES = [(str(year), str(year)) for year in range(2020, 2036)]


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch_number = models.PositiveIntegerField(unique=False)  # Unique batch number
    batch_name = models.CharField(max_length=10, unique=False, blank=True)  # Auto-generated
    year = models.CharField(max_length=4, choices=YEAR_CHOICES)
    month = models.CharField(max_length=20, choices=MONTH_CHOICES)

    def save(self, *args, **kwargs):
        if not self.batch_name:  # Auto-generate batch name
            self.batch_name = f"B{self.batch_number}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.name} - ({self.month} {self.year} - {self.batch_name})"


class ExtraCourse(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    lecture_name = models.CharField(max_length=255)
    salary_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=20,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.lecture_name} - {self.course_name} ({self.batch.month} {self.batch.year} - {self.batch.batch_name})"
