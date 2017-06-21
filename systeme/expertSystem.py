#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rule import rules
from point import Point


# entry = [Point(0, 0), Point(1, 0), Point(0, 1)] #  triangle rectangle isocele
# entry = [Point(0, 0), Point(2, 0), Point(1, sqrt(3))] # triangle equlaterale
# entry = [Point(0, 0), Point(10, 0), Point(10, 10), Point(7, 2)] # equlaterale concave
# entry = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)] # equlaterale convexe
entry = [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)]  # equlaterale croise


class Inference:
    def __init__(self, rules):
        self.rules = rules

    def process(self, entry):
        resultat = []
        rules_to_test = self.get_rules_to_test(resultat)
        while(len(rules_to_test) != 0):
            # first check to rule that stop the process
            for rule_name in rules_to_test:
                rule = self.rules[rule_name]
                self.rules[rule_name].tested = True
                if(rule.stop):
                    if rule.test(entry):
                        resultat.append(rule)
                        if rule.stop:
                            return resultat

            for rule_name in rules_to_test:
                rule = self.rules[rule_name]
                self.rules[rule_name].tested = True
                if rule.test(entry):
                    resultat.append(rule)
                    if rule.stop:
                        return resultat

            rules_to_test = self.get_rules_to_test(resultat)

        return resultat

    def get_rules_to_test(self, current_true_rules):
        rules_to_test = []
        for name, rule in self.rules.iteritems():
            rule = self.rules[name]
            if rule.tested is False:
                if(rule.check_need(current_true_rules)):
                    rules_to_test.append(name)

        return rules_to_test


if __name__ == "__main__":
    inference = Inference(rules)
    resultat = inference.process(entry)

    print "---------Resultat--------"
    for rule in resultat:
        print rule
