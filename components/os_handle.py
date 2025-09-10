from os import (
    startfile,
    remove,
    getenv,
    cpu_count,
    )
from os.path import (
    abspath as path_os,
    join,
    expanduser,
    exists,
    basename
    )
from sys import path as syspath
path = path_os('./')
syspath.append(path)
import psutil
# import threading
from shutil import which
import subprocess
from time import sleep
from cpuinfo import get_cpu_info
from multiprocessing import freeze_support
from  platform import (
    system as platform_system,
    release as platform_release
    )
from psutil import virtual_memory
from time import sleep

class OsHandler():
    def __init__(self):
        self.loop = True
        # self.thread = threading.Thread(target=self.delete_atalho)
        # self.thread.start()

    def kill_mycommerce_process(self):
        process_name = "mycommerce.exe"
        result = self.process_killer(process_name)
        if "ERRO" in result:
            # Se não encontrou o processo, tenta com psutil
            result = self.process_killer_by_psutil(process_name)
        return result

    def kill_mymonitorfat_process(self):
        process_name = "MyMonitorFaturamento.exe"
        result = self.process_killer(process_name)
        return result
    
    def kill_att_db_process(self):
        process_name = "AtualizarDB.exe"
        result = self.process_killer(process_name)
        return result
    
    def start_myzap_service(self):
        service_name = "svcMyZap"
        try:
            result = subprocess.run(["sc", "start", service_name],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                return f"Serviço '{service_name}' iniciado com sucesso."
            else:
                return f"Erro ao iniciar '{service_name}': {result.stderr or result.stdout}"
        except Exception as e:
            return f"Erro ao tentar iniciar o serviço '{service_name}': {e}"
    
    def stop_myzap_service(self):
        # verifica se o serviço svcMyZap está em execução e tenta pará-lo

        service_name = "svcMyZap"
        try:
            result = subprocess.run(["sc", "stop", service_name],
                                    capture_output=True, text=True)
            if result.returncode == 0:
                return f"Serviço '{service_name}' parado com sucesso."
            else:
                return f"Erro ao parar '{service_name}': {result.stderr or result.stdout}"
        except Exception as e:
            return f"Erro ao tentar parar o serviço '{service_name}': {e}"

    def myzap_service_status(self):
        service_name = "svcMyZap"
        try:
            for service in psutil.win_service_iter():
                if service.name().lower() == service_name.lower():
                    if service.status() == 'running':
                        # devolve o emoji de bolinha verde
                        return "🟢"
                    elif service.status() == 'stopped':
                        # devolve o emoji de bolinha vermelha
                        return "🔴"
            # bolinha amarela quando nao acha ou está finalizando/iniciando   
            return f"🟡"
        except Exception as e:
            return f"Erro ao verificar o status do serviço '{service_name}': {e}"
    
    def process_killer(self, nome_processo):
        command = f"taskkill /F /IM {nome_processo}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()

        stderr_str = error.decode('utf-8', errors='ignore')

        # Verificar se o processo não foi encontrado
        if "O processo" in stderr_str and "não foi encontrado" in stderr_str:
            return f"ERRO: o processo '{nome_processo}' não foi encontrado."
        elif process.returncode == 0:
            return "Processo encerrado com sucesso."
        else:
            # Retornar a saída de erro padrão se houver outros erros
            return f"ERRO: ao tentar encerrar o processo:\n{stderr_str}"  
    
    def process_killer_by_psutil(self, nome_processo: str):
        nome_processo = nome_processo.lower()
        encontrados = []

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] and proc.info['name'].lower() == nome_processo:
                    encontrados.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not encontrados:
            return f"ERRO: processo '{nome_processo}' não encontrado."

        erros = []
        for proc in encontrados:
            try:
                proc.kill()
            except Exception as e:
                erros.append(f"PID {proc.pid}: {e}")

        if erros:
            return "Ocorreram erros ao tentar encerrar:\n" + "\n".join(erros)
        else:
            return f"Processo '{nome_processo}' encerrado com sucesso."
    
    def download_version(self, path, file_name ):
        self.canceled = False
        # copy file to downloads folder
        d = join(expanduser('~'), 'Downloads')
        download_folder = f""" "{d}" """
        path = f""" "{path}\\{file_name}" """
        command = f'copy {path} {download_folder}'
        path_exe_on_download_folder = rf"""{d}\{file_name}"""

        download_sub = subprocess.Popen(
            command, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,shell=True)
        
        # ele fica verificando quando o download_sub terminou, dando margem para que o mesmo
        # possa ser cancelado quando necessário
        try:
            while True:
                if not self.canceled:
                    # Verificar se o processo terminou
                    try:
                        result, error = download_sub.communicate(timeout=0)
                        result = result.decode('utf-8', errors='ignore')
                        if result:
                            if not error:
                                startfile(path_exe_on_download_folder)
                                return "sucesso"
                            break
                    except:
                        pass    
                else:
                    # Cancelar o processo se a flag 'canceled' estiver definida
                    print('cancelado')
                    download_sub.kill()
                    download_sub.wait()
                    print('processo cancelado')
                    delete = subprocess.Popen(f'del "{path_exe_on_download_folder}"' ,shell=True)
                    self.finished = True
                    break
        except Exception as err:
            return err
    
    def download_process_stop(self):
        self.finished = False
        # ele vai parar a função download_version quando chamado
        self.canceled = True
        while not self.finished:
            pass

    def delete_atalho(self):
        while self.loop:
            path = r'C:\Users\Visual Software\Desktop\Suporte Web Visual Software.lnk'
            if exists(path):
                remove(path)
                subprocess.call('ie4uinit.exe -show', shell=True)
                print('arquivo de atalho deletado')
            sleep(1)
            
    def ping(self, host, timeout=1):
        param = '-n' if platform_system().lower()=='windows' else '-c'
        command = ['ping', param, '1,5', '-w', str(timeout), host]
        result = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        return result == 0
    
    def verify_if_has_connection(self, log_path = False):
        # if not log_path:
        ip = r'10.1.1.110'
        # else:
        #     # path = r'\\192.168.2.244\shared'
        #     ip = r'192.168.2.231'
                
        if self.ping(ip):
            print(f'tem conexão: ip: {ip}')
            return True
        else:
            print(f'não tem conexão: ip: {ip}')
            return False
    
    def get_machine_name(self):
        return getenv('COMPUTERNAME')
    
    def init_data_user(self):
        print('buscou pelos dados do pc')
        os_used = platform_system()
        os_version = platform_release()

        ram_quantity_of_machine = virtual_memory()
        ram_quantity_of_machine = ram_quantity_of_machine.total / 1024 / 1024 / 1024
        ram_quantity_of_machine = round(ram_quantity_of_machine, 1)
        
        cpu_quantity_of_machine = cpu_count()
        
        # obrigatorio ter isso usando pyinstaller se não cria janelas infinitas
        # freeze_support() Pyinstaller may spawn infinite processes if __main__ is not used
        freeze_support()
        cpu_model_of_machine  = get_cpu_info()['brand_raw']

        return {
            'os_used': os_used,
            'os_version': os_version,
            'ram_quantity_of_machine': ram_quantity_of_machine,
            'cpu_quantity_of_machine': cpu_quantity_of_machine,
            'cpu_model_of_machine': cpu_model_of_machine
        }
        
    def stop_loop_delete_atalho(self):
        self.loop = False     
    
    def get_default_browser_path(self):
        browser_path = which('open')

        osPlatform = platform_system()

        if osPlatform == 'Windows':
            # Find the default browser by interrogating the registry
            try:
                from winreg import HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, OpenKey, QueryValueEx

                with OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as regkey:
                    # Get the user choice
                    browser_choice = QueryValueEx(regkey, 'ProgId')[0]

                with OpenKey(HKEY_CLASSES_ROOT, r'{}\shell\open\command'.format(browser_choice)) as regkey:
                    # Get the application the user's choice refers to in the application registrations
                    browser_path_tuple = QueryValueEx(regkey, None)

                    # This is a bit sketchy and assumes that the path will always be in double quotes
                    browser_path = browser_path_tuple[0].split('"')[1]
                    browser_path = rf'{browser_path}'
                    return browser_path

            except Exception:
                return 'Não foi possível encontrar o navegador padrão.'

    def is_chrome_installed(self):
        # Verifica se o Google Chrome está instalado na pasta padrão no Windows
        if exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"):
            return True
        # Verifica se o Google Chrome está instalado na pasta padrão em sistemas Linux
        elif exists("/usr/bin/google-chrome"):
            return True
        else:
            return False
    
    def get_name_of_default_browser(self):
        path_default_browser = self.get_default_browser_path()
        if path_default_browser:
            brs = basename(path_default_browser)
            brs = brs.split('.')[0]
            return brs  
        
            
    def get_version_of_browser(self, browser_name):
        path_chrome = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        path_brave = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        
        if browser_name == 'chrome':
            if exists(path_chrome):
                path_browser = path_chrome
        elif browser_name == 'brave':
            if exists(path_brave):
                path_browser = path_brave

        command = f'wmic datafile where "name=\'{path_browser.replace("\\", "\\\\")}\'" get Version'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        version = result.stdout.strip().split("\n")[-1]
        return version

            
if __name__ == "__main__":
    # freeze_support()
    os_handler = OsHandler() 
    # while True:

    #     print(os_handler.ping('10.1.1.110'))
        
    #     sleep(0.5)
    print(os_handler.myzap_service_status())
    print(os_handler.stop_myzap_service())
    print(os_handler.myzap_service_status())