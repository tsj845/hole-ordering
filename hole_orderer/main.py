from sys import argv
from typing import List, Tuple

from .extractor import extract_circles, extract_coords_from_file, extract_coords_from_text
from .labeler import label
from .circle import Circle, Order
from .orderer import gen_order, order_circles
from .output import write_dxf_file, write_ord_file

def main():
    """
    example argv's

    python3 runner.py "name.DXF" 1 "order.txt" "dest.DXF"

    python3 runner.py "name.DXF" 3 "1,1\n2,2..." "dest.DXF"

    python3 runner.py "name.DXF" 5 "order.txt" 12 "dest1.DXF" "dest2.DXF"
    
    python3 runner.py "name.DXF" 7 "1,1\n2,2..." 12 "dest1.DXF" "dest2.DXF"

    python3 runner.py "name.DXF" 2 "ord1.txt" "ord2.txt" "dest1.DXF" "dest2.DXF"
    
    python3 runner.py "name.DXF" 4 "1,1\n2,2..." "3,3\n4,4..." "dest1.DXF" "dest2.DXF"
    
    python3 runner.py "name.DXF" 0 "style" "dest.DXF"

    python3 runner.py "genord" "style" "ord_dest.txt"

    """

    assert not (len(argv) < 2), "no args found"

    parts = extract_circles(argv[1])
    label(parts[1])
    clist: List[Circle] = parts[1]

    if argv[2] == "genord":
        order: Order = gen_order(clist, argv[3])
        write_ord_file(argv[-1], order)
        return

    tflag: int = int(argv[2])
    
    order: List[Tuple[int, int]] = None

    p1length: int = None

    if tflag != 0:
        # specifying order in one file
        if tflag & 1:
            # specifying order through command line arg
            if tflag & 2:
                order = extract_coords_from_text(argv[3])
            # specifying order through a file
            elif tflag <= 5:
                order = extract_coords_from_file(argv[3])
            else:
                raise ValueError("Invalid Flag")
            if tflag & 4:
                p1length = int(argv[4])
        # specifying two orders
        else:
            # specifying through files
            if tflag == 2:
                order = extract_coords_from_file(argv[3])
                p1length = len(order)
                order.extend(extract_coords_from_file(argv[4]))
            # specifying through command line
            elif tflag == 4:
                order = extract_coords_from_text(argv[3])
                p1length = len(order)
                order.extend(extract_coords_from_text(argv[4]))
            else:
                raise ValueError("Invalid Flag")
        order_circles(clist, order)
    else:
        style = argv[3]
        if style != "-1":
            order: Order = gen_order(clist, style)
            order_circles(clist, order)
    final: List[List[Circle]] = [clist]
    if p1length != None:
        final = [clist[:p1length], clist[p1length:]]
    
    write_dxf_file(argv[-len(final):], parts[0], final)