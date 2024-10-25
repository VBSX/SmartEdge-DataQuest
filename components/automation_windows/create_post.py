from os import getenv
from os.path import abspath as path_os
from sys import path as syspath
path = path_os('./')
syspath.append(path)

from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.firefox import options as FirefoxOptions
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
        test_mode = False,
        final_version = False,
        topic_name_of_final_version =None,
        test_forum = False,
        test_bitrix = False,
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
                self.navegador.quit()
            else:
                self.forum_post()
                sleep(6)
                self.create_posts_on_bitrix()
                self.navegador.quit()
                
        except SessionNotCreatedException as err:
            mgs = f"Erro: {err}"
            print(mgs)
            return 'Error',mgs
      
    def browser(self):
        self.default_browser_name = self.os_handler.get_name_of_default_browser()
        if self.default_browser_name == 'brave':
            service = Service(executable_path=ChromeDriverManager(driver_version=self.os_handler.get_version_of_browser(self.default_browser_name)).install())
            driver = Chrome(service=service, options=self.set_chrome_options())
            
            # service = Service(executable_path=ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
            # driver = Chrome(service=service, options=self.set_chrome_options())
            
            
        if self.default_browser_name == 'chrome':
            service = Service(executable_path=ChromeDriverManager().install())
            driver = Chrome(service=service, options=self.set_chrome_options())
            
        # elif self.default_browser_name == 'firefox':
        #     driver_used = 'firefox'
        #     return driver_used
        # elif self.default_browser_name == 'edge':
        #     driver_used = 'edge'
        #     return driver_used
        # elif self.default_browser_name == 'opera':
        #     driver_used = 'opera'
        #     return driver_used
        return driver
    
    def forum_post(self):
        if self.name_of_program == 'Mycommerce':
            self.open_browser('https://forum.visualsoftware.inf.br/forumdisplay.php?fid=30')
        elif self.name_of_program == 'MyFrota':
            self.open_browser('https://forum.visualsoftware.inf.br/forumdisplay.php?fid=85')
        elif self.name_of_program == 'MyPet':
            self.open_browser('https://forum.visualsoftware.inf.br/forumdisplay.php?fid=82')
        if self.final_version:
            self.insert_new_topic_for_final_version()
        else:
            self.open_last_version_forum()
            self.add_new_response()
        
    def set_chrome_options(self):
        options = ChromeOptions()
        options = self.set_options(options)
        return options
    
    def set_firefox_options(self):
        options = FirefoxOptions()
        options = self.set_options(options)
        return options
    
    def set_opera_options(self):
        # terminar o da opera
        options = ChromeOptions()
        options = self.set_options(options)
        return options
    
    def set_edge_options(self):
        # terminar o da edge
        options = ChromeOptions()
        options = self.set_options(options)
        return options
    
    def set_options(self, options):
        options.add_argument("--log-level=3") # Silences error messages from Selenium console
        # options.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'
        if self.default_browser_name == 'brave' and 'chrome':
            options.binary_location = self.os_handler.get_default_browser_path()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument("--profile-directory=Default")
            options.add_argument(f'--user-data-dir={self.path_user}\cache')
        else:
            is_chrome_installed = self.os_handler.is_chrome_installed()
            if is_chrome_installed:
                options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
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
        if self.name_of_program == 'MyPet' or self.name_of_program == 'MyFrota': 
            click_last_post = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/table/tbody/tr[3]/td[3]/div/span/span/a')))
            click_last_post.click()
        elif self.name_of_program == 'Mycommerce': 
            click_last_post = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/table[2]/tbody/tr[3]/td[3]/div/span/span/a')))
            click_last_post.click()  
            
    def add_new_response(self):
        path_body_message = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[6]/td[2]/div/iframe'
        insert_message_button = '/html/body/div/div[2]/div/form/div/input[1]'
        path = '/html/body/div[1]/div[2]/div/div[3]/a' 
        path_js_body = "#content > div > form > table:nth-child(2) > tbody > tr:nth-child(6) > td:nth-child(2) > div > iframe"
        
        if  self.final_version:
            path_js_body = "#content > div > form > table:nth-child(2) > tbody > tr:nth-child(5) > td:nth-child(2) > div > iframe"
            path_body_message = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[5]/td[2]/div/iframe'
            path_topic_name_label = '/html/body/div/div[2]/div/form/table[1]/tbody/tr[3]/td[2]/input'
            self.click_base(path_topic_name_label).send_keys(self.topic_name_of_final_version)
        else:    
            self.click_base(path)
        # self.click_base(path_body_message).send_keys(self.message_version)
        pyperclip.copy(self.message_version)
        self.click_base(path_body_message).send_keys(Keys.CONTROL, 'v') 
        active_element = self.navegador.execute_script(f"""return document.querySelector("{path_js_body}")""")
        active_element.send_keys(Keys.CONTROL + "a")
        active_element.send_keys(Keys.CONTROL + "c")
        active_element.send_keys(Keys.CONTROL + "v")
        active_element.send_keys(Keys.CONTROL + "a")
        active_element.send_keys(Keys.CONTROL + "c")
        
        if not self.test_mode:    
            # clica no botão de inserir mensagem do post
            self.click_base(insert_message_button)
        else:
            print('modo de teste')
            sleep(10)
    
    def insert_new_topic_for_final_version(self):
        click_new_topic_path = '/html/body/div/div[2]/div/div[3]/a/span'
        self.click_base(click_new_topic_path)
        self.add_new_response()
      
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
        try:
            logged = self.navegador.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/a")
            is_logged = logged.is_displayed()
        except:
            is_logged = False
            
        if not is_logged:
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
        self.bitrix_post1()
        self.bitrix_post_2()
        
    def open_bitrix(self, link_bitrix):
        self.navegador.get(link_bitrix)
        sleep(2)
        self.login_bitrix()
        
    def login_bitrix(self):
        # verifica se existe um elemento antes de proseguir
        try:
            logged = self.navegador.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/div[1]/div[2]/div[1]/ul")
            is_logged = logged.is_displayed()
        except:
            is_logged = False
        if not is_logged:
            path_email = '/html/body/div/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[1]/div/input'
            path_passwd = '/html/body/div/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[2]/div/div[1]/div/input'
            path_next_login = '/html/body/div/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[5]/button[1]'
            path_next_login2 = '/html/body/div/div[2]/div/div[1]/div/div/div[3]/div/form/div/div[3]/button[1]'
            self.send_keys_base(path_email, self.bitrix_username)
            sleep(2)
            self.click_base(path_next_login)

            self.send_keys_base(path_passwd, self.bitrix_passwd)
            self.click_base(path_next_login2)

    def bitrix_post1 (self):
        path_post_body = '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td/div/div[2]/div/div[1]/div/div/div[2]/div'
        path_button_send = '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/table/tbody/tr/td/div/div[2]/div/div[1]/div/div/div[3]/form/div[4]/span[1]'
        self.click_base(path_post_body)
        sleep(0.5)
        # envia para o navegador, lembrar de verificar onde esta o foco antes de mandar o comando
        actions = ActionChains(self.navegador)
        actions.key_down(Keys.CONTROL)
        actions.send_keys("v")
        actions.key_up(Keys.CONTROL)
        actions.perform()

        # clica no botão de formatar texto 
        for item in range(0,100):
            try:
                button_format_text = self.navegador.find_element(By.XPATH, f'/html/body/div[{item}]/span[3]/span[2]')       
                # hover mouse to element
                actions.move_to_element(button_format_text).perform()
                sleep(1)
                button_format_text.click()
                print('achou o elemento')
                break
            except:
                print('Não achou o elemento')
        
        if not self.test_mode:
            # self.click_base(path_button_send) 
            # como não estava funcionando clicar no botão, mesmo o caminho dele não ter sido alterado
            # deixar como ctrl + enter
            actions.key_down(Keys.CONTROL)
            actions.send_keys(Keys.ENTER)
            actions.key_up(Keys.CONTROL)
            actions.perform()
            sleep(2)
        else:
            print('modo de teste')
            sleep(10)
    
    def bitrix_post_2(self):
        # path_open_chat = r'/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/div[1]/div[2]/div[1]/ul/li[3]/ul/li[2]/a/span[2]'
        # self.click_base(path_open_chat)
        self.navegador.get('https://visualsoftware.bitrix24.com.br/online/')
        text_find_chat = 'canais - avisos'
        sleep(6)
        for element in range(0,100):
            try:
                element = self.navegador.find_element(By.XPATH, f'/html/body/div[{element}]/div/div[1]/div/div[1]/div[2]/div/div[1]/div/div[1]/div[2]/div/input')  
                element.click()
                element.send_keys(text_find_chat)
                element.send_keys(Keys.ENTER)
                # JA ABERTO O CHAT AGORA IRÁ ESCREVER A MENSAGEM
                sleep(1)
                actions = ActionChains(self.navegador)
                # actions.key_down(Keys.CONTROL).perform()
                # actions.send_keys("v").perform()
                # actions.key_up(Keys.CONTROL).perform()
                pyperclip.copy(self.message_version)
                actions.send_keys((Keys.CONTROL, 'v')).perform()
                if not self.test_mode:
                    actions.key_down(Keys.ENTER).perform()
                    actions.key_up(Keys.ENTER).perform()
                    sleep(10)
                else:
                    print('modo de teste')
                    sleep(60)
                break
            except:
                print('erro', element)

