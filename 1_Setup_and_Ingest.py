# Configuration
storage_account_name = "stresumeprojectdd"
container_name = "nyctaxi"

# ⚠️ SECURITY: Replace this with your actual key when running locally.
# NEVER commit the real key to GitHub!
access_key = "PASTE_YOUR_ACCESS_KEY_HERE"

# Clean the key just in case (removes invisible spaces)
access_key = access_key.strip()

# Set the Key for the session
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    access_key
)

print(f"🔍 Testing connection to: {storage_account_name}...")

# ATTEMPT 1: The Standard Blob Protocol (wasbs) - Validated for this project
try:
    print(f"\n1️⃣ Trying WASBS (Standard Blob)...")
    path_wasbs = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/"
    dbutils.fs.ls(path_wasbs)
    print("✅ SUCCESS! We will use 'wasbs' protocol.")
    final_path = path_wasbs
except Exception as e:
    print("❌ WASBS Failed.")

# ATTEMPT 2: The Data Lake Protocol (abfss)
try:
    print(f"\n2️⃣ Trying ABFSS (Data Lake Gen2)...")
    path_abfss = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/"
    dbutils.fs.ls(path_abfss)
    print("✅ SUCCESS! We will use 'abfss' protocol.")
    final_path = path_abfss
except Exception as e:
    print("❌ ABFSS Failed.")
