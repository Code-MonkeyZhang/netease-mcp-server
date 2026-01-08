import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import login_via_qrcode

if __name__ == "__main__":
    print("Starting login process...")
    result = login_via_qrcode()
    print(result)
