#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect
import MySQLdb


app = Flask(__name__)

with MySQLdb.connect(host="localhost", user="root", passwd="root", db="wb") as cs:

    @app.route("/question", methods=['GET', 'POST'])
    def question():
        if request.method == 'POST':
            question = str(request.form['question'])
            try:
                cs.execute("""INSERT INTO question(libelle) VALUES (%s);""", (question,))
                id = cs.lastrowid
                return redirect("/question/" + str(id), code=302)
            except MySQLdb.Error, e:
                try:
                    print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                except IndexError:
                    print "MySQL Error: %s" % str(e)
                return "Could not store the question", 500

        elif request.method == "GET":
            with open("template/add_question.html") as f:
                return f.read(), 200

    @app.route("/question/<id>", methods=['GET'])
    def a_question(id):
        try:
            id = str(id)
            cs.execute("""SELECT libelle FROM question WHERE id = (%s);""", (id,))
            for row in cs:
                question = row[0]
            return question, 200
        except MySQLdb.Error, e:
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            except IndexError:
                print "MySQL Error: %s" % str(e)
            return "Could not get the question", 500

    @app.route("/question_non_traite", methods=['GET'])
    def question_non_traite():
        pass

    if __name__ == "__main__":
        app.run()
