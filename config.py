import dotenv

# Load environment variables immediately
def init_env():
    dotenv.load_dotenv(".env")

# Call init_env at import time to ensure environment variables are loaded
init_env()

            
# Configuration for default debug values (only applied when debug decorators are used)
class DEBUG:
    class Node:
        enter = True
        exit = True
        error = True
