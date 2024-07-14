import os
import shutil
import subprocess
import tempfile

from aws_lambda_powertools import Logger

from crawlers.base import BaseCrawler
from db.documents import RepositoryDocument

logger = Logger(service="llm-twin-course/crawler")


class GithubCrawler(BaseCrawler):
    model = RepositoryDocument

    def __init__(self, ignore=(".git", ".toml", ".lock", ".png")) -> None:
        super().__init__()
        self._ignore = ignore

    def extract(self, link: str, **kwargs) -> None:
        logger.info(f"Starting scrapping GitHub repository: {link}")

        # 從連結中獲取repo name
        repo_name = link.rstrip("/").split("/")[-1]

        # 建立一個臨時目錄
        local_temp = tempfile.mkdtemp()

        try:
            # 切換到臨時目錄
            os.chdir(local_temp)

            # 使用 git clone 複製repo
            subprocess.run(["git", "clone", link])

            # 獲取複製下來的repo路徑
            repo_path = os.path.join(local_temp, os.listdir(local_temp)[0])

            # 遍歷repo的所有檔案和目錄
            tree = {}
            for root, dirs, files in os.walk(repo_path):
                dir = root.replace(repo_path, "").lstrip("/")
                if dir.startswith(self._ignore):
                    continue
                
                # 遍歷目錄中的所有檔案
                for file in files:
                    if file.endswith(self._ignore):
                        continue

                    file_path = os.path.join(dir, file)

                    # 開啟檔案並讀取其內容
                    with open(os.path.join(root, file), "r", errors="ignore") as f:
                        # 將檔案的內容加入到樹狀結構中
                        tree[file_path] = f.read().replace(" ", "")

            instance = self.model(
                name=repo_name, link=link, content=tree, owner_id=kwargs.get("user")
            )
            instance.save()

        except Exception:
            raise
        finally:
            # 無論是否發生異常，都刪除臨時目錄
            shutil.rmtree(local_temp)

        logger.info(f"Finished scrapping GitHub repository: {link}")