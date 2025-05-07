from collections import deque
from itertools import chain, combinations
 
# Constants to represent the indices of the treatment and outcome variables
TREATMENT = 0
OUTCOME = 1
 
class Variable:
    def __init__(self, row):
        self._parent = []           # List of parent nodes
        self._children = []         # List of child nodes
        self._descendant_of = []    # List of ancestors/descendants of this variable
        self._row = row             # Row index in adjacency matrix
 
    def add_children(self, child):
        if child not in self._children:
            self._children.append(child)
        child.add_parent(self)
        child.add_descendant(self)
        for parent in self._parent:
            child.add_descendant(parent)  # All ancestors of self are also ancestors of child
 
    def add_parent(self, parent):
        if parent not in self._parent:
            self._parent.append(parent)
 
    def add_descendant(self, ancestor):
        if ancestor not in self._descendant_of:
            self._descendant_of.append(ancestor)
 
    def get_parents(self):
        return self._parent
 
    def get_children(self):
        return self._children
 
    def get_descendant(self):
        return self._descendant_of
 
    def get_row(self):
        return self._row
 
# Find all undirected paths from start to target
# Used to identify all potential paths, including back-door paths
def bfs_all_paths_bidirectional(start, target):
    paths = []
    queue = deque([[start]])
 
    while queue:
        path = queue.popleft()
        current = path[-1]
 
        if current == target:
            paths.append(path)
            continue
 
        # Move bidirectionally: both to parents and children
        neighbors = current.get_children() + current.get_parents()
        for neighbor in neighbors:
            if neighbor not in path:
                queue.append(path + [neighbor])
    return paths
 
# Generate all subsets (powerset) of a given iterable
def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))
 
# Determine whether a node is a collider in a three-node sequence
def is_collider(prev, curr, next_):
    return prev in curr.get_parents() and next_ in curr.get_parents()
 
# Determine whether a path is blocked given a conditioning set
def path_blocked(path, conditioning_set):
    for i in range(1, len(path) - 1):
        prev = path[i - 1]
        curr = path[i]
        next_ = path[i + 1]
 
        if is_collider(prev, curr, next_):
            # Path through collider is only open if collider or its descendant is conditioned on
            if not (curr in conditioning_set or any(desc in conditioning_set for desc in curr.get_children())):
                return True  # Blocked
        else:
            # Path through non-collider is blocked if the variable is conditioned on
            if curr in conditioning_set:
                return True
    return False  # No blocking condition met
 
# Main function to analyze the DAG and determine valid adjustment sets
def find_adjustment_sets():
    # Adjacency matrix representing the DAG
    matrix = [
        #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 T
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1 Y
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 3
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 4
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 5
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 9
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 10
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 12
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 13
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 14
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 15
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 16
    ]
 
    # Create variables based on the matrix indices
    treatment = Variable(TREATMENT)
    outcome = Variable(OUTCOME)
    covariables = [Variable(i) for i in range(2, len(matrix))]
    variables = [treatment, outcome] + covariables
 
    # Add edges (children and parents) from adjacency matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                variables[i].add_children(variables[j])
 
    # Find all paths between treatment and outcome
    all_paths = bfs_all_paths_bidirectional(treatment, outcome)
 
    # Filter out direct front-door paths (i.e., treatment -> ... -> outcome)
    backdoor_paths = [
        path for path in all_paths
        if path[0] != treatment or path[1] in treatment.get_parents()
    ]
 
    valid_sets = []
    for subset in powerset(covariables):
        # Exclude conditioning on descendants of treatment
        if any(TREATMENT in [desc.get_row() for desc in var.get_descendant()] for var in subset):
            continue
        # Keep only sets that block all back-door paths
        if all(path_blocked(path, subset) for path in backdoor_paths):
            valid_sets.append(subset)
 
    # Get the smallest valid sets (minimal adjustment sets)
    minimal_sets = []
    if valid_sets:
        min_len = min(len(s) for s in valid_sets)
        minimal_sets = [s for s in valid_sets if len(s) == min_len]
 
    print("Minimal adjustment set:")
    for s in minimal_sets:
        print(sorted(v.get_row() for v in s))
 
if __name__ == "__main__":
    find_adjustment_sets()
