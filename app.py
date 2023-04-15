import os
import time
import random
import markdown
from datetime import datetime, timedelta

from flask_basicauth import BasicAuth
from flask import Flask, render_template, request, redirect, send_file, make_response

import config

app = Flask(__name__, template_folder="static/")

PATH = "static/notes"

app.config['BASIC_AUTH_USERNAME'] = config.AUTH_USERNAME 
app.config['BASIC_AUTH_PASSWORD'] = config.AUTH_PASSWORD 

basic_auth = BasicAuth(app)


def note_caption(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        return [i.split("\n")[0].split("# ")[-1] for i in file.readlines() if i[0] == "#"]


def note_creation(filename: str):
    return time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getctime(filename)))


@app.template_filter()
def md(text):
    return markdown.markdown(text)


@app.route('/static/images/<filename>')
def get_image(filename):
    response = make_response(send_file(f"static/images/{filename}"))
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    response.headers['Expires'] = (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    response.headers['Last-Modified'] = (datetime.now() - timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')

    return response


@app.route("/add", methods=["GET"])
def add_note_page():
    return render_template("add.html")


@app.route("/notes/remove/<filename>", methods=["GET"])
def remove_note(filename):
    os.remove(f"{PATH}/{filename}")

    return redirect("/")


@app.route("/notes/add/<filename>", methods=["POST"])
def add_note(filename):
    filename = f"{random.randrange(1000, 10000000000)}.md"
    with open(f"{PATH}/{filename}", "w", encoding="utf-8") as f:
        content = request.form["note-content"]
        print(content)
        f.write(content)
    return redirect(f"/notes/{filename}")


@app.route("/notes/edit/<filename>", methods=["GET", "POST"])
def edit_note(filename):
    lines = []
    with open(f"{PATH}/{filename}", "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip())

        note_content = "\n".join(lines)

    print(note_content)

    if request.method == "POST":
        edited_content = request.form["note-content"]
        print(edited_content)
        with open(f"{PATH}/{filename}", "w", encoding="utf-8") as f:
            f.seek(0)
            f.write(edited_content)
            f.truncate()
        return redirect(f"/notes/{filename}")

    return render_template("edit.html", filename=filename, note_content=note_content)


@app.route("/notes/<filename>", methods=["GET"])
def get_notes_by_filename(filename):
    html_lines = []
    with open(f"{PATH}/{filename}", "r", encoding="utf-8") as file:
        for line in file:
            html_lines.append(md(line.strip()))
    html_content = "\n".join(html_lines)
    return render_template("note.html", content=html_content, file=filename)


@app.route("/", methods=["GET"])
@basic_auth.required
def get_notes():
    notes = []
    for i in os.listdir(PATH):
        note_name = note_caption(f"{PATH}/{i}")[0]
        note_date = note_creation(f"{PATH}/{i}")
        note = {"caption": note_name, "date": note_date, "filename": i}
        notes.append(note)

    print(notes)
    return render_template(f"index.html", notes=notes, profile=config.profile, len=len)


def main(a=1, b=1): # without these arguments app does not want to work on heroku host idk whats the issue lol 
    return app.run(threaded=True, port=5000)


if __name__ == '__main__':
    main()
