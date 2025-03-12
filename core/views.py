from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import ExtraCourse
from .forms import CourseForm, BatchForm, ExtraCourseForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

def dashboard(request):
    extra_courses = ExtraCourse.objects.all()
    years = [year for year in range(2020, 2036)]  # Dynamic years for dropdown

    return render(request, "dashboard.html", {"extra_courses": extra_courses, "years": years})

def export_monthly_pdf(request):
    month = request.GET.get("month")
    year = request.GET.get("year")

    if not month or not year:
        return HttpResponse("Please select a valid month and year.", status=400)

    salary_records = ExtraCourse.objects.filter(batch__year=year, batch__month=month)

    total_paid = sum(record.salary_paid for record in salary_records)
    total_pending = sum(record.pending_amount for record in salary_records)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Salary_Report_{month}_{year}.pdf"'

    p = canvas.Canvas(response, pagesize=landscape(A4))  # Landscape Mode
    width, height = landscape(A4)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(250, height - 50, f"Salary Report - {month} {year}")

    y_position = height - 100

    # Table Header & Data
    table_data = [["Course", "Batch", "Lecturer", "Course Name", "Paid", "Pending", "Status"]]  # Header Row

    for record in salary_records:
        table_data.append([
            record.batch.course.name,
            record.batch.batch_name,
            record.lecture_name,
            record.course_name,
            str(record.salary_paid),
            str(record.pending_amount),
            record.payment_status
        ])

    # Set column widths
    col_widths = [120, 100, 120, 120, 80, 80, 100]  # Adjusted for landscape mode

    # Create Table
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    # Check for pagination
    table_height = len(salary_records) * 20 + 40  # Estimated table height
    if y_position - table_height < 100:  # If not enough space, move to a new page
        p.showPage()
        y_position = height - 100

    # Draw Table
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, y_position - len(salary_records) * 20 - 50)

    y_position -= len(salary_records) * 20 + 80  # Move below the table

    # Summary
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, f"Total Salary Paid: {total_paid}")
    p.drawString(50, y_position - 20, f"Total Pending Salary: {total_pending}")

    # Admin Signature
    p.drawString(500, y_position - 60, "Admin Signature: _______________")

    p.showPage()
    p.save()
    return response

def export_annual_pdf(request):
    year = request.GET.get("year")

    if not year:
        return HttpResponse("Please select a valid year.", status=400)

    salary_records = ExtraCourse.objects.filter(batch__year=year)

    total_paid = sum(record.salary_paid for record in salary_records)
    total_pending = sum(record.pending_amount for record in salary_records)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Annual_Salary_Report_{year}.pdf"'

    p = canvas.Canvas(response, pagesize=landscape(A4))  # Landscape mode
    width, height = landscape(A4)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(250, height - 50, f"Annual Salary Report - {year}")

    y_position = height - 100

    # Table Header & Data
    table_data = [["Course", "Batch", "Lecturer", "Course Name", "Paid", "Pending", "Status"]]  # Header Row

    for record in salary_records:
        table_data.append([
            record.batch.course.name,
            f"{record.batch.batch_name} ({record.batch.month})",
            record.lecture_name,
            record.course_name,
            str(record.salary_paid),
            str(record.pending_amount),
            record.payment_status
        ])

    # Set column widths
    col_widths = [120, 120, 120, 120, 80, 80, 100]  # Adjusted for landscape mode

    # Create Table
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    # Check for pagination
    table_height = len(salary_records) * 20 + 40  # Estimated table height
    if y_position - table_height < 100:  # If not enough space, move to a new page
        p.showPage()
        y_position = height - 100

    # Draw Table
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, y_position - len(salary_records) * 20 - 50)

    y_position -= len(salary_records) * 20 + 80  # Move below the table

    # Summary
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y_position, f"Total Salary Paid: {total_paid}")
    p.drawString(50, y_position - 20, f"Total Pending Salary: {total_pending}")

    # Admin Signature
    p.drawString(500, y_position - 60, "Admin Signature: _______________")

    p.showPage()
    p.save()
    return response
