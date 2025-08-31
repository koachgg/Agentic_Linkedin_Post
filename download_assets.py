import os
import requests

# --- Configuration ---
# Directory to save the downloaded files
VENDOR_DIR = "static/vendor"

# Dictionary of assets to download {filename: url}
ASSETS = {
    # CORRECTED: Save the Tailwind CDN script as a .js file
    "tailwind.js": "https://cdn.tailwindcss.com",
    "chart.min.js": "https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.min.js"
}
# --- End Configuration ---

def download_file(url, filepath):
    """Downloads a file from a URL to a specified path."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✅ Successfully downloaded {os.path.basename(filepath)}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")
        return False

def main():
    """Main function to download all specified assets."""
    print("--- Starting Asset Download ---")
    
    # Create the vendor directory if it doesn't exist
    if not os.path.exists(VENDOR_DIR):
        print(f"📂 Creating directory: {VENDOR_DIR}")
        os.makedirs(VENDOR_DIR)
    else:
        print(f"ℹ️ Directory already exists: {VENDOR_DIR}")

    # Download each asset
    success_count = 0
    for filename, url in ASSETS.items():
        filepath = os.path.join(VENDOR_DIR, filename)
        print(f"⬭️ Downloading {url} to {filepath}...")
        if download_file(url, filepath):
            success_count += 1

    print(f"--- Asset Download Complete: {success_count}/{len(ASSETS)} successful ---")
    
    # Return exit code based on success
    if success_count == len(ASSETS):
        print("🎉 All assets downloaded successfully!")
        return 0
    else:
        print("⚠️ Some assets failed to download")
        return 1

if __name__ == "__main__":
    exit(main())
