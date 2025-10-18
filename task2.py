#!/usr/bin/env python
# coding: utf-8
"""
Task 2: Scrape product names and prices from ONE e-commerce website
E-commerce Site: books.toscrape.com
Product Category: Science Books
Save this as: task2_scraping.py
Run with: python task2_scraping.py
"""

from bs4 import BeautifulSoup
import requests
import csv
import sys

print("=" * 80)
print("TASK 2: E-COMMERCE PRODUCT SCRAPING")
print("=" * 80)

# ============================================================================
# STEP 1: SETUP
# ============================================================================
# User-Agent header (makes request look like it's from a web browser)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}

# The e-commerce website we will scrape
url = "https://books.toscrape.com/catalogue/category/books/science_22/index.html"

print(f"\nWebsite: books.toscrape.com")
print(f"Category: Science Books")
print(f"URL: {url}")
print("\n" + "-" * 80)

# ============================================================================
# STEP 2: SEND REQUEST TO WEBSITE
# ============================================================================
print("\nStep 1: Connecting to website...")

try:
    # Send GET request to the website
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status code: {r.status_code}")
    
    # Check if request was successful
    if r.status_code == 200:
        print("✓ Successfully connected to website!")
    else:
        print("✗ Failed to connect. Scraping is not possible.")
        sys.exit(0)
        
except Exception as e:
    print(f"✗ Error connecting to website: {e}")
    sys.exit(0)

# ============================================================================
# STEP 3: PARSE HTML CONTENT
# ============================================================================
print("\nStep 2: Parsing HTML content...")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(r.content, "html.parser")
print("✓ HTML parsed successfully!")

# ============================================================================
# STEP 4: EXTRACT PRODUCT DATA
# ============================================================================
print("\nStep 3: Extracting product information...")

# List to store all products
products = []

# Find all product containers on the page
# Each product is in an <article> tag with class "product_pod"
product_containers = soup.find_all("article", class_="product_pod")

print(f"Found {len(product_containers)} products on the page")

# Loop through each product and extract name and price
for container in product_containers:
    try:
        # Extract Product Name
        # The name is in the "title" attribute of the <a> tag inside <h3>
        name_tag = container.find("h3").find("a")
        product_name = name_tag["title"] if name_tag else "N/A"
        
        # Extract Product Price
        # The price is in <p> tag with class "price_color"
        price_tag = container.find("p", class_="price_color")
        product_price = price_tag.text.strip() if price_tag else "N/A"
        
        # Add product to our list
        products.append({
            "name": product_name,
            "price": product_price
        })
        
    except Exception as e:
        # If there's an error with one product, skip it and continue
        continue

print(f"✓ Successfully extracted {len(products)} products!")

# ============================================================================
# STEP 5: DISPLAY PREVIEW
# ============================================================================
print("\n" + "=" * 80)
print("PREVIEW OF EXTRACTED DATA")
print("=" * 80)

if products:
    print(f"\nTotal products: {len(products)}\n")
    print("First 5 products:\n")
    
    for i, product in enumerate(products[:5], 1):
        print(f"{i}. Product: {product['name']}")
        print(f"   Price: {product['price']}\n")
else:
    print("\n✗ No products were extracted.")
    sys.exit(0)

# ============================================================================
# STEP 6: SAVE TO CSV FILE
# ============================================================================
print("=" * 80)
print("SAVING TO CSV FILE")
print("=" * 80)

# Output CSV filename
output_file = "task2_products.csv"

try:
    # Open CSV file for writing
    with open(output_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Write header row
        writer.writerow(["Product Name", "Price"])
        
        # Write all product data
        for product in products:
            writer.writerow([product["name"], product["price"]])
    
    print(f"\n✓ Successfully saved {len(products)} products to: {output_file}")
    
except Exception as e:
    print(f"\n✗ Error saving file: {e}")
    sys.exit(0)

# ============================================================================
# STEP 7: COMPLETION SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("TASK 2 COMPLETED SUCCESSFULLY!")
print("=" * 80)
print(f"\nWebsite scraped: books.toscrape.com")
print(f"Products found: {len(products)}")
print(f"Output file: {output_file}")
print("\nTo view results: Open 'task2_products.csv' in Excel or any text editor")
print("=" * 80)