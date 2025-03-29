import os  # Importing the os module to interact with the operating system
import requests  # Importing the requests module to make HTTP requests
from dotenv import load_dotenv  # Importing load_dotenv to load environment variables from a .env file

# Load environment variables from .env file
load_dotenv()

def fetch_repo_info(owner, repo_name):
    token = os.getenv('GITHUB_TOKEN')  # Get the API key from environment variables
    if not token:  # Check if the token is not set
        raise ValueError("GITHUB_TOKEN environment variable not set")  # Raise an error if the token is not set
    
    url = f"https://api.github.com/repos/{owner}/{repo_name}"  # URL for the GitHub API endpoint to get repository information
    headers = {
        'Authorization': f'token {token}',  # Authorization header with the token
    }

    response = requests.get(url, headers=headers)  # Make a GET request to the GitHub API

    if response.status_code == 200:  # Check if the request was successful
        return response.json()  # Return the JSON response
    else:
        print(f"Error: {response.status_code}")  # Print the error code if the request failed
        return None  # Return None if the request failed

def generate_markdown(repo):
    markdown_content = f"# {repo['name']}\n"  # Title of the repository
    markdown_content += f"\n## Description\n"  # Subtitle for the description
    markdown_content += f"{repo['description'] if repo['description'] else 'No description available!'}\n\n"  # Description of the repository
    markdown_content += f"## Repository URL\n"
    markdown_content += f"[{repo['html_url']}]({repo['html_url']})\n\n"  # URL of the repository
    markdown_content += f"## Languages\n"  # Subtitle for the languages used in the repository
    markdown_content += f"{', '.join(repo['language']) if repo['language'] else 'No languages available!'}\n\n"  # Languages used in the repository
    markdown_content += f"## Topics\n"  # Subtitle for the topics of the repository
    markdown_content += f"{', '.join(repo['topics']) if repo['topics'] else 'No topics available!'}\n\n"  # Topics of the repository
    
    with open('portfolio.md', 'a') as file:
        file.write(markdown_content)
    print(f"Markdown content for {repo['name']} generated and appended to portfolio.md")  # Print a message indicating that the markdown content has been generated  

if __name__ == "__main__":
    owner = "ajla-brdarevic"  # Owner of the repository
    repo_name = "GitHub-Portfolio-Generator"  # Name of the repository to fetch information from
    
    repo = fetch_repo_info(owner, repo_name)
    
    if repo:
        generate_markdown(repo)  # Call the function to generate markdown content for the repository
    else:
        print("Failed to fetch repository information")  # Print a message indicating that the repository information could not be fetched