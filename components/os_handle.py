import os
import sys
import threading
path = os.path.abspath('./')
sys.path.append(path)
import subprocess
from time import sleep
from cpuinfo import get_cpu_info
from multiprocessing import freeze_support
import platform
import psutil

class OsHandler():
    def __init__(self):
        self.loop = True
        # self.thread = threading.Thread(target=self.delete_atalho)
        # self.thread.start()

    def kill_mycommerce_process(self):
        process_name = "mycommerce.exe"
        result = self.process_killer(process_name)
        return result

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
            return f"Erro ao tentar encerrar o processo:\n{stderr_str}"

    def download_version(self, path, file_name ):
        # copy file to downloads folder
        d = os.path.join(os.path.expanduser('~'), 'Downloads')
        download_folder = f""" "{d}" """
        path = f""" "{path}\\{file_name}" """
        command = f'copy {path} {download_folder}'
        subprocess.call(command, shell=True)

    def delete_atalho(self):
        while self.loop:
            path = r'C:\Users\Visual Software\Desktop\Suporte Web Visual Software.lnk'
            if os.path.exists(path):
                os.remove(path)
                subprocess.call('ie4uinit.exe -show', shell=True)
                print('arquivo de atalho deletado')
            sleep(1)
            
    def verify_if_has_connection(self, log_path = False):
        # caminho da rede a ser verificado
        if not log_path:
            path = r'\\10.1.1.110\Arquivos'
        else:
            path = r'\\192.168.2.244\shared'
                
        # verifica se o caminho é acessível
        if os.path.exists(path):
            return True
        else:
            return False
    
    def get_machine_name(self):
        return os.getenv('COMPUTERNAME')
    
    def init_data_user(self):
        os_used = platform.system()
        os_version = platform.release()

        ram_quantity_of_machine = psutil.virtual_memory()
        ram_quantity_of_machine = ram_quantity_of_machine.total / 1024 / 1024 / 1024
        ram_quantity_of_machine = round(ram_quantity_of_machine, 1)
        
        cpu_quantity_of_machine = os.cpu_count()
        
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
        
if __name__ == "__main__":
    # freeze_support()
    os_handler = OsHandler()
    print(
    # os_handler.verify_if_has_connection(log_path=True),
    # os_handler.get_machine_name()
    os_handler.init_data_user()
    )
    # os_handler.stop_loop_delete_atalho()

