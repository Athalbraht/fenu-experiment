# config.py

import os

if os.path.exists("user.py"):
    from user import *
    print("Using user.py config")
else:
    from default import *
    print("user.py file not found. Using default.py")
