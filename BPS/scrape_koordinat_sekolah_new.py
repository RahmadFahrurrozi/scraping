import pandas as pd
import time
import re
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- FILE CONFIG ---
input_file = "database_sekolah_banyuwangi_lengkap_new.xlsx" 
output_file = "hasil_koordinat_sekolah_banyuwangi_new.xlsx"

def extract_coords(url):
    match = re.search(r'@([-?\d\.]+),([-?\d\.]+)', url)
    if match:
        return f"'{match.group(1)}", f"'{match.group(2)}"
    return "Cek Manual", "Cek Manual"

# --- SETUP CHROME ---
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

if not os.path.exists(input_file):
    print(f"File {input_file} tidak ditemukan!")
    sys.exit()

df = pd.read_excel(input_file)

# Tambahkan kolom baru jika belum ada
new_cols = ["Latitude", "Longitude"]
for col in new_cols:
    if col not in df.columns:
        df[col] = "Belum Diambil"

print(f"=== Scraping {len(df)} Sekolah ===")

try:
    for index, row in df.iterrows():
        if df.at[index, "Latitude"] != "Belum Diambil":
            continue

        nama_sekolah = str(row["Nama Sekolah"]).strip()
        alamat = str(row["Alamat"]).strip() if pd.notna(row["Alamat"]) else ""
        
        search_query = f"{nama_sekolah} {alamat} Banyuwangi"
        url_search = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        
        print(f"[{index+1}/{len(df)}] Mencari: {nama_sekolah}")
        driver.get(url_search)
        
        try:
            WebDriverWait(driver, 10).until(lambda d: "@" in d.current_url)
            time.sleep(2) 
            
            lat, lon = extract_coords(driver.current_url)
            df.at[index, "Latitude"] = lat
            df.at[index, "Longitude"] = lon

            print(f"Data Berhasil diambil: {nama_sekolah} | {lat}, {lon} | ")

        except Exception as e:
            print(f"Gagal mengambil detail: {nama_sekolah} | Error: {e}")
            df.at[index, "Latitude"] = "Cek Manual"

        if (index + 1) % 5 == 0:
            df.to_excel(output_file, index=False)
            print("Progress disimpan...")

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    df.to_excel(output_file, index=False)
    driver.quit()
    print(f"\nSelesai! Hasil: {output_file}")