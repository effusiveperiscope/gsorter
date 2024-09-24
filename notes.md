# GSorter
GSorter is a UI/framework written in PyQt5 for local
hand-annotation and hand-sorting tasks. It is primarily focused on picking top1
from alternatives.

# Conceptual model
Data in GSorter is structured in the following hierarchy:

`Project > Groups > Comparisons > Items`

* A *project* is a "save-unit". Each project contains one or more trees of
nameable groups, the data for which will be saved and exported together.
* Each *group* may contain other groups or may
contain a set of *comparisons* that you want the hand-annotator to handle in one go.
	- Only one group may be open at a time.
	- Certain data operations (forward broadcast, all-broadcast) may operate over a single group.
	- Future data operations may rely on groups as units. For example, merges may be performed over groups.
	- An example usage of groups may be to distribute the same project file to all hand-annotators, but instruct each to only work on a subset of groups.
* Each *comparison* represents a collection of one or more items to be compared among each other.
	- Only one comparison may be open at a time.
	- The final objective of the sorter is to produce a single output per comparison.
* *Items* are the smallest unit in this hierarchy, containing the data to be annotated/compared. 
	- In comparison tasks, each item is an alternative to be compared.
	- Items shall be given a "comparison ID" on creation; different items with the same
	comparison ID within the same group will be compared to each other.
	- The most recent updates to item data are timestamped. This allows for
	simple merges to be performed between two project files based on
	modification timestamp.

## Fields
Fields are 'rules' that tell the sorter how to display values from an item's data dictionary; without a defined Field, no data from an associated item key will be displayed.

## Timestamping
GSorter uses `ntplib` to obtain timestamps. These timestamps are not intended to
be exhaustively accurate or as robust as a true CRDT (since NTP allows for some
variation), but should be
 "precise" enough to account for merges between
project files where different groups were handled by different annotators.

# Interface
- I want to bcomparisonse through groups through a hierarchical interface, opening up
  an effective 'sub-project' for each one.
- Within each group I want to be able to easily navigate back and forth
  between items and visualize what item I am on using a list interface
- I want to be able to select from alternatives for each field individually and
  for entire elements, as well as annotate fields individually
- I want to be able to define information to be displayed vs. editable
- I want the entire thing to be keyboard navigable ;^)
- I want to be able to define custom comparison processing actions (e.g. regex sub over an attribute)
- I want to be able to define custom postprocessing
- I want to be able to search over comparisons by field and either highlight them or
	  perform other operations on them
- I want to be able to define PRESET VALUES for certain fields (in data).
	- And also broadcast forwards or broadcast all (enableable)