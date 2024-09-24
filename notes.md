# GenericSorter
GenericSorter is designed to be a generic interface for hand-annotation and
sorting tasks that can be customized for various data processing uses.

# Conceptual model
Project > Groups > Rows > Items > Fields
Each project represents a set of groups, the data for which will be saved and
exported together. It is the "save-unit".
Each group represents a set of items that you want the annotator to handle in batches.
	Only one group may be open at a time.
	A single add_data call creates a single group.
Each row represents a comparison of items OR a single item to be annotated by hand.
	Only one row may be open at a time.
Each field is a single field that can be either annotated or selected from alternatives.
	Multiple fields may be visible per item.

# Example model specifications
Multifile into one group, each file is to be processed into one or more items
Mirror hierarchy of files

# Interface
- I want to browse through groups through a hierarchical interface, opening up
  an effective 'sub-project' for each one.
- Within each group I want to be able to easily navigate back and forth
  between items and visualize what item I am on using a list interface
- I want to be able to select from alternatives for each field individually and
  for entire elements, as well as annotate fields individually
- I want to be able to define information to be displayed vs. editable
- I want the entire thing to be keyboard navigable ;^)
- I want to be able to define custom row processing actions (e.g. regex sub over an attribute)
- I want to be able to define custom postprocessing
- I want to be able to search over rows by field and either highlight them or
	  perform other operations on them
- I want to be able to define PRESET VALUES for certain fields (in data).
	- And also broadcast forwards or broadcast all (enableable)

# Problems
- Is there even an effective way to display a group-like interface in PyQt?
	- Yep, according to ChatGPT, QTreeView works for this purpose.
- How do I do type annotations?
- Is a single file -> a single group?
	- How do you associate multiple filesystem files w/ a single group?
- What is "FileLike" (project.py 23)?

# TODO
File -> Item
Rows
