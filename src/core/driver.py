from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.file_detector import LocalFileDetector

from src.utils.path import Files


class DriverBrowser:
    def __init__(self,
                 browser_name: str,
                 browser_headless: bool,
                 remote_browser: bool,
                 executor: str,
                 mk_video: bool,
                 ):
        """
        browser_name - браузер, для локального запуска (g-google, f-firefox)
        browser_headless - запуск браузера без окна
        remote_browser - инициализация браузера в контейнере через  selenoid
        executor - адрес, где находится исполнитель по запуска браузера( через контейнеры selenoid)
        mk_video - запись тестов( не актуально)
        """
        self.browser_name = browser_name
        self.browser_headless = browser_headless
        self.remote_browser = remote_browser
        self.executor = executor
        self.mk_video = mk_video

    def setup_driver(self) -> any:
        if self.remote_browser:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--enable-automation")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--incognito")
            prefs = {"download.default_directory": '/home/selenium/Downloads',
                     "profile.default_content_settings.popups": 0,
                     "profile.default_content_setting_values.automatic_downloads": 1
                     }
            options.add_experimental_option("prefs", prefs)
            caps = {"browserName": "chrome",
                    "browserVersion": "100.0",
                    "selenoid:options":
                        {
                            "enableVNC": False,
                            "enableVideo": True if self.mk_video else False,
                            "privileged": True},
                    'goog:loggingPrefs':
                        {'performance': 'ALL',
                         'driver': 'ALL',
                         'browser': 'ALL'}}

            if not self.executor:
                self.executor = "http://selenoid:4444/wd/hub"

            driver = webdriver.Remote(
                command_executor=self.executor,
                options=options,
                desired_capabilities=caps
            )

            driver.file_detector = LocalFileDetector()

            driver.command_executor.set_timeout(30)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)
            return driver

        if self.browser_name == 'g':
            options = webdriver.ChromeOptions()

            if self.browser_headless:
                options.add_argument("--headless")

            prefs = {"download.default_directory": Files.DOWNLOAD_FILES_PATH}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("--disable-notifications")
            options.add_argument("--enable-automation")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-extensions")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--incognito")

            caps = DesiredCapabilities.CHROME
            caps['goog:loggingPrefs'] = {'performance': 'ALL',
                                         'browser': 'ALL',
                                         'driver': 'ALL', }
            caps.update({"applicationCacheEnabled": False})
            driver = webdriver.Chrome(ChromeDriverManager().install(),
                                      chrome_options=options,
                                      desired_capabilities=caps)
            driver.delete_all_cookies()
            driver.command_executor.set_timeout(30)
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)
            return driver