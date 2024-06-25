try:
    import jinja2
    import pdfkit
    from num2words import num2words
    import os
except ImportError as e:
    missing_module = str(e).split(' ')[-1]
    print(f"The module {missing_module} is not installed.")
    print("Please install the required module using:")
    print(f"pip install {missing_module}")
    exit()

# Your existing code follows here...
def render_template(template_path, context):
    path, filename = os.path.split(template_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(context)

def generate_invoice(data):
    # Calculate derived fields
    for item in data['items']:
        item['net_amount'] = item['unit_price'] * item['quantity'] - item.get('discount', 0)
        item['tax_type'] = 'CGST/SGST' if data['place_of_supply'] == data['place_of_delivery'] else 'IGST'
        if item['tax_type'] == 'CGST/SGST':
            item['cgst'] = item['net_amount'] * 0.09
            item['sgst'] = item['net_amount'] * 0.09
            item['total_amount'] = item['net_amount'] + item['cgst'] + item['sgst']
        else:
            item['igst'] = item['net_amount'] * 0.18
            item['total_amount'] = item['net_amount'] + item['igst']
    
    data['total_amount'] = sum(item['total_amount'] for item in data['items'])
    data['amount_in_words'] = num2words(data['total_amount'], to='currency', lang='en')

    # Render the HTML template
    html_out = render_template('invoice_template.html', data)

    # Generate PDF from HTML
    pdfkit.from_string(html_out, 'invoice.pdf')

data = {
    'company_logo': 'path/to/logo.png',
    'seller_details': {
        'name': 'Seller Name',
        'address': 'Seller Address',
        'city': 'City',
        'state': 'State',
        'pincode': '123456',
        'pan': 'ABCDE1234F',
        'gst': '12ABCDE3456F1Z2'
    },
    'place_of_supply': 'State',
    'billing_details': {
        'name': 'Customer Name',
        'address': 'Customer Address',
        'city': 'City',
        'state': 'State',
        'pincode': '123456',
        'state_code': '12'
    },
    'shipping_details': {
        'name': 'Customer Name',
        'address': 'Customer Address',
        'city': 'City',
        'state': 'State',
        'pincode': '123456',
        'state_code': '12'
    },
    'place_of_delivery': 'State',
    'order_details': {
        'order_no': '123456',
        'order_date': '2024-06-25'
    },
    'invoice_details': {
        'invoice_no': 'INV-123456',
        'invoice_date': '2024-06-26'
    },
    'reverse_charge': 'No',
    'items': [
        {
            'description': 'Item 1',
            'unit_price': 100.0,
            'quantity': 2,
            'discount': 10.0,
            'tax_rate': 0.18
        },
        {
            'description': 'Item 2',
            'unit_price': 200.0,
            'quantity': 1,
            'discount': 0.0,
            'tax_rate': 0.18
        }
    ],
    'signature_image': 'path/to/signature.png'
}

generate_invoice(data)
