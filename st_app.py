#ECO5012 st_app.py
#100476251
#May 02, 2026

# Install all libraries required by the ECO5012B_App
! pip install -q streamlit yfinance pandas numpy matplotlib
! pip install -q textblob requests beautifulsoup4

# Download the Cloudflare Tunnel binary for Linux ( amd64 )
!wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared # Make it executable
!./cloudflared --version # Verify installation

from google.colab import files
import os
# Create the pages/ sub-folder (equivalent to mkdir)
os.makedirs("pages", exist_ok=True)
# Trigger a file-picker dialog -- select Home.py from your
uploaded = files.upload()
# Confirm Home.py landed in the right place
print("Files uploaded to root:", os.listdir("."))

from google.colab import files
import os, shutil
# Upload the four page files (multi-select is supported)
uploaded = files.upload()
# Move every uploaded file into the pages/ folder
for filename in uploaded.keys():
    dest = os.path.join("pages", filename)
    shutil.move(filename, dest)
    print(f"Moved {filename} --> pages/{filename}")
# Verify the final folder structure
print("\nRoot folder:", os.listdir("."))
print("pages/ folder:", os.listdir("pages"))

# Shell command to print the full folder tree
# Should mirror the ECO5012B_App structure exactly
! echo " === Root === " && ls -1
! echo " === pages / === " && ls -1 pages /

import pandas as pd
import os

# Check if the file exists
file_path = 'merged_gdp_sentiment_data.csv'
if not os.path.exists(file_path):
    print(f"Error: The file '{file_path}' does not exist in the current directory.")
else:
    try:
        df_check = pd.read_csv(file_path)
        print(f"Columns in '{file_path}':")
        print(df_check.columns.tolist())
        print("\nFirst 5 rows of the DataFrame:")
        display(df_check.head())
    except Exception as e:
        print(f"Error reading '{file_path}': {e}")

import pandas as pd
import os

file_path = 'merged_gdp_sentiment_data.csv'

if os.path.exists(file_path):
    try:
        # Correctly read with comma delimiter, setting the second row (header=1) as columns and DATE as index
        df_corrected = pd.read_csv(file_path, sep=',', header=1, index_col=0)
        print("Successfully re-read CSV with corrected parameters.")
        print("Columns after correction:")
        print(df_corrected.columns.tolist())
        print("\nFirst 5 rows of the corrected DataFrame:")
        display(df_corrected.head())

        # Now, modify the Streamlit app file if the corrected DataFrame looks good
        # This part will be done in the next step based on user confirmation.
    except Exception as e:
        print(f"Error re-reading '{file_path}' with corrected parameters: {e}")
else:
    print(f"Error: The file '{file_path}' does not exist.")

import os
import time

# Start Streamlit in the background
os.system(
    "streamlit run Home.py --server.port 8501 --server.headless true &"
)
# Brief pause to let Streamlit initialise before the tunnel connects
time.sleep(3)
print("Streamlit server started on port 8501")

import subprocess
import time
import re

# Launch cloudflared tunnel and capture its output
tunnel = subprocess.Popen(
    ["./cloudflared", "tunnel", "--url", "http://localhost:8501"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True
)

# Read output line-by-line until we find the public URL
print("Starting new tunnel -- please wait...")
for line in tunnel.stdout:
    match = re.search(r"https://[a-z0-9\-]+\.trycloudflare\.com", line)
    if match:
        url = match.group(0)
        print("\n" + "=" *60)
        print(f"Your Streamlit app is live at:")
        print(f" {url}")
        print("=" *60)
        break
