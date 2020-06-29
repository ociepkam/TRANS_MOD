import yaml


def load_config():
    try:
        with open("config.yaml") as yaml_file:
            doc = yaml.load(yaml_file, Loader=yaml.FullLoader)
        return doc
    except:
        raise Exception("Can't load config file")


# Ę, Ł, Ń doesn't work
def replace_polish(text):
    letters = {"Ĺ»": "Ż", "Ã": "Ó", "Ă“": "Ł", "Ä†": "Ć", "Ä": "Ę", "Ĺš": "Ś", "Ä„": "Ą", "Ĺą": "Ź", "Å": "Ń",
               "ĹĽ": "ż", "Ã³": "ó", "Ĺ‚": "ł", "Ä‡": "ć", "Ä™": "ę", "Ĺ›": "ś", "Ä…": "ą", "Ĺş": "ź", "Ĺ„": "ń"}

    for k, v in letters.items():
        text = text.replace(k, v)
    return text