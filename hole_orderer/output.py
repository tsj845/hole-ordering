from typing import List, Tuple
from .circle import Circle, Order


def write_dxf_file(outpaths: List[str], parts: Tuple[str, str, str], circles: List[List[Circle]]) -> None:
    """
    writes one or more files in dxf format

    almost all arguments to this function can be obtained from other functions in this package

    "outpaths" is a list of output files

    "parts" is the first item of the tuple obtained from "extractor.extract_circles" and contains the content before, within, and after the "ENTITIES" section

    "circles" is a nested list of circles, this must have the same length as "outpaths"

    each output group within "circles" will be written in the order provided, it is expected that the order given is the desired order for the output
    """

    # check that there are as many output destinations as there are seperate outputs
    if len(outpaths) != len(circles):
        raise ValueError("there must be as many output paths as there are output groups")
    
    # loop over output groups
    for i in range(len(circles)):
        clist: List[Circle] = circles[i]

        # build of the content of the entities section
        build: str = "  0\n"

        # add each circle def
        for c in clist:
            build += f"CIRCLE{c.text}\n"
        
        # full file content to be written
        finaltext: str = f"{parts[0]}ENTITIES\n{build}ENDSEC{parts[2]}"

        # write file
        with open(outpaths[i], mode="w") as f:
            f.truncate()
            f.write(finaltext)

def write_ord_file(outpath: str, order: Order) -> None:
    """
    writes an order to a file
    """

    # file content to be written
    writstr: str = ""

    # convert the order to text
    for c in order:
        writstr += f"{c[0]},{c[1]}\n"

    # write file
    with open(outpath, mode="w") as f:
        f.truncate()
        f.write(writstr)