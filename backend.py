from bs4 import BeautifulSoup as bs
import requests
import re
from flask import Flask, render_template
import config_loader as cl

app = Flask(__name__)

def get_program_answers(request):
    programs = cl.get_divisions()
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
                    p[sub_program] = {"answers": answers, "total": total, "percent": int(answers/total*100)}
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
    url = cl.get_url()
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