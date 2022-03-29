"""
Loads config.yaml
"""
import yaml

class Configuration:

    def __init__(self, conf_yaml):
        self.conf_dict = self.load_config(conf_yaml)
        self.from_addr = self.conf_dict['from_addr']
        self.to_addr = self.conf_dict['to_addr']
        self.password = self.conf_dict['password']
        self.margin_type_list = self.conf_dict['margin_type']
        self.cc_with_sod_ci = self.conf_dict["cc_with_sod_ci"]
        self.cc_with_eod_ci = self.conf_dict["cc_with_eod_ci"]
        self.ci_eod_with_sod = self.conf_dict["ci_eod_with_sod"]
        self.smtp_server = self.conf_dict["smtp_server"]
        self.smtp_server_port = self.conf_dict["smtp_server_port"]


    def load_config(self, conf_yaml):
        stream = open(conf_yaml, 'r')
        return yaml.safe_load(stream)

#eex_old/conf/config.yaml

conf = Configuration('conf/config.yaml')
