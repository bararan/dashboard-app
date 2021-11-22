from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from xhtml2pdf import pisa
import csv
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
from profiles.models import Profile
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer


# Create your views here.

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def create_report_view(req):
    if req.is_ajax():
        name = req.POST.get('name')
        remarks = req.POST.get('remarks')
        image = req.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=req.user)
        # Report.objects.create(
        #     name = name,
        #     remarks = remarks,
        #     image = img,
        #     author = author,
        # )
        form = ReportForm(req.POST or None)
        if form.is_valid():
            image = req.POST.get('image')
            img = get_report_image(image)
            author = Profile.objects.get(user=req.user)
            instance = form.save(commit=False) #So that the new object is not committed to the db yet.
            instance.image = img
            instance.author = author
            instance.save()
        return HttpResponse('')#JsonResponse({})

@login_required
def render_pdf_view(req, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    print(obj.image.path)
    print(obj.image.url)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"' #This one creates a downloadable pdf
    response['Content-Disposition'] = 'filename="report.pdf"' #This one opens the generated pdf in the same tab.
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def csv_upload_view(req):
    if req.method == 'POST':
        csv_file = req.FILES.get('file')
        file_name = csv_file.name
        obj, created = CSV.objects.get_or_create(file_name=file_name)
        if not created:
            return JsonResponse({'msg': file_name + ' already uploaded.', 'type': 'danger'})
        obj.csv_file = csv_file
        obj.save()
        with open(obj.csv_file.path, 'r') as f:
            msg_text = 'File successfully uploaded.'
            alert_type = 'success'
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                sale_id = row[1]
                prod_name = row[2]
                quantity = int(row[3])
                customer_name = row[4]
                sale_date = parse_date(row[5])
                try:
                    product = Product.objects.get(name__iexact=prod_name) # __iexact makes the search case insensitive.
                    customer, _ =Customer.objects.get_or_create(name__iexact=customer_name) # The second, suppressed output is True if obj is created.
                    position = Position.objects.create(product=product, quantity=quantity, created=sale_date)
                    seller = Profile.objects.get(user=req.user)
                    sale, _ = Sale.objects.get_or_create(
                        sale_id=sale_id,
                        customer=customer,
                        seller=seller,
                        created = sale_date
                    )
                    sale.positions.add(position)
                    sale.save()
                except Product.DoesNotExist:
                    alert_type = 'warning'
                    msg_text += '<br>' + prod_name + ' does not exist. Skipped transaction #' + row[0]
        return JsonResponse({'msg': msg_text, 'type': alert_type})