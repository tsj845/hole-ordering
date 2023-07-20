from typing import List, Tuple

Order = List[Tuple[int, int]]

class Circle:
    """
    stores data about a circle
    """
    def __init__(self, x: float, y: float, z: float, r: float, text: str) -> None:
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.r: float = r
        self.text: str = text
        self.row: int = None
        self.col: int = None
    def coords(self) -> Tuple[int, int]:
        return (self.col, self.row)
    def __repr__(self) -> str:
        # return f"Circle {{\n  x: {self.x},\n  y: {self.y},\n  z: {self.z},\n  r: {self.r}" + (f",\n  id: {self.col},{self.row}" if (self.row != None and self.col != None) else "") + "\n}"
        return f"({self.col}, {self.row})"