#id1: 322520255
#name1: Itamar Ben Nun
#username1: itamarbennun
#id2: 316061787
#name2: Tal Malka
#username2: talmalka2


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields.

	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 1 # Todo: figure out what should be the initial value


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None #Todo: not clear if the indication of virtual node is Node that is None or Node that has key as None

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = None
		self.min = None
		self.max = None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		curr, edges = self.search_helper(key)
		return None,edges if curr.key is None else curr, edges

		# def search_helper(node, key_name, edges):
		# 	if node is None:
		# 		return None, edges
		# 	if node.key == key_name:
		# 		return node, edges
		# 	elif node.key < key_name:
		# 		return search_helper(node.right, key_name, edges+1)
		# 	else:
		# 		return search_helper(node.left, key_name, edges+1)
		# return search_helper(self.root, key, 1)


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or the virtual Node if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search_helper(self, key):
		curr = self.root, edges = 1
		while curr.key is not None:
			if curr.key == key:
				return curr, edges
			elif curr.key < key:
				curr = curr.right
				edges += 1
			else:
				curr = curr.left
				edges += 1
		return curr, edges  # Todo: what should be the edges value if the node is None

	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		curr = self.max, edges = 1
		while curr.key is not None:
			if curr.key == key:
				return curr, edges
			elif curr.key < key:
				break
			else:
				curr = self.predecessor(curr)
				edges += 1
		return None, edges # Todo: what should be the edges value if the node is None

		# def search_helper(node, key_name, edges):
		# 	if node is None:
		# 		return None, edges
		# 	if node.key < key_name:
		# 		return None, edges
		# 	if node.key == key_name:
		# 		return node, edges
		# 	else:
		# 		return search_helper(self.predecessor(node), key_name, edges + 1)
		# return search_helper(self.max, key, 1)


	# add func documentation for predecessor
	"""returns the predecessor of a given node
	@type node: AVLNode
	@param node: the node whose predecessor is to be found
	@rtype: AVLNode
	@returns: the predecessor of the given node
	"""
	def predecessor(self, node):
		if node.left is not None:
			curr= node.left
			while curr.right is not None:
				curr = curr.right
			return curr
		curr = node
		while curr.parent is not None and curr.parent.left == curr:
			curr = curr.parent
		return curr.parent


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		where_to_insert, edges = self.search_helper(key)
		where_to_insert.key = key
		where_to_insert.value = val
		left_node= AVLNode(None, None)
		left_node.parent = where_to_insert
		right_node = AVLNode(None, None)
		right_node.parent = where_to_insert
		where_to_insert.left = left_node
		where_to_insert.right = right_node
		where_to_insert.height = 0
		if self.max is None or key > self.max.key:
			self.max = where_to_insert
		if self.min is None or key < self.min.key:
			self.min = where_to_insert

		curr = where_to_insert.parent
		while curr is not None:
			bf = curr.right.height - curr.left.height
			if bf == 0:
				break
			elif bf == 1 or bf == -1:
				curr.height += 1
				curr = curr.parent
			else: # you are not balanced, bf is +- 2, fix yourself and only then move up
				if bf == -2:
					right_child_bf = curr.right.right.height - curr.right.left.height
					if right_child_bf == -1:
						# rotate left
					else: # right_child_bf == 1
						# rotate right between two other childs and then left rotate
				else: # bf == 2
					left_child_bf = curr.left.right.height - curr.left.left.height
					if left_child_bf == 1:
						# rotate right
					else:
						# rotate left between two other childs and then right rotate
				curr.height += 1 # Todo: check if needed
				curr = curr.parent


		#Todo: need to update the size of the nodes on the path from the root to the new node
		return where_to_insert, edges, 0 #case A: no rotation needed, parent is balanced


	def rotate_left(self, node):
		child = node.right
		node.right = child.left
		child.left = node
		child.height = 1 + max(child.left.height, child.right.height)
		node.height = 1 + max(node.left.height, node.right.height)
		return child


	def rotate_right(self, node):
		child = node.left
		node.left = child.right
		child.right = node
		child.height = 1 + max(child.left.height, child.right.height)
		node.height = 1 + max(node.left.height, node.right.height)
		return child

	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return


	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None, None


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		in_order = []
		def in_order_helper(node):
			if node is not None:
				in_order_helper(node.left)
				in_order.append((node.key, node.value))
				in_order_helper(node.right)
		return in_order_helper(self.root)


	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return self.max

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return 0 if self.root is None else self.root.size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root
