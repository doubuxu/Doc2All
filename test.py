import os

import dotenv
dotenv.load_dotenv()
a=os.getenv("API_KEY")
print(a)