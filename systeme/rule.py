#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mathUtil import getAllAngle, getAllLengthSide, distance2Point, getAngleVector


class Rule():
    def __init__(self, conditions, libelle, **args):
        self.conditions = conditions
        self.libelle = libelle

        self.tested = False

        if "need" in args:
            self.need = args["need"]
        else:
            self.need = None

        if "stop" in args:
            self.stop = args["stop"]
        else:
            self.stop = False

    def test(self, entry):
        resultat = False
        for nameRule, conditionsTest in self.conditions.iteritems():
            try:
                if nameRule == "side":
                    valueFound = len(entry)
                elif nameRule == "nbr_angle_droit":
                    valueFound = 0
                    for angle in getAllAngle(entry):
                        if angle == 90:
                            valueFound += 1
                elif nameRule == "same_length_side":
                    valueFound = 0
                    allLengthSide = getAllLengthSide(entry)
                    for lengthSide in allLengthSide:
                        recurance = allLengthSide.count(lengthSide)
                        if(recurance != 1):
                            valueFound = recurance
                            break
                elif nameRule == "any_angle":
                    allAngle = getAllAngle(entry)
                    valueFound = 0
                    for angle in allAngle:
                        if angle > valueFound:
                            valueFound = angle
                elif nameRule == "all_angle":
                    valueWanted = conditionsTest[1]
                    boolTest = conditionsTest[0]
                    for angle in getAllAngle(entry):
                        if boolTest == "=<":
                            if(angle > valueWanted):
                                return False
                    return True
                elif nameRule == "sum_all_angle":
                    valueFound = sum(getAllAngle(entry))
                elif nameRule == "inscriptible":
                    valueFound = False
                    diag1 = distance2Point(entry[0], entry[2])
                    diag2 = distance2Point(entry[1], entry[3])
                    a = float(diag1) / float(diag2)

                    ba = float((distance2Point(entry[0], entry[3]) +
                                distance2Point(entry[2], entry[1])))
                    bb = float((distance2Point(entry[0], entry[1]) +
                                distance2Point(entry[2], entry[3])))

                    b = ba / bb
                    valueFound = a == b
                elif nameRule == "trapeze":
                    valueFound = False

                    vectorBA = entry[1] - entry[0]
                    vectorCD = entry[2] - entry[3]
                    angle = getAngleVector(vectorBA, vectorCD)
                    if angle == 0 or angle == 180:
                        valueFound = True
                    else:
                        vectorBC = entry[2] - entry[1]
                        vectorAD = entry[3] - entry[0]
                        angle = getAngleVector(vectorBC, vectorAD)
                        if angle == 0 or angle == 180:
                            valueFound = True

                else:
                    return False
                boolTest = conditionsTest[0]
                valueWanted = conditionsTest[1]

                if(boolTest == "="):
                    return valueFound == valueWanted
                elif(boolTest == ">"):
                    return valueFound > valueWanted
                elif(boolTest == "<"):
                    return valueFound < valueWanted
                else:
                    return False
            except KeyError, e:
                raise e
                return False

        if resultat is True:
            return self

    def __str__(self):
        return self.libelle

    def check_need(self, rules_to_test):
        if self.need is None:
            return True

        for rule_needed in self.need:
            rule_needed_found = False
            for rule in rules_to_test:
                if rule_needed == rule:
                    rule_needed_found = True

            if not rule_needed_found:
                return False

        return True


rules = {
    "triangle": Rule({"side": ["=", 3]}, "triangle"),
    "quadrilatere": Rule({"side": ["=", 4]}, "quadrilatere")


}


# triangle
dict_rule_triangle = {
    "triangle_rectangle": Rule({"nbr_angle_droit": ["=", 1]}, "rectangle",
                               need=[rules["triangle"]]),
    "triangle_isocele": Rule({"same_length_side": ["=", 2]}, "isocele",
                             need=[rules["triangle"]]),
    "triangle_equlaterale": Rule({"same_length_side": ["=", 3]}, "equlaterale",
                                 need=[rules["triangle"]])
}
rules.update(dict_rule_triangle)

# quadrilatere
dict_rule_quatrilatere = {
    "quadrilatere_concave": Rule({"any_angle": [">", 90]}, "concave", need=[rules["quadrilatere"]]),
    "quadrilatere_convexe": Rule({"all_angle": ["=<", 90]}, "convexe", need=[rules["quadrilatere"]]),
    "quadrilatere_croise": Rule({"sum_all_angle": ["<", 360]}, "croise", need=[rules["quadrilatere"]], stop=True)
}
rules.update(dict_rule_quatrilatere)

# Inscriptible
inscriptible = Rule({"inscriptible": ["=", True]}, "inscriptible", need=[
    rules["quadrilatere_convexe"]])
rules.update({"quadrilatere_inscriptible": inscriptible})

# Trapeze
trapeze = Rule({"trapeze": ["=", True]}, "trapeze", need=[
    rules["quadrilatere_convexe"]])
rules.update({"quadrilatere_trapeze": trapeze})
