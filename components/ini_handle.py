from configparser import ConfigParser

class IniConfig:
    def __init__(self, config_path=None):
        self.config_path = config_path or r'C:\Visual Software\MyCommerce\Config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_path)

        self.host_ini = self.read_config('IPServidor')
        self.database_ini = self.read_config('database')
        self.port_ini = self.read_config('PortaServidor')

    def read_config(self, key_of_field):
        return self.config.get('Servidor', key_of_field, fallback=None)

    def set_host(self, host):
        self.config_att_value('IPServidor', host)

    def set_database(self, database):
        self.config_att_value('database', database)

    def set_port(self, port):
        self.config_att_value('PortaServidor', port)

    def config_att_value(self, key, new_value):
        self.config.set('Servidor', key, str(new_value))
        with open(self.config_path, 'w') as arquivo:
            self.config.write(arquivo)

if __name__ == '__main__':
    config = IniConfig()
    print(config.read_config('PortaServidor'))
