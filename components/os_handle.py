import subprocess

class OsHandler():
    def __init__(self):
        pass

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

if __name__ == "__main__":
    os_handler = OsHandler()
    print(os_handler.kill_mycommerce_process())
