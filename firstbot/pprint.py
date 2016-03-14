def pprint_field(field):
    pstr = ""
    for y1 in range(3):
        for y2 in range(3):
            for j in range(3):
                i = (y1*9+y2*3+j)
                pstr += "".join(map(str, field[i*3:(i+1)*3]))
                pstr += "|"
            pstr += "\n"
        pstr += "---+---+---\n"
    return pstr


def pprint(macroboard):
    pstr = ""
    for y in range(3):
        pstr += "".join(("{:2d}{:2d}{:2d}".format(*macroboard[y*3:(y+1)*3])))
        pstr += "\n"
    return pstr
