#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread
from requests import Request, Session
import json
from time import sleep

import MySQLdb
from flask import Flask, request, redirect, Response

from systeme.expertSystem import Inference
from systeme.rule import rules
from systeme.point import Point


class Traitement_question_thread(Thread):

    def __init__(self, db):
        Thread.__init__(self)
        self.alive = False
        self.db = db

    def run(self):
        self.alive = True

        with Session() as session:
            while(self.alive):
                url = "http://127.0.0.1:5000/question_non_traite"

                header = {"Accept": "application / json",
                          "Content-Type": "application/json;charset=utf-8"
                          }

                # Prepaation of the request
                req = Request("GET", url, data="", headers=header)
                prepped = req.prepare()

                resp = session.send(prepped)

                if resp.status_code != 200:
                    continue
                else:
                    quest = json.loads(resp._content)
                    entry = []
                    for p in json.loads(quest["question"]):
                        entry.append(Point(p["x"], p["y"]))

                    inference = Inference(rules)
                    list_rule = inference.process(entry)

                    la_response = ""
                    for rule in list_rule:
                        la_response += str(rule) + ", "
                    la_response = la_response[0:-2]

                    try:
                        cs = db.cursor()
                        cs.execute("INSERT INTO response (id, libelle) VALUES( " +
                                   str(quest["id"]) + ", \"" + la_response + "\");")

                        cs.execute("UPDATE question SET traite = TRUE WHERE id= " +
                                   str(quest["id"]) + ";")
                        cs.execute("UPDATE question SET id_response = " + str(quest["id"]) + " WHERE id= " +
                                   str(quest["id"]) + ";")

                        db.commit()
                    except MySQLdb.Error, e:
                        try:
                            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                        except IndexError, i:
                            print "MySQL Error: %s" % str(i)
                        return "Could not store the question", 500


host = "127.0.0.1"  # poridore.mysql.pythonanywhere-services.com
user = "root"
pwd = ""
db = "wb"

db = MySQLdb.connect(host, user, pwd, db)

app = Flask(__name__)


@app.route("/response/<id>", methods=['GET'])
def question(id):
    try:
        cs = db.cursor()
        cs.execute(" SELECT  libelle FROM response WHERE id = " + str(id))

        for row in cs:
            libelle = row[0]

            return libelle, 200

        return "Pas de reponse pour l'instant", 404

    except MySQLdb.Error, e:
        try:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError, i:
            print "MySQL Error: %s" % str(i)
        return "Could not get the question", 500


if __name__ == "__main__":
    traitement_question_thread = Traitement_question_thread(db)
    traitement_question_thread.start()
    app.run(host="0.0.0.0", port=5001)
    traitement_question_thread.alive = False
    db.close()
