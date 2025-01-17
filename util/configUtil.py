import json
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO)  # 设置日志级别


class CookieManager:
    def __init__(self, config_file_path):
        self.config = {}
        self.config_file_path = config_file_path

    def _login_and_save_cookies(self, login_url="https://show.bilibili.com/platform/home.html"):
        logging.info("启动浏览器中.....")
        self.driver = webdriver.Edge()
        self.wait = WebDriverWait(self.driver, 0.5)
        self.driver.get(login_url)
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.find_element(By.CLASS_NAME, "nav-header-register").click()
        logging.info("浏览器启动, 进行登录.")
        while True:
            try:
                self.driver.find_element(By.CLASS_NAME, "nav-header-register")
            except Exception as _:
                break
        time.sleep(1)
        self.config["bilibili_cookies"] = self.driver.get_cookies()
        with open(self.config_file_path, 'w') as f:
            json.dump(self.config, f, indent=4)
        self.driver.quit()
        logging.info("登录成功, 浏览器退出.")
        return self.config["bilibili_cookies"]

    def get_cookies(self):
        try:
            with open(self.config_file_path, 'r') as f:
                self.config = json.load(f)
        except Exception as e:
            return self._login_and_save_cookies()

        if self.config == {}:
            return self._login_and_save_cookies()
        else:
            cookies = self.config["bilibili_cookies"]
            return cookies

    def get_cookies_str(self):
        cookies = self.get_cookies()
        cookies_str = ""
        for cookie in cookies:
            cookies_str += cookie["name"] + "=" + cookie["value"] + "; "
        return cookies_str

    def get_cookies_str_force(self):
        cookies = self._login_and_save_cookies()
        cookies_str = ""
        for cookie in cookies:
            cookies_str += cookie["name"] + "=" + cookie["value"] + "; "
        return cookies_str


if __name__ == "__main__":
    cookie_manager = CookieManager("../config/cookies.json")
    logging.info(str(cookie_manager.get_cookies_str()))
