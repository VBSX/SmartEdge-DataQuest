
import configparser
class IniConfig():
    def __init__(self):
        c_path = r'C:\Visual Software\MyCommerce'
        self.path_config = c_path + r'\Config.ini'
        self.config = configparser.ConfigParser()
        self.config.read(self.path_config)

        self.host_ini = self.read_config('IPServidor')
        self.database_ini = self.read_config('database')
        self.port_ini = self.read_config('PortaServidor')

    def read_config(self, key):
        valor = self.config.get('Servidor', f'{key}')
        return valor
    
    def set_host(self, host):
        self.config_att_value('IPServidor', host)
    
    def set_database(self, database):
        self.config_att_value('database', database)
        
    def set_port(self, port):
        self.config_att_value('PortaServidor', port)
    
    def config_att_value(self, key, new_value):
        self.config.set('Servidor', f'{key}', f'{new_value}')
        with open(self.path_config, 'w') as arquivo:
            self.config.write(arquivo)

if __name__ == '__main__':
    config = IniConfig()
    print(config.ip_ini)
    