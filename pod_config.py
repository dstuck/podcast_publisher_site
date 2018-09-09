import yaml

def get_conf(conf_loc='config.yaml'):
    with open(conf_loc, 'r') as ymlfile:
        conf = yaml.load(ymlfile)
    return conf
