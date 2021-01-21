from bs4 import BeautifulSoup as bs
import requests
import re
from flask import Flask, render_template

url = "https://dm.quicksearch.se/QSNetComponents/QS.Org/default.aspx?HolderGroupId=%7BB1D742BA-92A6-49A3-AFC5-FAD6D7016860%7D&RootGroupdId=%7BE4F30D0D-D812-4EE8-AAB4-89E4C2204C03%7D&ContractId=%7BABF0D62C-E7EA-419A-AD76-C7EADAA134E5%7D&LanguageId=%7BA1DE86C9-934F-4FCE-B753-9F01AEDBB8BE%7D&UserId=%7BD5113524-69DA-43BA-A898-36F2678CA2C7%7D&circular_id=%7B7EB91046-7E2B-4112-ABDD-864EC69EC9C5%7D&Freq=True&antiCsrfToken=11151249041l163190"
programs = {"IT": ["TKITE", "MPIDE", "MPSOF", "MPDSC"]}

app = Flask(__name__)

def get_program_answers(request):
    program_answers = {}
    parser = bs(request, "html.parser")
    answers_reg = re.compile(r"[a-zA-Z]*\s\((\d+)/(\d+)")
    tag = list(parser.find_all(["span"]))
    for program_name in programs.keys():
        program = programs.get(program_name)
        program_answers[program_name] = {"sub_divisions": {}}
        for sub_program in program:
            for span in tag:
                text = span.get_text()
                if sub_program in text:
                    answers, total = answers_reg.match(text).groups()
                    answers = int(answers)
                    total = int(total)
                    p = program_answers[program_name]["sub_divisions"]
                    p[sub_program] = {"answers": answers, "total": total, "percent": answers/total*100}
    return program_answers

def count_total(division_dict):
    total = 0
    answers = 0
    sub_divisions = division_dict["sub_divisions"]
    for key in sub_divisions:
        answers += sub_divisions[key]["answers"]
        total += sub_divisions[key]["total"]
    return (answers, total)

def get_data():
    req = requests.get(url)
    program_answers = get_program_answers(req.text)
    for key in program_answers.keys():
        key_object = program_answers[key]
        (answers, total) = count_total(key_object)
        key_object["total"] = total
        key_object["answers"] = answers
        key_object["percent"] = int(answers / total*100)
    return program_answers

@app.route('/')
def get_answers():
    data = get_data()
    return render_template("index.html", result=data)

if __name__ == "__main__":
   app.run(host='0.0.0.0')