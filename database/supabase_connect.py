# This is the boilerplate for database connections and configuration for the application

import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)


if __name__ == "__main__":
    # Simple test to verify connection
    response = supabase.table("10_Process_Pipe").select("*").execute()
    print(response.data)