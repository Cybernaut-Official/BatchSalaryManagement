from django.shortcuts import render
from .models import ExtraCourse
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from datetime import datetime
from django.core.paginator import Paginator
from django.utils.timezone import now

def dashboard(request):
    current_year = datetime.now().year
    current_month = datetime.now().strftime("%B")

    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    existing_years = set(map(int, ExtraCourse.objects.values_list("batch__year", flat=True)))
    year_range = set(range(current_year - 5, current_year + 6))
    all_years = sorted(existing_years.union(year_range))

    selected_year = int(request.GET.get("year", current_year))
    selected_month = request.GET.get("month", current_month)

    # Fetch filtered data
    filtered_data = ExtraCourse.objects.filter(batch__year=str(selected_year), batch__month=selected_month)

    # Implement Pagination (10 records per page)
    paginator = Paginator(filtered_data, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "extra_courses": page_obj,  # Pass paginated data
        "years": all_years,
        "months": months,
        "selected_year": selected_year,
        "selected_month": selected_month,
    }
    return render(request, "dashboard.html", context)

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
    table_data = [["Course", "Batch", "Lecturer", "Course Name", "Salary", "Paid", "Status"]]  # Header Row

    for record in salary_records:
        table_data.append([
            record.batch.course.name,
            record.batch.batch_name,
            record.lecture_name,
            record.course_name,
            str(record.salary_paid),
            str(record.salary_paid),
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

def get_annual_report(request):
    selected_year = request.GET.get("year", None)
    if not selected_year:
        selected_year = str(now().year)

    salary_entries = ExtraCourse.objects.filter(batch__year=selected_year)

    monthly_data = {}
    monthly_totals = {}

    for entry in salary_entries:
        month_name = entry.batch.month  

        if month_name not in monthly_data:
            monthly_data[month_name] = []
            monthly_totals[month_name] = {"total_paid": 0, "total_pending": 0}  # Initialize totals

        monthly_data[month_name].append(entry)
        monthly_totals[month_name]["total_paid"] += entry.salary_paid
        monthly_totals[month_name]["total_pending"] += entry.pending_amount

    # Extract numeric totals for display
    total_yearly_paid = sum(value["total_paid"] for value in monthly_totals.values())
    total_yearly_pending = sum(value["total_pending"] for value in monthly_totals.values())

    context = {
        "selected_year": selected_year,
        "monthly_data": monthly_data,
        "monthly_totals": monthly_totals,
        "total_yearly_paid": total_yearly_paid,
        "total_yearly_pending": total_yearly_pending,
    }

    return render(request, "annual_report.html", context)
