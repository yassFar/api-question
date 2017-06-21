from math import degrees, sqrt, acos


def getAngle(a, b, c):
    vectorBA = a - b
    vectorBC = c - b
    try:
        dot_product = (
            (vectorBA[0] * vectorBC[0] + vectorBA[1] * vectorBC[1]) /
            (sqrt(vectorBA[0] * vectorBA[0] + vectorBA[1] * vectorBA[1])
             * sqrt(vectorBC[0] * vectorBC[0] + vectorBC[1] * vectorBC[1]))
        )
    except ZeroDivisionError:
        raise ZeroDivisionError

    try:
        radian = acos(dot_product)
    # if dot_product == 1.0
    except Exception:
        radian = 0

    angle = degrees(radian)
    return angle


def getAngleVector(vector1, vector2):
    try:
        dot_product = (
            (vector1[0] * vector2[0] + vector1[1] * vector2[1]) /
            (sqrt(vector1[0] * vector1[0] + vector1[1] * vector1[1])
             * sqrt(vector2[0] * vector2[0] + vector2[1] * vector2[1]))
        )
    except ZeroDivisionError:
        raise ZeroDivisionError

    try:
        radian = acos(dot_product)
    # if dot_product == 1.0
    except Exception:
        radian = 0

    angle = degrees(radian)
    return angle


def getAllAngle(entry):
    resultat = []
    for i in range(len(entry)):
        point1 = entry[i - 1]
        point2 = entry[i]
        if i == len(entry) - 1:
            point3 = entry[0]
        else:
            point3 = entry[i + 1]
        resultat.append(getAngle(point1, point2, point3))

    return resultat


def getAllLengthSide(entry):
    resultat = []

    for i in range(len(entry)):
        point1 = entry[i]
        if i == len(entry) - 1:
            point2 = entry[0]
        else:
            point2 = entry[i + 1]

        resultat.append(distance2Point(point1, point2))
    return resultat


def distance2Point(a, b):
    return round(sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2), 4)
