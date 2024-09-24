from gsorter.comparison import Comparison
from gsorter.item import Item
from abc import ABC, abstractmethod
from typing import Callable
from pydantic import BaseModel, Field
import os
import itertools

class Group(BaseModel):
    name: str = 'group'
    groups: list['Group'] = Field(default_factory=lambda:[])
    comparisons: dict[str, Comparison] = Field(default_factory=lambda:{})
    is_current_group: bool = False
    current_comparison: int = None

    # utility functions for tree operations
    def on_leaf_groups(self, op, **kwargs):
        if len(self.groups) == 0:
            op(self, **kwargs)
        else:
            for group in self.groups:
                group.on_leaf_groups(op, **kwargs)
    
    def on_items(self, op, **kwargs):
        for comparison in self.comparisons.values():
            for item in comparison.data:
                op(item, **kwargs)

    def on_leaf_items(self, op, **kwargs):
        self.on_leaf_groups(lambda g: g.on_items(op, **kwargs), **kwargs)

class Grouper(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def __call__(self, i, **kwargs) -> Group:
        pass

class _FromItems(Grouper):
    """Converts multiple items into a single group using the items' comparison_ids."""
    def __call__(self, i : list[Item], **kwargs) -> Group:
        group = Group(
            name = kwargs.get('name', None)
        )
        for item in i:
            if not item.comparison_id in group.comparisons:
                group.comparisons[item.comparison_id] = Comparison(comparison_id=item.comparison_id, data=[])
            group.comparisons[item.comparison_id].data.append(item)
        return group

class MultiFile(Grouper):
    """Converts multiple files into a single group.
    Calls a file_fn over each file_path; file_fns return a list of Item.
    All items produced this way are concatenated into a single group, using _FromItems.
    """
    def __init__(self,
        file_fn : Callable[str, list[Item]],
        **kwargs):
        self.file_fn = file_fn
        self.name = kwargs.get('name', 'multi_file_group')

    def __call__(self, i : list[str], **kwargs) -> Group:
        items = []
        for path in i:
            items.extend(self.file_fn(path))
        g = _FromItems()

        return g(items, name=self.name, **kwargs)

#class Alphabetize(Grouper):
#    """Takes one existing support vertex (only connected to items)
#    group and splits it into sub-groups by starting character of comparison ID."""

#class Split(Grouper):
#   """Takes one existing support vertex group and splits it into n sub-groups."""

#class Mirror(Grouper):
#    """Creates group structures that mirror a filesystem structure.
#    Takes a list"""
#    def __call__(self,
#        l : list[str],
#        file_fn : Callable[str, list[Item]],
#        **kwargs) -> Group:
#        for basepath in l:
#            for path, dirnames, files in os.walk():
#                with files as f:
#
## Applies other Groupers recursively over list arguments
#class Sequential(Grouper):
#    def __call__(self, l : list[Grouper], **kwargs):
#        pass