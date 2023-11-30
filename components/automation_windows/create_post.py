from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import os

class BrowserController():
    def __init__(self, message_version, forum_username, forum_passwd, bitrix_username, bitrix_passwd):
        self.path_user = os.getenv('APPDATA')
        self.navegador = self.browser()
        self.wait = WebDriverWait(self.navegador, 10)
        self.message_version = message_version
        self.forum_username = forum_username
        self.forum_passwd = forum_passwd
        self.bitrix_username = bitrix_username
        self.bitrix_passwd = bitrix_passwd

        self.forum_post()
        sleep(5)
        self.create_posts_on_bitrix()
      
    def browser(self):
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.set_chrome_options())
        return driver
    
    def forum_post(self):
        self.open_browser('https://forum.visualsoftware.inf.br/forumdisplay.php?fid=30')
        self.open_last_version_forum()
        self.add_new_response()
        
    def set_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3") # Silences error messages from Selenium console
        options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        # options.add_experimental_option("detach", True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--profile-directory=Default")
        options.add_argument(f'--user-data-dir={self.path_user}\cache')
        
        return options
    
    def open_browser(self, url):
        self.navegador.get(url)
        sleep(2)
        self.login_forum()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[3]/a/span')))

    def open_last_version_forum(self):
        click_last_post = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/table[2]/tbody/tr[3]/td[3]/div/span/span/a')))
        click_last_post.click()
            
    def add_new_response(self):
        path = '/html/body/div[1]/div[2]/div/div[3]/a' 
        path_body_message = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[6]/td[2]/div/iframe'
        insert_message_button = '/html/body/div/div[2]/div/form/div/input[1]'
        self.click_base(path)
        self.click_base(path_body_message).send_keys(self.message_version)
        
        active_element = self.navegador.execute_script("""return document.querySelector("#content > div > form > table:nth-child(2) > tbody > tr:nth-child(6) > td:nth-child(2) > div > iframe")""")
        active_element.send_keys(Keys.CONTROL + "a")
        active_element.send_keys(Keys.CONTROL + "c")
        active_element.send_keys(Keys.CONTROL + "v")
        active_element.send_keys(Keys.CONTROL + "a")
        active_element.send_keys(Keys.CONTROL + "c")

        # clica no botão de inserir mensagem do post
        # self.click_base(insert_message_button)
    
    def click_base(self, path, xpath = True):
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
    
    def login_forum(self):
        logged = self.navegador.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/a")
        if not logged.is_displayed():
            path_label_username = '/html/body/div/div[2]/div/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[2]/input'
            path_label_passwd = '/html/body/div/div[2]/div/table/tbody/tr[2]/td/form/table/tbody/tr[3]/td[2]/input'
            button_login_path = '/html/body/div/div[2]/div/table/tbody/tr[2]/td/form/table/tbody/tr[4]/td/input'
            passwd = self.forum_passwd
            user = self.forum_username
            self.send_keys_base(path_label_username, user)
            self.send_keys_base(path_label_passwd, passwd)
            self.click_base(button_login_path)
    
    def create_posts_on_bitrix(self):
        link_bitrix = 'https://visualsoftware.bitrix24.com.br/stream/'
        self.open_bitrix(link_bitrix)
        # self.bitrix_post1()
        # self.bitrix_post_2()
        
    def open_bitrix(self, link_bitrix):
        self.navegador.get(link_bitrix)
        sleep(2)
        self.login_bitrix()
        
    def login_bitrix(self):
        # verifica se existe um elemento antes de proseguir
        logged = self.navegador.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td/div/div[2]/div/div[1]/div/div/div[2]/div")
        if not logged.is_displayed():
            path_email = '/html/body/div[1]/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[1]/div/input'
            path_passwd = '/html/body/div[1]/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[2]/div/div[1]/div/input'
            path_next_login = '/div/form/div/div[5]/button[1]'
            self.send_keys_base(path_email, self.bitrix_username)
            self.click_base(path_next_login)
            self.send_keys_base(path_passwd, self.bitrix_passwd)
            self.click_base(path_next_login)

    def bitrix_post1 (self):
        path_post_body = '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td/div/div[2]/div/div[1]/div/div/div[2]/div'
        self.click_base(path_post_body)
        
        # envia para o navegador, lembrar de verificar onde esta o foco antes de mandar o comando
        actions = ActionChains(self.navegador)
        actions.send_keys('1')
        actions.perform()

        active_element = self.navegador.execute_script("return document.activeElement;")
        active_element.send_keys(Keys.CONTROL + "v")
        active_element.send_keys(Keys.ENTER)
    
    def bitrix_post_2(self):
        path_open_chat = r'/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/div[1]/div[2]/div[1]/ul/li[3]/ul/li[2]/a'
        path_chat_searcher = r'/html/body/div[20]/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input'
        path_chat_searcher2 = r'/html/body/div[42]/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input'
        path_chat_searcher3  = r'/html/body/div[26]/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input'
        
        path_chat = '/html/body/div[26]/div/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[3]/div/div[1]/div[2]/div[1]/textarea'
        
        self.click_base(path_open_chat)
        text_find_chat = 'canais - avisos'
        sleep(7)
        list_elements = [path_chat_searcher,path_chat_searcher2, path_chat_searcher3]

        for element in list_elements:
            try:
                element = self.navegador.find_element(By.XPATH, element)  
                element.click()
                element.send_keys(text_find_chat)
                element.send_keys(Keys.ENTER)
                # JA ABERTO O CHAT AGORA IRÁ ESCREVER A MENSAGEM
                chat = self.click_base(path_chat)
                chat.send_keys(Keys.CONTROL + "v")
                chat.send_keys(Keys.ENTER)
                break
            except:
                print('erro', element)

if __name__ == '__main__':
    navegador = BrowserController("""Olá! Versão [b]9.11.13.0000[/b] do [b]MyCommerce[/b] disponível para atualizações. 

[b]INCONSISTÊNCIAS ENCONTRADAS INTERNAMENTE[/b]
[b]143232[/b] - Ajustada inconsistência ao incluir produtos do tipo grade.

Compatível com a versão [b]1.32.13.2132[/b] do [b]MyCommerce PDV[/b]. 

Atenciosamente, Vitor Hugo Borges Dos Santos.""",

)

