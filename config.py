from dotenv import load_dotenv
import os

load_dotenv()

BLOG_DB_URL=os.environ.get("BLOG_DB_URL")