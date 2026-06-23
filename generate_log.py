from datetime import datetime
import os

def generate_log(data):
    # STEP 1: Validate input
    if not isinstance(data, list):
        raise ValueError("log_data must be a list of strings")
    
    for item in data:
        if not isinstance(item, str):
            raise ValueError("All elements in log_data must be strings")

    # STEP 2: Generate a filename with today's date
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"log_{date_str}.txt"

    # STEP 3: Write the log entries to a file using File I/O
    with open(filename, "w") as file:
        for entry in data:
            file.write(f"{entry}\n")

    # STEP 4: Print a confirmation message with the filename
    print(f"Log written to {filename}")
    
    return filename


def fetch_api_data():
    try:
        import requests
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        if response.status_code == 200:
            return response.json()
        return {}
    except ImportError:
        print("Warning: requests library not installed. Install with: pip install requests")
        return {}


if __name__ == "__main__":
    log_entries = [
        "User logged in",
        "User updated profile", 
        "Report exported",
        "Session ended"
    ]
    
    filename = generate_log(log_entries)
    
    post = fetch_api_data()
    if post:
        print(f"Fetched Post Title: {post.get('title', 'No title found')}")
        print(f"Fetched Post Body: {post.get('body', 'No body found')[:50]}...")
    
    print(f"Script completed successfully. Log file: {filename}")