# 🛍️ Shopify Products Importer

A small **Django-based web app** that fetches products from a **public Shopify store JSON endpoint** (`/products.json`) and generates a CSV formatted according to **Shopify’s official product import template**.

---

## 🚀 What This Project Does

✅ Accepts a **Shopify store base URL** (e.g., `https://examplestore.myshopify.com`)  
✅ Iterates through paginated `/products.json` pages (`?limit=250&page=N`) until no products remain  
✅ Adjusts **inventory & pricing** for each primary variant:  
- **Price:** adds `+1000` to variant price  
- **Compare-at-price:** sets to `double` of adjusted price  
- **Inventory:** forces minimum `100` if inventory quantity is below 100  

✅ Generates a CSV with:  
- Handles, titles, descriptions, vendor, options  
- Variant info (price, inventory, compare-at-price, SKU, etc.)  
- Image URLs & positions  
- Google Shopping fields, metafields, and placeholders for empty Shopify columns  

✅ Saves CSV in `MEDIA_ROOT` and provides a **download URL** in the UI  

---

## 🏃‍♂️ Quick Start (Development)

### 1️⃣ Create and Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

### 2️⃣ Install Dependencies
pip install django requests

### 3️⃣ Run Migrations
python manage.py migrate

### 4️⃣ Start Development Server
python manage.py runserver

### 5️⃣ Open in Browser
Go to *http://127.0.0.1:8000/* and enter the Shopify store URL

👨‍💻 Author
Muneeb Ali
📧 muneeb00ali@gmail.com
