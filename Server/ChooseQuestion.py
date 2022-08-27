import requests
import ServerTools
import json

config = ServerTools.read_config()

def get_the_question_structure():
    url = config["Printer_URL"]+"/structure"
    x = requests.get(url)
    return json.loads(x.text)


if __name__=="__main__":
    print(get_the_question_structure())