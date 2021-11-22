import uuid, base64
import matplotlib.pyplot as mpl
import seaborn
from io import BytesIO
from customers.models import Customer
from profiles.models import Profile

def generate_code():
    return str(uuid.uuid4()).replace('-','').upper()[:12]

def get_customer_from_id(id):
    return Customer.objects.values_list('name').get(id=id)[0] # .filter returns a tuple of tuples, .get returns a tuple here

def get_seller_from_id(id):
    return Profile.objects.get(id=id).user.username

def get_date_from_datetime(dt):
    return dt.strftime('%d/%m/%Y')

def get_key(group_var):
    if group_var == '#1':
        return 'created'
    elif group_var == '#2':
        return 'sale_id'
    else:
        print("This should not happen and you need to raise an exception here!")

'''
Try to do this with e.g. bokeh instead of matplotlib
'''

def get_graph():
    buffer = BytesIO()
    mpl.savefig(buffer, format='png')
    buffer.seek(0) #move the cursor to the beginning of the buffer
    png_img = buffer.getvalue()
    graph = base64.b64encode(png_img) # 64-bit encode the bytes-like buffer object
    graph = graph.decode('utf-8') # decode as a utf-8 string
    buffer.close() # Free up memory
    return graph

def get_chart(chart_type, data, group_var, **kwargs):
    mpl.switch_backend('AGG')
    fig = mpl.figure(figsize=(10,4))
    key = get_key(group_var)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type == '#1':
        mpl.bar(d[key], d['total_price'])
        # seaborn.barplot(x=key, y='total_price', data=d)
    elif chart_type == '#2':
        labels = kwargs.get('labels')
        mpl.pie(data=d, x='total_price', labels=d[key].values)
    elif chart_type == '#3':
        mpl.plot(d[key], d['price'])
        # seaborn.lineplot(data=d, x=key, y='total_price')
    else:
        print('this should not happen and you need an exception here!')
    mpl.tight_layout() # Auto-adjusts chart size to figsize.
    return get_graph()