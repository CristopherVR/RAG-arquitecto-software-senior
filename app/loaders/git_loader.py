from git import Repo
import os
import shutil


class GitLoader:

    @staticmethod
    def clone_repository(repo_url: str, local_path: str):

        try:

            # Si ya existe, eliminarlo para volver a clonar
            if os.path.exists(local_path):

                print("🗑 Eliminando repositorio anterior...")
                shutil.rmtree(local_path)

            print("⬇ Clonando repositorio desde GitHub...")

            Repo.clone_from(repo_url, local_path)

            print("✅ Repositorio clonado correctamente")

            return local_path

        except Exception as e:

            print("❌ Error clonando repositorio")

            print(e)

            return None