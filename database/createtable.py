# postgres functions are called as RPC to supabase

from supabase import Client, create_client
import dotenv
import os

dotenv.load_dotenv()

def create_table(tablename):
    """Create the Process_Pipe table in the database."""
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    supabase.rpc(tablename).execute()