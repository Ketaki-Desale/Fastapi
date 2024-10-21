import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql://postgres.foqyncaqywjeijrsnket:ketakidesale@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
JWT_SECRET = "https://jwt.io/#debugger-io?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
