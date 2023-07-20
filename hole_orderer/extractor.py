from typing import List, Tuple

from .circle import Circle, Order

_COORDPRECISION: int = 0

def extract_circles(inpath: str) -> Tuple[Tuple[str, str, str], List[Circle]]:
    """
    extracts circles from a file

    **DATA ASSUMPTIONS THAT MUST BE HELD**
    -  there are ONLY circle definitions within the 'ENTITIES' section

    returns:
    ((pre-entity text, entity section contents (missing start and end tags), post-entity text), Circle[])
    """
    
    rawtext: str = None

    # get file contents
    with open(inpath, mode="r") as f:
        rawtext = f.read()
    
    # extract content of the entities section
    text: List[str] = rawtext.split("ENTITIES")
    hold = text[1].split("ENDSEC", 1)
    text[1] = hold[0]
    text.append(hold[1])
    del hold

    retlst: List[Circle] = []

    # loop over every definition of a circle
    for cdef in text[1].split("CIRCLE")[1:]:
        # isolate coords and radius
        datc = cdef.split("AcDbCircle")[1][:-2].strip().splitlines()
        # get coords
        x = round(float(datc[1]), _COORDPRECISION)
        y = round(float(datc[3]), _COORDPRECISION)
        z = round(float(datc[5]), _COORDPRECISION)
        # get radius
        r = round(float(datc[7]), 2)
        # add the circle
        retlst.append(Circle(x, y, z, r, cdef[:-1]))

    return (tuple(text), retlst)

def extract_coords_from_text(coords_text: str) -> Order:
    """
    get coordinates from a newline separated list of x,y values in string form
    """

    # ensure text was supplied
    if coords_text == None:
        raise ValueError("text cannot be none")

    # list of coordinates to return
    retlst = []

    coords_text = coords_text.replace('\\n', '\n')

    # loop over each newline separated item
    for l in coords_text.strip().splitlines():
        # split the numbers apart
        k = l.strip().split(",")
        # convert to int and append to list
        retlst.append((int(k[0]), int(k[1])))
    
    return retlst

def extract_coords_from_file(coords_path: str) -> Order:
    """
    get coordanites from a file with contents conforming to the format for the "extractor.extract_coords_from_text" function's input
    """

    # check that a path was given
    if coords_path == None:
        raise ValueError("path cannot be none")

    # file content
    text: str = None

    # read file
    with open(coords_path, mode="r") as f:
        text = f.read()
    
    # avoid code repetition
    return extract_coords_from_text(text)