from typing import List

from .circle import Circle

def _x_sort_key(item: Circle) -> float:
    return item.x

def _y_sort_key(item: Circle) -> float:
    return item.y

def label(clist: List[Circle]) -> None:
    """
    labels the items of the list in place
    """
    
    clist.sort(key=_y_sort_key)
    rowid: int = 0
    lasty: float = None
    for c in clist:
        if c.y != lasty:
            lasty = c.y
            rowid += 1
        c.row = rowid
    clist.sort(key=_x_sort_key)
    colid: int = 0
    lastx: float = None
    for c in clist:
        if c.x != lastx:
            lastx = c.x
            colid += 1
        c.col = colid