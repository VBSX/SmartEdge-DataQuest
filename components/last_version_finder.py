import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from components.os_handle import OsHandler

class LatestVersion():
    def __init__(self):
        base_path = r'\\10.1.1.110\\Arquivos\\Atualizacoes\\'
        self.path_mycommerce_att = base_path+'MyCommerce'
        self.path_mycommerce_pdv = base_path+'MyCommercePDV'
        self.path_mylocacao = base_path+'MyLocacao'
        self.path_mypet = base_path+'PetShop'
        self.path_myzap = base_path+'MyZap - Configurador'
        self.path_vsintegracoes = base_path+'vsIntegracoes'
        self.os_handler = OsHandler()
        self.has_connection = self.os_handler.verify_if_has_connection()
        
    def latest_release_version(self, path, software_name):
        if self.has_connection:
            all_archives = os.listdir(path)
            archives = []
            # find by .exe files
            if software_name =='Mycommerce':
                endswith = 'MyCommerce_Full.exe'
            elif software_name == 'MycommercePDV':
                endswith = 'MyCommercePDV - Initial_Install - 3.60.42.0.exe'
            elif software_name == 'MyLocacao':
                endswith = 'MyLocacao_Full.exe'
            elif software_name == 'MyPet':
                endswith = 'PetShop_Full.exe'
            elif software_name == 'MyZap':
                endswith = 'MyZap - Configurador_Full.exe'
            elif software_name == 'vsIntegracoes':
                endswith = 'vsIntegracoes_Full.exe'
            

            for archive in all_archives:
                if archive.endswith('0.exe') and not archive.endswith(endswith):
                    archives.append(archive)
                    
            if len(archives) >1:
                # aqui ele vai ordernar do menor para o maior, no caso o maoir é o mais recente
                archives.sort()
                return archives[-1]
            elif len(archives) == 1:
                return archives[0]
    
    def latest_release_version_text(self):
        return self.text_strip(self.latest_release_version(self.path_mycommerce_att, 'Mycommerce'))
    
    def latest_build_version(self):
        if self.has_connection:
            all_archives = os.listdir(self.path_mycommerce_att)
            # find by .exe files
            archives = [archive for archive in all_archives if archive.endswith('.exe') if not archive.endswith('MyCommerce_Full.exe') if not archive.endswith('0.exe')]
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
                        'MyLocacao_', 'Robô MyZap - Atu_'
                        ]
        if text:
            for item in list_of_text:
                if item in text:
                    text = text.replace(item, '').replace('.exe', '')

        return text

    def download_file(self, file_name):
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
    
    def close(self):
        self.os_handler.stop_loop_delete_atalho()
    
if __name__ == '__main__':
    # print('mylocacao',LatestVersion().latest_release_version_text_mylocacao())
    # print('mypet',LatestVersion().latest_release_version_text_mypet())
    # print('myzap',LatestVersion().latest_release_version_text_myzap())
    # print('vsintegracoes',LatestVersion().latest_release_version_text_vsintegracoes())
    print(LatestVersion().download_latest_release())
    # print(LatestVersion().latest_release_version_text())
    
    

