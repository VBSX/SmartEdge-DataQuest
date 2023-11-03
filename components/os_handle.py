import os
import sys
import threading
path = os.path.abspath('./')
sys.path.append(path)
import subprocess
from time import sleep

class OsHandler():
    def __init__(self):
        thread = threading.Thread(target=self.delete_atalho)
        thread.start()

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
        
        print(download_folder)
        
        path = f""" "{path}\\{file_name}" """
        print(path)
        command = f'copy {path} {download_folder}'
        print(command)
        subprocess.call(command, shell=True)

    def delete_atalho(self):
        while True:
            path = r'C:\Users\Visual Software\Desktop\Suporte Web Visual Software.lnk'
            if os.path.exists(path):
                os.remove(path)
                subprocess.call('ie4uinit.exe -show', shell=True)
                print('arquivo de atalho deletado')
            sleep(1)
            
if __name__ == "__main__":
    os_handler = OsHandler()

