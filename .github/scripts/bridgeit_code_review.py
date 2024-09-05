import requests
import os
import sys
from github import Github

# Set up your custom API details
API_URL = os.getenv("BRIDGEIT_URL")
API_KEY = os.getenv("BRIDGEIT_API_ACCESS_TOKEN")
APP_KEY = os.getenv("BRIDGEIT_APP_KEY")

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def load_prompt_template(template_path):
    """Load the prompt template from a file."""
    try:
        with open(template_path, "r") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading prompt template {template_path}: {e}")
        return None

def review_code(file_path, code_content, prompt_template):
    """Use Cisco BridgeIT API to review code."""
    try:
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-key': API_KEY
        }
        prompt_content = prompt_template.format(code_content=code_content)

        data = {
            "messages": [
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": prompt_content}
            ],
            "user": "{\"appkey\": \"" + APP_KEY + "\"}",
            "stop": ["<|im_end|>"]
        }
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error reviewing code for {file_path}: {e}")
        return None

def post_review_comment(repo_name, pr_number, review, token):
    """Post review comments to a GitHub pull request."""
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        pull_request = repo.get_pull(pr_number)
        pull_request.create_issue_comment(review)
    except Exception as e:
        print(f"Error posting review comment: {e}")

def main(file_path, repo_name, pr_number, token, prompt_template_path):
    print(f"Reviewing {file_path}...")
    code_content = read_file(file_path)
    if code_content:
        prompt_template = load_prompt_template(prompt_template_path)
        if prompt_template:
            review = review_code(file_path, code_content, prompt_template)
            if review:
                print(f"Review for {file_path}:\n{review}\n")
                post_review_comment(repo_name, pr_number, review, token)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bridgeit_code_review.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("PR_NUMBER"))
    token = os.getenv("G_AUTO_TOKEN")
    prompt_template_path = ".github/scripts/prompt_csharp_template.txt"  # Path to the prompt template file

    main(file_path, repo_name, pr_number, token, prompt_template_path)
