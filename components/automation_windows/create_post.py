from os import getenv
from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from components.os_handle import OsHandler
import pyperclip


class BrowserController():
    def __init__(
        self,
        message_version,
        forum_username,
        forum_passwd,
        bitrix_username,
        bitrix_passwd,
        name_of_program,
        test_mode=False,
        final_version=False,
        topic_name_of_final_version=None,
        test_forum=False,
        test_bitrix=False,
    ):
        self.os_handler = OsHandler()
        self.path_user = getenv('APPDATA')

        try:
            self.navegador = self.browser()
            self.wait = WebDriverWait(self.navegador, 10)
            self.message_version = message_version
            self.forum_username = forum_username
            self.forum_passwd = forum_passwd
            self.bitrix_username = bitrix_username
            self.bitrix_passwd = bitrix_passwd
            self.test_mode = test_mode
            self.final_version = final_version
            self.topic_name_of_final_version = topic_name_of_final_version
            self.name_of_program = name_of_program

            if test_mode:
                print(test_mode)
                if test_forum:
                    self.forum_post()
                elif test_bitrix:
                    self.create_posts_on_bitrix()
            else:
                self.forum_post()
                sleep(6)
                self.create_posts_on_bitrix()

        except SessionNotCreatedException as err:
            mgs = f"Erro: {err}"
            print(mgs)
            return 'Error', mgs

        finally:
            if hasattr(self, "navegador"):
                self.navegador.quit()

    # -------------------------------------------------------------------
    # BROWSERS
    # -------------------------------------------------------------------
    def browser(self):
        self.default_browser_name = self.os_handler.get_name_of_default_browser()

        if self.default_browser_name == 'brave':
            service = ChromeService(
                executable_path=ChromeDriverManager(
                    chrome_type=ChromeType.BRAVE,
                    driver_version=self.os_handler.get_version_of_browser(self.default_browser_name)
                ).install()
            )
            driver = webdriver.Chrome(service=service, options=self.set_chrome_options())

        elif self.default_browser_name == 'chrome':
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.set_chrome_options())

        elif self.default_browser_name == 'firefox':
            service = FirefoxService()
            driver = webdriver.Firefox(service=service, options=self.set_firefox_options())

        else:
            raise Exception(f"Navegador {self.default_browser_name} não suportado ainda.")

        return driver

    def set_chrome_options(self):
        options = ChromeOptions()
        options = self.set_options(options)
        return options

    def set_firefox_options(self):
        options = FirefoxOptions()
        options = self.set_options(options)
        return options

    def set_options(self, options):
        options.add_argument("--log-level=3")  # Silencia mensagens de erro do console Selenium
        if self.default_browser_name in ['brave', 'chrome']:
            options.binary_location = self.os_handler.get_default_browser_path()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument("--profile-directory=Default")
            options.add_argument(f'--user-data-dir={self.path_user}\\cache')
        return options

    # -------------------------------------------------------------------
    # FÓRUM
    # -------------------------------------------------------------------
    def forum_post(self):
        urls = {
            'Mycommerce': 'https://forum.visualsoftware.inf.br/forumdisplay.php?fid=30',
            'MyFrota': 'https://forum.visualsoftware.inf.br/forumdisplay.php?fid=85',
            'MyPet': 'https://forum.visualsoftware.inf.br/forumdisplay.php?fid=82',
        }
        self.open_browser(urls.get(self.name_of_program))

        if self.final_version:
            self.insert_new_topic_for_final_version()
        else:
            self.open_last_version_forum()
            self.add_new_response()

    def open_browser(self, url):
        self.navegador.get(url)
        sleep(2)
        self.login_forum()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[3]/a/span')))

    def open_last_version_forum(self):
        if self.name_of_program in ['MyPet', 'MyFrota']:
            click_last_post = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/table/tbody/tr[3]/td[3]/div/span/span/a'))
            )
        else:  # Mycommerce
            click_last_post = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/table[2]/tbody/tr[3]/td[3]/div/span/span/a'))
            )
        click_last_post.click()

    def add_new_response(self):
        path_body_message = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[6]/td[2]/div/iframe'
        insert_message_button = '/html/body/div/div[2]/div/form/div/input[1]'
        path = '/html/body/div[1]/div[2]/div/div[3]/a'

        if self.final_version:
            path_body_message = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[5]/td[2]/div/iframe'
            path_topic_name_label = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[3]/td[2]/input'
            self.click_base(path_topic_name_label).send_keys(self.topic_name_of_final_version)
        else:
            self.click_base(path)

        # Inserir mensagem dentro do iframe
        iframe = self.wait.until(EC.presence_of_element_located((By.XPATH, path_body_message)))
        self.navegador.switch_to.frame(iframe)

        pyperclip.copy(self.message_version)
        body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body.click()
        ActionChains(self.navegador).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

        self.navegador.switch_to.default_content()

        if not self.test_mode:
            self.click_base(insert_message_button)
        else:
            print('modo de teste')
            sleep(5)

    def insert_new_topic_for_final_version(self):
        click_new_topic_path = '/html/body/div/div[2]/div/div[3]/a/span'
        self.click_base(click_new_topic_path)
        self.add_new_response()

    def login_forum(self):
        try:
            logged = self.navegador.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/a")
            is_logged = logged.is_displayed()
        except:
            is_logged = False

        if not is_logged:
            path_label_username = '/html/body/div/div[2]/div/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input'
            path_label_passwd = '/html/body/div/div[2]/div/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/input'
            button_login_path = '/html/body/div/div[2]/div/table/tbody/tr[2]/td/form/table/tbody/tr[4]/td/input'
            self.send_keys_base(path_label_username, self.forum_username)
            self.send_keys_base(path_label_passwd, self.forum_passwd)
            self.click_base(button_login_path)

    # -------------------------------------------------------------------
    # BITRIX
    # -------------------------------------------------------------------
    def create_posts_on_bitrix(self):
        link_bitrix = 'https://visualsoftware.bitrix24.com.br/stream/'
        self.open_bitrix(link_bitrix)
        self.bitrix_post1()
        self.bitrix_post_2()

    def open_bitrix(self, link_bitrix):
        self.navegador.get(link_bitrix)
        sleep(2)
        self.login_bitrix()

    def login_bitrix(self):
        try:
            logged = self.navegador.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/div[1]/div[2]/div[1]/ul")
            is_logged = logged.is_displayed()
        except:
            is_logged = False

        if not is_logged:
            path_email = '//*[@id="login"]'
            path_passwd = '/html/body/div[1]/div[3]/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/div/label'
            path_next_login = '/html/body/div[1]/div[3]/div/div/div/div/div/div/div[2]/div[1]/div/div/button/span'
            path_next_login2 = '/html/body/div[1]/div[3]/div/div/div/div/div/div/div[2]/div[1]/div/div/button'
            self.send_keys_base(path_email, self.bitrix_username)
            sleep(2)
            self.click_base(path_next_login)
            sleep(2)
            self.send_keys_base(path_passwd, self.bitrix_passwd)
            self.click_base(path_next_login2)

    def bitrix_post1(self):
        path_post_body = '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td/div/div[2]/div/div[1]/div/div/div[2]/div'
        self.click_base(path_post_body)

        actions = ActionChains(self.navegador)
        actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

        if not self.test_mode:
            actions.key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
            sleep(2)
        else:
            print('modo de teste')
            sleep(5)

    def bitrix_post_2(self):
        self.navegador.get('https://visualsoftware.bitrix24.com.br/online/')
        sleep(6)
        text_find_chat = 'canais - avisos'

        elements = self.navegador.find_elements(By.XPATH, '//input[@type="text"]')
        if elements:
            chat_input = elements[0]
            chat_input.click()
            chat_input.send_keys(text_find_chat)
            chat_input.send_keys(Keys.ENTER)

            actions = ActionChains(self.navegador)
            pyperclip.copy(self.message_version)
            actions.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

            if not self.test_mode:
                actions.send_keys(Keys.ENTER).perform()
                sleep(5)
            else:
                print('modo de teste')
                sleep(10)

    # -------------------------------------------------------------------
    # HELPERS
    # -------------------------------------------------------------------
    def click_base(self, path, xpath=True):
        if xpath:
            click = self.wait.until(EC.presence_of_element_located((By.XPATH, path)))
        else:
            click = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, path)))
        click.click()
        return click

    def send_keys_base(self, path, keys):
        send_keys = self.wait.until(EC.presence_of_element_located((By.XPATH, path)))
        send_keys.send_keys(keys)
        return send_keys


if __name__ == '__main__':
    from os import getenv
    #pega os dados do arquivo test_post.ini
    from configparser import ConfigParser
    config = ConfigParser()
    config.read('components/automation_windows/test_post.ini')
    bitrix_username = config.get('DEFAULT', 'BITRIX_USERNAME')
    bitrix_senha = config.get('DEFAULT', 'BITRIX_PASSWORD')
    forum_username = config.get('DEFAULT', 'FORUM_USERNAME')
    forum_passwd = config.get('DEFAULT', 'FORUM_PASSWORD')
    
    
    navegador = BrowserController(
        message_version="Nova versão disponível para testes 🚀",
        bitrix_username=bitrix_username,
        bitrix_passwd=bitrix_senha,
        forum_username=forum_username,
        forum_passwd=forum_passwd,
        test_mode=True,
        test_bitrix=True,
        name_of_program='Mycommerce'
    )
