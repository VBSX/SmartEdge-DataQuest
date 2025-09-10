from os.path import abspath as path_os
from os import listdir
from sys import path as syspath
path = path_os('./')
syspath.append(path)
from components.os_handle import OsHandler

class LatestVersion():
    def __init__(self):
        base_path = r'\\10.1.1.110\\Arquivos\\Atualizacoes\\'
        self.path_mycommerce_att = base_path+'MyCommerce'
        self.path_mycommerce_pdv = base_path+'MyCommercePDV'
        self.path_mylocacao = base_path+'MyLocacao'
        self.path_mypet = base_path+'PetShop'
        self.path_myzap = base_path+'MyZap - Configurador'#+ r'\\Versoes liberadas\\Última liberada'
        self.path_vsintegracoes = base_path+'vsIntegracoes'
        self.path_myfrota = base_path+'MyFrota'
        self.path_mycomanda = base_path+'MyComanda'
        self.os_handler = OsHandler()
        self.has_connection = self.os_handler.verify_if_has_connection()
        
    def latest_release_version(self, path, software_name):
        if self.has_connection:
            all_archives = listdir(path)
            archives = []
            # find by .exe files
            if software_name =='Mycommerce':
                startwith = 'MyCommerce_Full'
            elif software_name == 'MycommercePDV':
                startwith = 'MyCommercePDV - Initial_Install'
            elif software_name == 'MyLocacao':
                startwith = 'MyLocacao_Full'
            elif software_name == 'MyPet':
                startwith = 'PetShop_Full'
            elif software_name == 'MyZap':
                startwith = 'MyZap - Configurador_Full'
            elif software_name == 'vsIntegracoes':
                startwith = 'vsIntegracoes_Full_'
            elif software_name == 'MyFrota':
                startwith = 'MyFrota__Full_'
            elif software_name == 'MyComanda':
                startwith = 'MyComanda_Full_'

            for archive in all_archives:
                if archive.endswith('0.exe') and not archive.startswith(startwith):
                    archives.append(archive)
        
                 
            if len(archives) > 1:
                if software_name == 'MyPet': 
                    # Ordena a lista usando uma função de chave personalizada para classificar as versões mais recentes
                    archives.sort(key=lambda x: tuple(map(int, x.split('_')[1].split('.')[:-1])), reverse=True)
                    return archives[0]  # Retorna o primeiro item (o mais recente) da lista ordenada
                else:
                    archives.sort(reverse=True)
                    return archives[0]
            elif len(archives) == 1:
                return archives[0]
    
    def latest_release_version_text(self):
        return self.text_strip(self.latest_release_version(self.path_mycommerce_att, 'Mycommerce'))
    
    def latest_build_version(self):
        if self.has_connection:
            all_archives = listdir(self.path_mycommerce_att)
            # find by .exe files
            archives = [archive for archive in all_archives if archive.endswith('.exe') if not archive.endswith('MyCommerce_Full.exe') if not archive.endswith('MyCommerce_Full_Em_Teste.exe') if not archive.endswith('0.exe')]
            if archives:
                return archives[-1]
            else:
                return 'SemBuild'
        else:
            return 'SemBuild'
        
    def latest_build_version_text(self):
        if self.latest_build_version() == 'SemBuild':
            return 'SemBuild'
        else:
            return self.text_strip(self.latest_build_version())
   
    def text_strip(self, text):
        list_of_text = ['MyCommercePDV_FULL_',
                        'MyCommerce_Atu',
                        'PetShopAtu_',
                        'vsIntegracoes_Atu_',
                        'vsIntegracoes_Full_',
                        'MyLocacao_', 'Robô MyZap - Atu_', 'MyFrota__Atu_',
                        "MyComanda_"
                        ]
        if text:
            for item in list_of_text:
                if item in text:
                    text = text.replace(item, '').replace('.exe', '').replace(' ', '')

        return text

    def download_file(self, file_name, is_other_version_than_build_and_release=False, path=None):
        if is_other_version_than_build_and_release and path:
            return self.os_handler.download_version(path, file_name)
        else:
            return self.os_handler.download_version(self.path_mycommerce_att, file_name)

    def download_latest_build(self):
        if self.has_connection:
            build = self.latest_build_version() 
            if build == 'SemBuild':
                return 'SemBuild'
            else:
                return self.download_file(build)
        else:
            return 'SemBuild'
            
    def download_latest_release(self):
        if self.has_connection:
            return self.download_file(self.latest_release_version(self.path_mycommerce_att,'Mycommerce'))
        else:
            return 'SemBuild'

    def latest_release_version_text_pdv(self):
        return self.text_strip(self.latest_release_version(self.path_mycommerce_pdv, 'MycommercePDV'))
    
    def latest_release_version_text_mylocacao(self):
        return self.text_strip(self.latest_release_version(self.path_mylocacao, 'MyLocacao'))
    
    def latest_release_version_text_mypet(self):
        return self.text_strip(self.latest_release_version(self.path_mypet,'MyPet'))
    
    def latest_release_version_text_myzap(self):
        return self.text_strip(self.latest_release_version(self.path_myzap,'MyZap'))
    
    def latest_release_version_text_vsintegracoes(self):
        return self.text_strip(self.latest_release_version(self.path_vsintegracoes, 'vsIntegracoes'))
    
    def latest_release_version_text_myfrota(self):
        return self.text_strip(self.latest_release_version(self.path_myfrota, 'MyFrota'))
    
    def latest_release_version_text_mycomanda(self):
        return self.text_strip(self.latest_release_version(self.path_mycomanda, 'MyComanda'))
    
    def close(self):
        self.os_handler.stop_loop_delete_atalho()
    
    def cancel_download(self):
        self.os_handler.download_process_stop()
        
    def download_by_version(self, version):
        # o usuario pode colocar a versão da seguinte forma 10.07.02.0000
        
        # remove 0 a esquerda
        version_parts = version.split('.')
        version_parts = [str(int(part)) for part in version_parts]
        version = '.'.join(version_parts)
        
        version_finded_path = self.find_if_version_exists(version)
        version_full_name = f'MyCommerce_Atu {version}.exe'
        if version_finded_path != None:
            self.download_file(path=version_finded_path, is_other_version_than_build_and_release=True, file_name=version_full_name)
            return True
        else:
            return False
        
        
    def find_if_version_exists(self, version):
        # lista todos os arquivos do diretorio
        all_archives = listdir(self.path_mycommerce_att)
        archives = []
        version_folder = version.split('.')
        
        for part in version_folder:
            # ele vai tirar as duas ultimas partes para sair de "10.7.2.0" para "10.7.0" que é a forma 
            # usada na pasta da versão

            if len(version_folder) > 2:
                version_folder.pop()    
                
        version_folder = '.'.join(version_folder)+'.0'
            
            
            
        # sera buscado a pasta com o texto 'Versão {10.7.0}' e depois acessada a pasta "Versão Final" e logo em seguida 
        # será verificado se existe o arquivo com o texto '10.7.2.0.exe'
        version_text = f'Versão {version_folder}'
        for archive in all_archives:
            if version_text in archive:
                version_path = f"{self.path_mycommerce_att}\\{archive}\\Versão Final"
                if listdir(version_path):
                    for file in listdir(version_path):
                        # aqui vai ser verificado se existe o arquivo 
                        # com o texto 'MyCommerce_Atu 10.7.2.0.exe'
                        version_full_name = f'MyCommerce_Atu {version}.exe'
                        if version_full_name in file:
                            return version_path
        return None

    
        
if __name__ == '__main__':
    # print('mylocacao',LatestVersion().latest_release_version_text_mylocacao())
    # print('mypet',LatestVersion().latest_release_version_text_mypet())
    # print('myzap',LatestVersion().latest_release_version_text_myzap())
    # print('vsintegracoes',LatestVersion().latest_release_version_text_vsintegracoes())
    print(LatestVersion().latest_release_version_text_mycomanda())
    # print(LatestVersion().download_by_version('10.07.02.0000'))
    # print(LatestVersion().download_latest_release())
    
    
    

