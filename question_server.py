#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask, request, redirect, Response
import MySQLdb


host = "127.0.0.1"  # poridore.mysql.pythonanywhere-services.com
user = "root"
pwd = ""
db = "wb"
app = Flask(__name__)

url = "http://poridore.pythonanywhere.com/"

db = MySQLdb.connect(host, user, pwd, db)


@app.route("/question", methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        try:
            question = str(request.form['question'])
        except KeyError, e:
            question = str(request._content)
        try:
            cs = db.cursor()
            cs.execute("""INSERT INTO question(libelle) VALUES (%s);""", (question,))
            id = cs.lastrowid
            db.commit()
            return redirect("/question/" + str(id), code=302)
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError, i:
                print "MySQL Error: %s" % str(i)
            return "Could not store the question", 500

    elif request.method == "GET":
        with open("template/add_question.html") as f:
            return f.read(), 200


@app.route("/question/<param>", methods=['GET', 'POST'])
def a_question(param):
    if request.method == 'POST':
        question = param
        try:
            cs = db.cursor()
            cs.execute("""INSERT INTO question(libelle) VALUES (%s);""", (question,))
            id = cs.lastrowid
            db.commit()

            resp = Response("")
            resp.headers['Link'] = url + "response/" + str(id) + "; rel=\"response\""
            return resp, 201
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError, z:
                print "MySQL Error: %s" % str(z)
            return "Could not store the question", 500

    elif request.method == 'GET':
        try:
            id = str(param)
            cs = db.cursor()
            cs.execute("""SELECT id, libelle FROM question WHERE id = (%s);""", (id,))
            for row in cs:
                id = row[0]
                question = row[1]
                resp = {"id": id, "question": question}
            return json.dumps(resp), 200
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError, i:
                print "MySQL Error: %s" % str(i)
            return "Could not get the question", 500


@app.route("/question_non_traite", methods=['GET'])
def question_non_traite():
    try:
        cs = db.cursor()
        cs.execute(""" SELECT id, libelle FROM question WHERE traite = FALSE LIMIT 1 """)

        for row in cs:
            id = row[0]
            question = row[1]
            resp = {"id": id, "question": question}

            return json.dumps(resp), 200

        return "", 404

    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError, i:
            print "MySQL Error: %s" % str(i)
        return "Could not get the question", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    db.close()
