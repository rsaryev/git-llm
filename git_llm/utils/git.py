from git import Repo

ALLOW_FILES = ['.js', '.mjs', '.ts', '.tsx', '.css', '.scss', '.less', '.html', '.htm', '.json', '.py',
               '.java', '.c', '.cpp', '.cs', '.go', '.php', '.rb', '.rs', '.swift', '.kt', '.scala', '.m', '.h',
               '.sh', '.pl', '.pm', '.lua', '.sql', '.r', '.rmd', '.dart']


class Git:
    def __init__(self):
        self.repo = Repo(search_parent_directories=True)
        if not self.has_repository():
            raise Exception("🤖 No git repository found")

    def has_repository(self):
        return self.repo.bare is False

    def git_diff(self):
        allowed_extensions = [f"*{ext}" for ext in ALLOW_FILES]
        return self.repo.git.diff("--staged", "--diff-filter=ACMRT", "--", *allowed_extensions)

    def git_commit(self, message):
        return self.repo.git.commit("-m", message)


git = Git()
