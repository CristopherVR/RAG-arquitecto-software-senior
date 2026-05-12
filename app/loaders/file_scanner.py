import os

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".cs",
    ".java",
    ".md",
    ".yaml",
    ".yml",
    ".json",
]

class FileScanner:

    @staticmethod
    def scan_repository(repo_path):

        files = []

        for root, dirs, filenames in os.walk(repo_path):

            dirs[:] = [
                d for d in dirs
                if d not in [".git", "node_modules", "bin", "obj", "__pycache__"]
            ]

            for file in filenames:

                ext = os.path.splitext(file)[1]

                if ext in SUPPORTED_EXTENSIONS:

                    full_path = os.path.join(root, file)

                    files.append(full_path)

        return files