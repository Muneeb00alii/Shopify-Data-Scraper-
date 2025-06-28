import csv
import io
import uuid
from django.shortcuts import render, redirect
from django.http import FileResponse
import requests
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import codecs


def home(request):
    context = {}

    if request.method == 'POST':
        store_url = request.POST.get('shopify_url')
        if not store_url:
            context['error'] = 'Please provide a valid Shopify store URL.'
            return render(request, 'home.html', context)

        products = []
        product_count = 0
        page = 1

        while True:
            json_url = f"{store_url}/products.json?limit=250&page={page}"
            response = requests.get(json_url)

            if response.status_code != 200:
                context['error'] = f"Failed to fetch products. Check the URL."
                break

            data = response.json()
            current_page_products = data.get('products', [])

            if not current_page_products:
                break

            for product in current_page_products:
                product_count += 1
                title = product.get('title', '')
                body_html = product.get('body_html', '')
                vendor = product.get('vendor', '')
                tags = ','.join(product.get('tags', []))
                handle = product.get('handle', '')
                images = [img.get('src') for img in product.get('images', [])]

                color = ""
                for option in product.get('options', []):
                    if 'Color' in option.get('name', ''):
                        color = option.get('values', [""])[0]
                        break

                for i, variant in enumerate(product.get('variants', [])):
                    if i == 0:
                        inventory_qty = max(variant.get('inventory_quantity', 0), 100)
                        adjusted_price = float(variant.get('price', 0)) + 1000
                        adjusted_compare_at_price = adjusted_price * 2

                        product_info = {
                            'Handle': handle,
                            'Title': title,
                            'Body (HTML)': body_html,
                            'Vendor': vendor,
                            'Product Category': "",
                            'Type': "",
                            'Tags': tags,
                            'Published': variant.get('created_at', ''),
                            'Option1 Name': "Title",
                            'Option1 Value': variant.get('title', ''),
                            'Option1 Linked To': "",
                            'Option2 Name': variant.get('option2', ''),
                            'Option2 Value': variant.get('option2', ''),
                            'Option2 Linked To': "",
                            'Option3 Name': variant.get('option3', ''),
                            'Option3 Value': variant.get('option3', ''),
                            'Option3 Linked To': "",
                            'Variant SKU': variant.get('sku', ''),
                            'Variant Grams': variant.get('grams', ''),
                            'Variant Inventory Tracker': "shopify",
                            'Variant Inventory Qty': inventory_qty,
                            'Variant Inventory Policy': "deny",
                            'Variant Fulfillment Service': "manual",
                            'Variant Price': adjusted_price,
                            'Variant Compare At Price': adjusted_compare_at_price,
                            'Variant Requires Shipping': "TRUE",
                            'Variant Taxable': "FALSE",
                            'Variant Barcode': variant.get('barcode', ""),
                            'Image Src': images[0] if images else None,
                            'Image Position': "1",
                            'Image Alt Text': "",
                            'Gift Card': "FALSE",
                            'SEO Title': "",
                            'SEO Description': "",
                            'Google Shopping / Google Product Category': "",
                            'Google Shopping / Gender': "",
                            'Google Shopping / Age Group': "adults; teens",
                            'Google Shopping / MPN': "",
                            'Google Shopping / Condition': "new",
                            'Google Shopping / Custom Product': "FALSE",
                            'Google Shopping / Custom Label 0': "",
                            'Google Shopping / Custom Label 1': "",
                            'Google Shopping / Custom Label 2': "",
                            'Google Shopping / Custom Label 3': "",
                            'Google Shopping / Custom Label 4': "",
                            'Age group (product.metafields.shopify.age-group)': "adults; teens",
                            'Bag/Case material (product.metafields.shopify.bag-case-material)': "",
                            'Carry options (product.metafields.shopify.carry-options)': "",
                            'Color (product.metafields.shopify.color-pattern)': color,
                            'Target gender (product.metafields.shopify.target-gender)': "female",
                            'Variant Image': images[0] if images else None,
                            'Variant Weight Unit': "kg",
                            'Variant Tax Code': "",
                            'Cost per item': "",
                            'Included / Pakistan': "",
                            'Price / Pakistan': adjusted_price,
                            'Compare At Price / Pakistan': adjusted_compare_at_price,
                            'Included / International': "",
                            'Price / International': "",
                            'Compare At Price / International': "",
                            'Status': "active",
                        }
                        products.append(product_info)

                    for j, image in enumerate(images[1:], start=1):
                        product_info_additional = {k: "" for k in product_info}
                        product_info_additional.update({
                            'Handle': handle,
                            'Title': title,
                            'Image Src': image,
                            'Image Position': str(j + 1),
                        })
                        products.append(product_info_additional)

            page += 1

        # Generate CSV in memory
        if products:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=products[0].keys())
            writer.writeheader()
            writer.writerows(products)

            file_content = output.getvalue()
            csv_bytes = file_content.encode('utf-8-sig')
            file_name = f"shopify_products_{uuid.uuid4().hex}.csv"
            file_path = default_storage.save(file_name, ContentFile(csv_bytes))
            context['csv_file_url'] = default_storage.url(file_path)
            context['csv_filename'] = file_name
            context['product_count'] = product_count

    return render(request, 'home.html', context)

def cancel_download(request):
    file = request.GET.get('file')
    if file:
        default_storage.delete(file)
    return redirect('home')
