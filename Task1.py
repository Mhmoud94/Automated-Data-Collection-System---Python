#!/usr/bin/env python
# coding: utf-8
"""
Task 1: Scrape textual information from 2 websites about AI/ML topics
Save this as: task1_scraping.py
Run with: python task1_scraping.py
"""

from bs4 import BeautifulSoup
import requests
import sys

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}

print("=" * 80)
print("TASK 1: WEB SCRAPING - STARTING")
print("=" * 80)

# ============================================================================
# WEBSITE 1: TechTarget - Machine Learning
# ============================================================================
print("\n[1/2] Scraping Website 1: TechTarget...")
url1 = "https://www.techtarget.com/searchenterpriseai/definition/machine-learning-ML"

try:
    r1 = requests.get(url1, headers=headers, timeout=15)
    print(f"    Status code: {r1.status_code}")
    
    if r1.status_code == 200:
        soup1 = BeautifulSoup(r1.content, "html.parser")
        
        # Extract headline
        headline1 = soup1.find("h1")
        headline1_text = headline1.text.strip() if headline1 else "No headline found"
        
        # Extract content
        content1 = []
        main_content = soup1.find("div", {"class": "main-content"})
        
        if main_content:
            # Get definition section
            definition = main_content.find("section", {"class": "section definition-section"})
            if definition:
                paragraphs = definition.find_all("p")
                for p in paragraphs:
                    text = p.text.strip()
                    if text:
                        content1.append(text)
            
            # Get main article chapters
            chapters = main_content.find_all("section", {"class": "section main-article-chapter"})
            for chapter in chapters:
                paragraphs = chapter.find_all("p")
                for p in paragraphs:
                    text = p.text.strip()
                    if text:
                        content1.append(text)
        
        print(f"    ✓ Success! Extracted {len(content1)} paragraphs")
        website1_success = True
    else:
        print(f"    ✗ Failed. Status code: {r1.status_code}")
        headline1_text = "N/A"
        content1 = []
        website1_success = False
        
except Exception as e:
    print(f"    ✗ Error: {e}")
    headline1_text = "N/A"
    content1 = []
    website1_success = False

# ============================================================================
# WEBSITE 2: IBM - Artificial Intelligence
# ============================================================================
print("\n[2/2] Scraping Website 2: IBM...")
url2 = "https://www.ibm.com/topics/artificial-intelligence"

try:
    r2 = requests.get(url2, headers=headers, timeout=15)
    print(f"    Status code: {r2.status_code}")
    
    if r2.status_code == 200:
        soup2 = BeautifulSoup(r2.content, "html.parser")
        
        # Extract headline
        headline2 = soup2.find("h1")
        headline2_text = headline2.text.strip() if headline2 else "No headline found"
        
        # Extract content from paragraphs
        content2 = []
        paragraphs = soup2.find_all("p")
        
        # Get first 10 meaningful paragraphs
        count = 0
        for p in paragraphs:
            text = p.text.strip()
            if len(text) > 50:  # Only meaningful paragraphs
                content2.append(text)
                count += 1
                if count >= 10:
                    break
        
        print(f"    ✓ Success! Extracted {len(content2)} paragraphs")
        website2_success = True
    else:
        print(f"    ✗ Failed. Status code: {r2.status_code}")
        headline2_text = "N/A"
        content2 = []
        website2_success = False
        
except Exception as e:
    print(f"    ✗ Error: {e}")
    headline2_text = "N/A"
    content2 = []
    website2_success = False

# ============================================================================
# SAVE TO FILE
# ============================================================================
print("\n" + "=" * 80)
print("SAVING RESULTS TO FILE")
print("=" * 80)

output_file = "task1_output.txt"

try:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("TASK 1: WEB SCRAPING - TEXTUAL INFORMATION\n")
        f.write("Topic: Machine Learning and Artificial Intelligence\n")
        f.write("=" * 80 + "\n\n")
        
        # Website 1
        f.write(f"SOURCE: TechTarget\n")
        f.write(f"URL: {url1}\n")
        f.write(f"Status: {'Success' if website1_success else 'Failed'}\n")
        f.write("-" * 80 + "\n")
        f.write(f"HEADLINE: {headline1_text}\n")
        f.write("-" * 80 + "\n")
        f.write("CONTENT:\n\n")
        
        if content1:
            for i, paragraph in enumerate(content1, 1):
                f.write(f"{paragraph}\n\n")
        else:
            f.write("No content extracted.\n\n")
        
        f.write("\n" + "=" * 80 + "\n\n")
        
        # Website 2
        f.write(f"SOURCE: IBM\n")
        f.write(f"URL: {url2}\n")
        f.write(f"Status: {'Success' if website2_success else 'Failed'}\n")
        f.write("-" * 80 + "\n")
        f.write(f"HEADLINE: {headline2_text}\n")
        f.write("-" * 80 + "\n")
        f.write("CONTENT:\n\n")
        
        if content2:
            for i, paragraph in enumerate(content2, 1):
                f.write(f"{paragraph}\n\n")
        else:
            f.write("No content extracted.\n\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"✓ Successfully saved to: {output_file}")
    
except Exception as e:
    print(f"✗ Error saving file: {e}")

# ============================================================================
# DISPLAY SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nWebsite 1 (TechTarget):")
print(f"  Status: {'✓ Success' if website1_success else '✗ Failed'}")
print(f"  Headline: {headline1_text[:60]}...")
print(f"  Paragraphs: {len(content1)}")

print(f"\nWebsite 2 (IBM):")
print(f"  Status: {'✓ Success' if website2_success else '✗ Failed'}")
print(f"  Headline: {headline2_text[:60]}...")
print(f"  Paragraphs: {len(content2)}")

print(f"\n✓ Output saved to: {output_file}")
print(f"\nTo view results: Open '{output_file}' in a text editor")
print("\n" + "=" * 80)
print("TASK 1 COMPLETED!")
print("=" * 80)