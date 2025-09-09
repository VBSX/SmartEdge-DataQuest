from configparser import ConfigParser

class IniConfig:
    def __init__(self, config_path=None, post_creator_ini=False):
        self.post_creator_ini = post_creator_ini
        
        if not self.post_creator_ini:
            self.config_path = config_path or r'C:\Visual Software\MyCommerce\Config.ini'
            self.config_path_mycomanda = r"C:\Visual Software\MyComanda\Config.ini"
        else:
            self.config_path = r'components/automation_windows/post_creator.ini'
        self.config = ConfigParser()
        self.config.read(self.config_path)

        self.host_ini = self.read_config('IPServidor')
        self.database_ini = self.read_config('database')
        self.port_ini = self.read_config('PortaServidor')
        self.test_mode = self.read_config('cqp')
        
    def read_config(self, key_of_field):
        if self.post_creator_ini:
            self.config.read(self.config)
            return self.config.get('DEFAULT', key_of_field, fallback=None)
        else:
            return self.config.get('Servidor', key_of_field, fallback=None)

    def set_host(self, host):
        self.config_att_value('IPServidor', host)

    def set_database(self, database):
        self.config_att_value('database', database)

    def set_port(self, port):
        self.config_att_value('PortaServidor', port)

    def set_test_mode(self, test_mode):
        self.config_att_value('cqp', test_mode)
    
    def config_att_value(self, key, new_value):
        try:
            self.config.set('Servidor', key, str(new_value))
            for file in [self.config_path, self.config_path_mycomanda]:
                with open(file, 'w') as arquivo:
                    self.config.write(arquivo)

        except Exception as e:
            return e

if __name__ == '__main__':
    config = IniConfig()
    print(config.read_config('PortaServidor'))
