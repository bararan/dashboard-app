from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from .models import Sale
from .forms import SaleSearchForm
from .utils import get_customer_from_id, get_seller_from_id, get_date_from_datetime, get_chart
from reports.forms import ReportForm
# Create your views here.

@login_required
def home_view(req):
    sales_data = None
    positions_data = None
    merged_data = None
    main_data = None
    chart = None
    is_post = False
    report_form = ReportForm()
    search_form = SaleSearchForm(req.POST or None)
    if req.method == 'POST':
        is_post = True
        date_from = req.POST.get('date_from')
        date_to = req.POST.get('date_to')
        chart_type = req.POST.get('chart_type')
        group_var = req.POST.get('group_by')
        qs = Sale.objects.filter(
            created__date__gte=date_from, # leaving out __date generates a warning that the field is interpreted as a naive date
            created__date__lte=date_to
        )
        if len(qs) > 0:
            sales_df = pd.DataFrame(qs.values()) # Data will have field names as column headers
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['seller_id'] = sales_df['seller_id'].apply(get_seller_from_id)
            sales_df['created'] = sales_df['created'].apply(get_date_from_datetime) # Can also use a lambda fn here: lambda x: x.strtime('%d/%m/%Y')
            sales_df['updated'] = sales_df['updated'].apply(get_date_from_datetime)
            sales_df.rename(
                {
                    'customer_id': 'customer',
                    'seller_id': 'salesman',
                },
                axis=1,
                inplace=True
            ) # inplace here ensures that the original dataframe is modified, so no (re)assignment is needed.
            sales_data = sales_df.to_html() #Converts the dataframe to an HTML object
            positions = []
            for s in qs:
                positions.extend(
                    [
                        {
                            'sale_id': p.get_sale_id(),
                            'position_id': p.id,
                            'product': p.product.name,
                            'quantity': p.quantity,
                            'price': p.price,
                        }
                        for p in s.get_positions()
                    ]
                )
            positions_df = pd.DataFrame(positions)
            positions_data = positions_df.to_html()
            merged_df = sales_df.merge(positions_df, on='sale_id')
            merged_data = merged_df.to_html()

            main_df = merged_df.groupby('sale_id', as_index=False)['price'].agg('sum')
            main_data = main_df.to_html()
            chart = get_chart(chart_type, sales_df, group_var)

    context = {
        'sales_data': sales_data,
        'report_form': report_form,
        'positions_data': positions_data,
        'merged_data': merged_data,
        'main_data': main_data,
        'chart': chart,
        'search_form': search_form,
        'is_post': is_post,
    }
    return render(req, 'sales/home.html', context)

class SalesListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailsView(LoginRequiredMixin, DetailView):
    model = Sale
    template_name = 'sales/detail.html'

''' If using the function views below instead of the class views above
    remember to change the url paths in urls.py as
    path('/sales', sale_list_view, name='sales'),
    path('/sales/<pk>', sale_details_view, name='details') 
'''
# def sale_list_view(req): #This one allows for filtering and can be used in place of the class view above
#     qry = Sale.objects.all()
#     return render(req, 'sales/main.html', {'object_list': qry})


# def sale_details_view(req, **kwargs):
#     pk = kwargs.get('pk')
#     obj = Sale.objects.get(pk=pk) #or obj=get_object_or_404(Sale, pk=pk)
#     return render(req, 'sales/detail.html', {'object': obj})
