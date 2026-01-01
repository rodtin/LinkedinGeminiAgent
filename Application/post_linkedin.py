import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
URN_ID = os.getenv('LINKEDIN_URN_ID') # e.g., "urn:li:person:..." or "urn:li:organization:..."

def post_to_linkedin(file_path):
    if not ACCESS_TOKEN or not URN_ID:
        print("Error: LINKEDIN_ACCESS_TOKEN and LINKEDIN_URN_ID environment variables must be set.")
        print("Please configure your credentials in the 'Application/.env' file.")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Basic parsing: Assuming the file is pure markdown text for the body
        post_body = content

        url = "https://api.linkedin.com/v2/ugcPosts"
        
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        post_data = {
            "author": URN_ID,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": post_body
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code == 201:
            print(f"Success! Post created: {file_path}")
            print("Response:", response.json())
            
            # Rename the file to mark it as posted
            try:
                directory = os.path.dirname(file_path)
                filename = os.path.basename(file_path)
                new_filename = f"POSTED_{filename}"
                new_file_path = os.path.join(directory, new_filename)
                
                os.rename(file_path, new_file_path)
                print(f"File renamed to: {new_file_path}")
            except Exception as rename_error:
                print(f"Warning: Post successful, but failed to rename file: {rename_error}")

        else:
            print(f"Failed to post. Status Code: {response.status_code}")
            print("Response:", response.text)

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run post_linkedin.py <path_to_markdown_file>")
        sys.exit(1)
    
    file_to_post = sys.argv[1]
    post_to_linkedin(file_to_post)