if __name__ == '__main__':
    navegador = BrowserController(
        message_version="""
        Ei, pessoal! Temos novidades! A versão [b]10.07.22.0000[/b] do [b]Mycommerce[/b] já está no ar e pronta para ser atualizada! 🚀

        [b]🔍INCONSISTÊNCIAS RELATADAS POR CLIENTES:[/b]
        - Transferências de estoque sem complicações! Ajustamos a inconsistência ao gerar nota de transferências de estoque.
        - Relatórios de comissão em sintonia! Corrigimos a inconsistência onde os relatórios de comissão detalhado e resumido apresentavam valores diferentes.

        🌟 E não para por aí! Esta versão é 100% compatível com: 
        [b]03.67.02.0000[/b] do [b]MyCommerce PDV 🛒[/b]
        [b]10.07.03.0000[/b] do [b]MyLocação 🚗[/b]
        [b]10.05.00.0000[/b] do [b]MyPet 🐾[/b]
        [b]03.06.00.0000[/b] do [b]MyZap 📱[/b]
        [b]07.08.00.0000[/b] do [b]VsIntegrações 🔗[/b]

        ✨ Não espere mais, atualize e veja as novidades! 💡

        """,
        bitrix_username='',
        bitrix_passwd='',
        forum_username='',
        forum_passwd='',
        test_mode=True,
        # test_bitrix=True,
        test_forum=True,
        name_of_program='Mycommerce'
        # final_version=True,
        # topic_name_of_final_version= '9.12.x'
        )
