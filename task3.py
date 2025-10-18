#!/usr/bin/env python
# coding: utf-8
"""
Task 3: Scrape weather data from 2 websites with error handling
Weather Websites:
  1. wttr.in (Simple weather API)
  2. timeanddate.com (Weather information site)
Save this as: task3_scraping.py
Run with: python task3_scraping.py
"""

from bs4 import BeautifulSoup
import requests
import sys
from datetime import datetime

print("=" * 80)
print("TASK 3: WEATHER DATA SCRAPING WITH ERROR HANDLING")
print("=" * 80)

# ============================================================================
# SETUP
# ============================================================================
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": USER_AGENT}

# City to get weather for
city = "stockholm"

print(f"\nCity: {city.capitalize()}")
print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "-" * 80)

# List to store weather data from both websites
all_weather_data = []

# ============================================================================
# WEBSITE 1: WTTR.IN (Simple Weather Service)
# ============================================================================
print("\n[WEBSITE 1] Scraping from wttr.in...")
print("-" * 80)

url1 = f"https://wttr.in/{city}?format=j1"
source1 = "Wttr.in"

try:
    # STEP 1: Try to connect to website
    print(f"Connecting to: {url1}")
    r1 = requests.get(url1, headers=headers, timeout=10)
    
    # STEP 2: Check status code
    print(f"Status code: {r1.status_code}")
    
    if r1.status_code == 200:
        # STEP 3: Parse JSON response
        data = r1.json()
        current = data.get("current_condition", [{}])[0]
        
        # STEP 4: Extract weather information
        temperature = f"{current.get('temp_C', 'N/A')}°C"
        description = current.get("weatherDesc", [{}])[0].get("value", "N/A")
        humidity = f"{current.get('humidity', 'N/A')}%"
        wind_speed = f"{current.get('windspeedKmph', 'N/A')} km/h"
        
        # STEP 5: Store data
        weather_data1 = {
            "source": source1,
            "url": url1,
            "status": "Success",
            "city": city.capitalize(),
            "temperature": temperature,
            "description": description,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        all_weather_data.append(weather_data1)
        print(f"✓ Success! Weather data retrieved")
        print(f"  Temperature: {temperature}")
        print(f"  Description: {description}")
        
    else:
        # Handle non-200 status codes
        print(f"✗ Failed! HTTP Status: {r1.status_code}")
        weather_data1 = {
            "source": source1,
            "url": url1,
            "status": f"Failed - HTTP {r1.status_code}",
            "city": city.capitalize(),
            "temperature": "N/A",
            "description": "N/A",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        all_weather_data.append(weather_data1)

# ERROR HANDLING: Timeout
except requests.exceptions.Timeout:
    print("✗ Error: Request timed out (took too long)")
    weather_data1 = {
        "source": source1,
        "url": url1,
        "status": "Failed - Timeout",
        "city": city.capitalize(),
        "temperature": "N/A",
        "description": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    all_weather_data.append(weather_data1)

# ERROR HANDLING: Connection Error
except requests.exceptions.ConnectionError:
    print("✗ Error: Connection failed (check internet)")
    weather_data1 = {
        "source": source1,
        "url": url1,
        "status": "Failed - Connection Error",
        "city": city.capitalize(),
        "temperature": "N/A",
        "description": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    all_weather_data.append(weather_data1)

# ERROR HANDLING: Any other error
except Exception as e:
    print(f"✗ Error: {str(e)}")
    weather_data1 = {
        "source": source1,
        "url": url1,
        "status": f"Failed - {str(e)}",
        "city": city.capitalize(),
        "temperature": "N/A",
        "description": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    all_weather_data.append(weather_data1)

# ============================================================================
# WEBSITE 2: TIMEANDDATE.COM (Weather Website)
# ============================================================================
print("\n[WEBSITE 2] Scraping from timeanddate.com...")
print("-" * 80)

url2 = f"https://www.timeanddate.com/weather/sweden/{city}"
source2 = "TimeAndDate.com"

try:
    # STEP 1: Try to connect to website
    print(f"Connecting to: {url2}")
    r2 = requests.get(url2, headers=headers, timeout=10)
    
    # STEP 2: Check status code
    print(f"Status code: {r2.status_code}")
    
    if r2.status_code == 200:
        # STEP 3: Parse HTML
        soup = BeautifulSoup(r2.content, "html.parser")
        
        # STEP 4: Extract temperature
        temp_div = soup.find("div", class_="h2")
        temperature = temp_div.text.strip() if temp_div else "N/A"
        
        # STEP 5: Extract weather description
        # Try to find weather description in paragraphs or spans
        desc_elem = soup.find("p")
        description = desc_elem.text.strip() if desc_elem else "N/A"
        
        # Additional info might be in tables
        humidity = "N/A"
        wind_speed = "N/A"
        
        # Try to find table with weather details
        table = soup.find("table")
        if table:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    label = cells[0].text.strip().lower()
                    value = cells[1].text.strip()
                    if "humidity" in label:
                        humidity = value
                    elif "wind" in label:
                        wind_speed = value
        
        # STEP 6: Store data
        weather_data2 = {
            "source": source2,
            "url": url2,
            "status": "Success",
            "city": city.capitalize(),
            "temperature": temperature,
            "description": description,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        all_weather_data.append(weather_data2)
        print(f"✓ Success! Weather data retrieved")
        print(f"  Temperature: {temperature}")
        print(f"  Description: {description}")
        
    else:
        # Handle non-200 status codes
        print(f"✗ Failed! HTTP Status: {r2.status_code}")
        weather_data2 = {
            "source": source2,
            "url": url2,
            "status": f"Failed - HTTP {r2.status_code}",
            "city": city.capitalize(),
            "temperature": "N/A",
            "description": "N/A",
            "humidity": "N/A",
            "wind_speed": "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        all_weather_data.append(weather_data2)

# ERROR HANDLING: Timeout
except requests.exceptions.Timeout:
    print("✗ Error: Request timed out (took too long)")
    weather_data2 = {
        "source": source2,
        "url": url2,
        "status": "Failed - Timeout",
        "city": city.capitalize(),
        "temperature": "N/A",
        "description": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    all_weather_data.append(weather_data2)

# ERROR HANDLING: Connection Error
except requests.exceptions.ConnectionError:
    print("✗ Error: Connection failed (check internet)")
    weather_data2 = {
        "source": source2,
        "url": url2,
        "status": "Failed - Connection Error",
        "city": city.capitalize(),
        "temperature": "N/A",
        "description": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    all_weather_data.append(weather_data2)

# ERROR HANDLING: Any other error
except Exception as e:
    print(f"✗ Error: {str(e)}")
    weather_data2 = {
        "source": source2,
        "url": url2,
        "status": f"Failed - {str(e)}",
        "city": city.capitalize(),
        "temperature": "N/A",
        "description": "N/A",
        "humidity": "N/A",
        "wind_speed": "N/A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    all_weather_data.append(weather_data2)

# ============================================================================
# SAVE TO TEXT FILE
# ============================================================================
print("\n" + "=" * 80)
print("SAVING RESULTS TO FILE")
print("=" * 80)

output_file = "task3_weather.txt"

try:
    with open(output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write("TASK 3: WEATHER DATA SCRAPING\n")
        f.write(f"City: {city.capitalize()}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        # Write data from each website
        for i, weather in enumerate(all_weather_data, 1):
            f.write(f"WEBSITE {i}: {weather['source']}\n")
            f.write("-" * 80 + "\n")
            f.write(f"URL: {weather['url']}\n")
            f.write(f"Status: {weather['status']}\n")
            f.write(f"City: {weather['city']}\n")
            f.write(f"Temperature: {weather['temperature']}\n")
            f.write(f"Description: {weather['description']}\n")
            f.write(f"Humidity: {weather['humidity']}\n")
            f.write(f"Wind Speed: {weather['wind_speed']}\n")
            f.write(f"Timestamp: {weather['timestamp']}\n")
            f.write("=" * 80 + "\n\n")
    
    print(f"✓ Successfully saved to: {output_file}")
    
except Exception as e:
    print(f"✗ Error saving file: {e}")

# ============================================================================
# DISPLAY SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

for i, weather in enumerate(all_weather_data, 1):
    print(f"\nWebsite {i}: {weather['source']}")
    print(f"  Status: {weather['status']}")
    if "Success" in weather['status']:
        print(f"  Temperature: {weather['temperature']}")
        print(f"  Description: {weather['description']}")

print("\n" + "=" * 80)
print("TASK 3 COMPLETED!")
print("=" * 80)
print(f"\nOutput file: {output_file}")
print("To view: Open 'task3_weather.txt' in any text editor")
print("=" * 80)