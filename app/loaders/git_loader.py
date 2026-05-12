from git import Repo
import os

class GitLoader:

    @staticmethod
    def clone_repository(repo_url: str, local_path: str):

        if os.path.exists(local_path):
            print("Repositorio ya existe")
            return local_path

        print("Clonando repositorio...")
        Repo.clone_from(repo_url, local_path)

        return local_path