import requests
import json
import zipfile
import shutil

from robot.api import logger
from robot.api.deco import library, keyword, not_keyword


@library(scope="SUITE", version="1.0", auto_keywords=False)
class ChromeDriver:
    ENDPOINT = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
    PLATFORM = "win64"
    EXTRACT_FULL_PATH = "./cdriver.exe"

    @not_keyword
    def log_set(self, lvl: str, msg: str) -> None:
        print(f"{lvl} : {msg}")
        if lvl.upper() == "INFO":
            logger.info(msg)
        elif lvl.upper() == "WARN":
            logger.warn(msg)

    @keyword()
    def update_chromedriver(self):
        for i in json.loads(requests.get(self.ENDPOINT).text)["channels"]["Stable"]["downloads"]["chromedriver"]:
            if i["platform"] == self.PLATFORM:
                response = requests.get(url=i["url"], stream=True)
                with open("chromedriver.zip", mode="wb") as file:
                    file.write(response.content)
                with zipfile.ZipFile("chromedriver.zip", mode="r") as archive:
                    archive.printdir()
                    archive.open("chromedriver-win64/chromedriver.exe")
                    archive.extractall(".")
                shutil.move("./chromedriver-win64/chromedriver.exe", self.EXTRACT_FULL_PATH)
        self.log_set("info", "ChromeDriver updated.")


if __name__ == "__main__":
    C = ChromeDriver()
    C.update_chromedriver()
