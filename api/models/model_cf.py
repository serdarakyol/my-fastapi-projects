from typing import List, Optional
from dataclasses import dataclass

@dataclass
class CFRequest:
    """
    Item: items exist in the cart
    n_item: number of item to recommend
    """
    item: List
    n_item: int

@dataclass
class CFResponse:
    """
    input_item: items exist in the cart
    similar_items: recommendions
    """
    input_item: List
    similar_items: Optional[List]
