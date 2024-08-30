import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Ensure these environment variables are set in your environment
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_ANON_KEY")

# Check if the environment variables are set
if not supabase_url or not supabase_key:
    raise ValueError("Supabase URL or Key is not set. Please check your environment variables.")

print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key}")
supabase: Client = create_client(supabase_url, supabase_key)

def fetch_data():
    # Example function to fetch data from a table
    table_name = 'actual_table_name'  # Replace with your actual table name
    print(f"Fetching data from table: {table_name}")
    response = supabase.table(table_name).select('*').execute()
    if response.error:
        print("Error fetching data:", response.error)
    else:
        print("Data:", response.data)

if __name__ == "__main__":
    print("Connected to Supabase")
    fetch_data()
