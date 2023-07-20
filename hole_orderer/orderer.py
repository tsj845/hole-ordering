from typing import Dict, List, Literal, Tuple

from .circle import Circle, Order

def _row_sort_key(item: Circle) -> int:
    return item.row

def _col_sort_key(item: Circle) -> int:
    return item.col

def order_circles(clist: List[Circle], order: Order) -> List[Circle]:
    """
    orders the list in place, then returns the list
    """

    if len(clist) != len(order):
        raise ValueError("length of circle list must equal length of order list")
    
    def _order_sort_key(item: Circle) -> int:
        return order.index(item.coords())
    
    clist.sort(key=_order_sort_key)

    return clist

def gen_order(clist: List[Circle], style: Literal["sweeplr","sweepud","spiralin","spiralout"]) -> Order:
    """
    creates and Order for the given list of circles in a pre-defined pattern
    """
    
    ret: Order = []
    tmp: List[Order] = []
    if style in ("sweeplr", "sweepud"):
        if style == "sweeplr":
            # sort with row as primary key, col as secondary
            clist.sort(key=_col_sort_key)
            clist.sort(key=_row_sort_key)
            # keeps track of the row of the previous circle
            lasty: int = None
            # loop over circles
            for c in clist:
                # if row is different, add a new list to tmp and update lasty
                if c.row != lasty:
                    lasty = c.row
                    tmp.append([])
                # add circle to the last sublist of tmp
                tmp[-1].append(c.coords())
        else:
            # sort with col as primary key, row as secondary
            clist.sort(key=_row_sort_key)
            clist.sort(key=_col_sort_key)
            # keeps track of the col of the previous circle
            lastx: int = None
            # loop over circles
            for c in clist:
                # if row is different, add a new list to tmp and update lasty
                if c.col != lastx:
                    lastx = c.col
                    tmp.append([])
                # add circle to the last sublist of tmp
                tmp[-1].append(c.coords())
        rev: bool = True
        for l in tmp:
            rev = not rev
            if rev:
                # reverse so that the order goes back and forth
                l.reverse()
            ret.extend(l)
    else:
        clist.sort(key=_col_sort_key)
        clist.sort(key=_row_sort_key)

        mapping: Dict[Tuple[int, int], bool] = {}

        for c in clist:
            mapping[c.coords()] = True
        
        targ: int = 1
        loop: int = 0
        
        # makes the spiral
        while True in mapping.values():
            if loop == 2:
                loop = 0
                # shifts the spiral between even and odd numbers every time it reaches the bottom left diagonal
                targ -= 1

            tmp.append([])
            
            for c in clist:
                co = c.coords()
                if c.row == targ and mapping[co]:
                    mapping[co] = False
                    tmp[-1].append(co)
            
            targ = tmp[-1][-1][0]

            tmp.append([])
            
            for c in clist:
                co = c.coords()
                if c.col == targ and mapping[co]:
                    mapping[co] = False
                    tmp[-1].append(co)
            
            if len(tmp[-1]) == 0:
                for c in clist:
                    if mapping[c.coords()]:
                        targ = c.row
                        break
                if loop == 1:
                    targ += 1
            else:
                targ = tmp[-1][-1][1]

            loop += 1

            if loop > 4:
                break

            clist.reverse()
        
        for l in tmp:
            ret.extend(l)

        if style == "spiralout":
            # reverse order so that the spiral moves out instead of in
            ret.reverse()
        elif style != "spiralin":
            raise ValueError("Invalid Style")
    
    return ret