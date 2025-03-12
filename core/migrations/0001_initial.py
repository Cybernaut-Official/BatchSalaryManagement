# Generated by Django 5.1.7 on 2025-03-12 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.PositiveIntegerField(unique=True)),
                ('batch_name', models.CharField(blank=True, max_length=10, unique=True)),
                ('year', models.CharField(choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029'), ('2030', '2030'), ('2031', '2031'), ('2032', '2032'), ('2033', '2033'), ('2034', '2034'), ('2035', '2035')], max_length=4)),
                ('month', models.CharField(choices=[('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'), ('May', 'May'), ('June', 'June'), ('July', 'July'), ('August', 'August'), ('September', 'September'), ('October', 'October'), ('November', 'November'), ('December', 'December')], max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
            ],
        ),
        migrations.CreateModel(
            name='ExtraCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('lecture_name', models.CharField(max_length=255)),
                ('salary_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pending_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Partial', 'Partial')], default='Pending', max_length=20)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.batch')),
            ],
        ),
    ]
