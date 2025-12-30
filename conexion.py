from dotenv import load_dotenv
import os
from supabase import create_client

class ConexionDB:
    def __init__(self):
        load_dotenv()
        
    def conexionSupabase(self):
        url = os.getenv('SUPABASE_URL')
        api_key = os.getenv('SUPABASE_API_KEY')
        
        supabase = create_client(url, api_key)
        
        return supabase