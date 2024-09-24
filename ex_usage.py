from gsorter.project import ProjectSpec
from gsorter.group import Group
import json

def horse_add_data(files: list[str]) -> Group:
    g = Group() 
    g.name = ' '.join(files)
    g.rows = []
    for j in files:
        with open(j) as f:
            o = json.load(f)
        g.rows.append() 

def test_usage():
    spec = ProjectSpec(
        add_data='')
    sorter = GenericSorter(spec)
    sorter.run()
