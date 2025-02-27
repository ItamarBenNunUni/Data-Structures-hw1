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


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key is not None

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or the virtual Node if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search_helper(self, key): # Time complexity: O(logn)
		curr = self
		edges = 1
		while curr.is_real_node():
			if curr.key == key:
				return curr, edges
			elif curr.key < key:
				curr = curr.right
				if curr.is_real_node():
					edges += 1
			else:
				curr = curr.left
				if curr.is_real_node():
					edges += 1
		return curr, edges

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
		self.tree_size = 0

	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key): # Time complexity: O(logn)
		if key is None:
			return None, 1
		if self.root is None:
			return None, 1
		curr, edges = self.root.search_helper(key)
		if not curr.is_real_node():
			return None, edges
		else:
			return curr, edges

	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key): # Time complexity: O(logn)
		if key is None:
			return None, 1
		if self.root is None:
			return None, 1
		curr, edges = self.finger_search_helper(key)
		if not curr.is_real_node():
			return None, edges
		else:
			return curr, edges

	"""searches for a node in the dictionary corresponding to the key, starting at the max
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or the virtual Node if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search_helper(self, key): # Time complexity: O(logn)
		curr = self.max
		edges = 0
		while curr.parent is not None and curr.parent.key >= key:
			curr = curr.parent
			edges += 1
		x, e = curr.search_helper(key)
		return x, e + edges

	"""returns the predecessor of a given node
	@type node: AVLNode
	@param node: the node whose predecessor is to be found
	@rtype: AVLNode
	@returns: the predecessor of the given node
	"""
	def predecessor(self, node): # Time complexity: O(logn)
		if node.left.is_real_node():
			curr = node.left
			while curr.right.is_real_node():
				curr = curr.right
			return curr
		curr = node
		while curr.parent is not None and curr.parent.left == curr:
			curr = curr.parent
		if curr.parent is not None and curr.parent.right == curr: #first turn left
			return curr.parent
		return None


	"""returns the successor of a given node
	@type node: AVLNode
	@param node: the node whose successor is to be found
	@rtype: AVLNode
	@returns: the successor of the given node
	"""
	def successor(self, node): # Time complexity: O(logn)
		if node.right.is_real_node():
			curr = node.right
			while curr.left.is_real_node():
				curr = curr.left
			return curr
		curr = node
		while curr.parent is not None and curr.parent.right == curr:
			curr = curr.parent
		if curr.parent is not None and curr.parent.left == curr: #first turn right
			return curr.parent
		return None

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
	def insert(self, key, val): # Time complexity: O(logn)
		if key is None:
			return
		self.tree_size += 1
		if self.root is None:
			return self.insert_root(key, val)
		#insertion de-facto + min/max updating
		where_to_insert, edges = self.root.search_helper(key)
		return self.insert_de_facto(where_to_insert, edges, key, val)

	"""Rebalances the AVL tree starting from the given node upwards.

	@type node: AVLNode
	@param node: the node to start rebalancing from
	@rtype: int
	@returns: the number of PROMOTE cases during the AVL rebalancing
	"""
	def rebalance(self, node): # Time complexity: O(logn)
		curr = node
		h = 0 #number of promotes
		while curr is not None:
			right_edge = curr.height - curr.right.height
			left_edge = curr.height - curr.left.height
			if left_edge == 1 and right_edge == 1: #problem is fixed
				break
			elif (left_edge == 1 and right_edge == 0) or (left_edge == 0 and right_edge == 1): #case 1 - both symmetrical options: promote (slide 19)
				curr.height += 1
				h += 1
			elif (left_edge == 2 and right_edge == 0) or (left_edge == 0 and right_edge == 2): #cases 2+3 (slide 22)
				if left_edge == 0: #cases 2+3 - symmetrical option as shown
					child_left_edge = curr.left.height - curr.left.left.height
					child_right_edge = curr.left.height - curr.left.right.height
					if child_left_edge == 1 and child_right_edge == 2: #case 2 - symmetrical option as shown: single rotation to the right (slide 26)
						curr = self.rotate_right(curr)
					elif child_left_edge == 2 and child_right_edge == 1: #case 3 - symmetrical option as shown: double rotation to the left and then right (slide 27)
						curr.left = self.rotate_left(curr.left)
						curr = self.rotate_right(curr)
					elif child_left_edge == 1 and child_right_edge == 1: #special join case - symmetrical option as shown: single rotation to the right
						curr = self.rotate_right(curr)
				elif right_edge == 0: #cases 2+3 - symmetrical option flipped from shown
					child_left_edge = curr.right.height - curr.right.left.height
					child_right_edge = curr.right.height - curr.right.right.height
					if child_left_edge == 2 and child_right_edge == 1: #case 2 - symmetrical option flipped from shown: single rotation to the left
						curr = self.rotate_left(curr)
					elif child_left_edge == 1 and child_right_edge == 2: #case 3 - symmetrical option flipped from shown: double rotation to the right and then left
						curr.right = self.rotate_right(curr.right)
						curr = self.rotate_left(curr)
					elif child_left_edge == 1 and child_right_edge == 1: #special join case - symmetrical option flipped from shown: single rotation to the left
						curr = self.rotate_left(curr)
			curr = curr.parent
		return h

	"""Performs a left rotation on the given node.

	@type node: AVLNode
	@param node: the node to perform the left rotation on
	@rtype: AVLNode
	@returns: the new root of the subtree after the rotation
	"""
	def rotate_left(self, node):
		#declare variables
		x = node
		a = x.left
		y = x.right
		b = y.left
		c = y.right
		x_parent = x.parent
		#re-assigning
		x.right = b
		b.parent = x
		y.left = x
		x.parent = y
		y.parent = x_parent
		#height updating
		x.height = 1 + max(a.height, b.height)
		y.height = 1 + max(x.height, c.height)
		#root edge case
		if x_parent is None:
			self.root = y
		else:
			if x == x_parent.right:
				x_parent.right = y
			if x == x_parent.left:
				x_parent.left = y
		return y

	"""Performs a right rotation on the given node.

	@type node: AVLNode
	@param node: the node to perform the right rotation on
	@rtype: AVLNode
	@returns: the new root of the subtree after the rotation
	"""
	def rotate_right(self, node):
		#declare variables
		y = node
		c = y.right
		x = y.left
		a = x.left
		b = x.right
		y_parent = y.parent
		#re-assigning
		y.left = b
		b.parent = y
		x.right = y
		y.parent = x
		x.parent = y_parent
		#height updating
		y.height = 1 + max(b.height, c.height)
		x.height = 1 + max(a.height, y.height)
		#root edge case
		if y_parent is None:
			self.root = x
		else:
			if y == y_parent.right:
				y_parent.right = x
			if y == y_parent.left:
				y_parent.left = x
		return x

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
	def finger_insert(self, key, val): # Time complexity: O(logn)
		if key is None:
			return
		self.tree_size += 1
		if self.root is None:
			return self.insert_root(key, val)
		#insertion de-facto + min/max updating
		where_to_insert, edges = self.finger_search_helper(key)
		return self.insert_de_facto(where_to_insert, edges, key, val)

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node): # Time complexity: O(logn)
		if node is None:
			return
		#regular BST deletion
		if (node.height == 0 and node.parent is None) or (self.root is None):
			self.root = None
			self.min = None
			self.max = None
			return
		if node.height == 0:#case 1: leaf
			virtual_node = AVLNode(None, None)
			virtual_node.parent = node.parent
			if node == node.parent.right:
				node.parent.right = virtual_node
			if node == node.parent.left:
				node.parent.left = virtual_node
		elif node.left.is_real_node() and node.right.is_real_node():#case 3: two children
			succ = self.successor(node)
			key, value = succ.key, succ.value
			self.delete(succ)
			node.key, node.value = key, value
		else:#case 2: one child
			if node.parent is not None:
				if node == node.parent.left:
					if node.left.is_real_node():
						node.parent.left = node.left
						node.left.parent = node.parent
					else:
						node.parent.left = node.right
						node.right.parent = node.parent
				if node == node.parent.right:
					if node.left.is_real_node():
						node.parent.right = node.left
						node.left.parent = node.parent
					else:
						node.parent.right = node.right
						node.right.parent = node.parent
			else:#delete root
				if node.left.is_real_node():
					self.root = node.left
					node.left.parent = None
				else:
					self.root = node.right
					node.right.parent = None
		#rebalance
		curr = node.parent
		while curr is not None:
			right_edge = curr.height - curr.right.height
			left_edge = curr.height - curr.left.height
			bf = abs(right_edge - left_edge)
			if bf <= 1 and right_edge != 2 and left_edge != 2: #problem is fixed
				break
			if right_edge == 2 and left_edge == 2: #case 1
				curr.height -= 1
			elif left_edge == 3 and right_edge == 1: #cases 2+3+4
				child = curr.right
				child_left_edge = child.height - child.left.height
				child_right_edge = child.height - child.right.height
				if (child_left_edge == 1 and child_right_edge == 1) or (child_left_edge == 2 and child_right_edge == 1):
					curr = self.rotate_left(curr)
				elif child_left_edge == 1 and child_right_edge == 2:
					curr.right = self.rotate_right(curr.right)
					curr = self.rotate_left(curr)
			elif left_edge == 1 and right_edge == 3: #cases 2+3+4 - flipped
				child = curr.left
				child_left_edge = child.height - child.left.height
				child_right_edge = child.height - child.right.height
				if (child_left_edge == 1 and child_right_edge == 1) or (child_left_edge == 1 and child_right_edge == 2):
					curr = self.rotate_right(curr)
				elif child_left_edge == 2 and child_right_edge == 1:
					curr.left = self.rotate_left(curr.left)
					curr = self.rotate_right(curr)
			curr = curr.parent
		#update min/max
		self.set_min()
		self.set_max()
		self.tree_size -= 1

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
	def join(self, tree2, key, val): # Time complexity: O(logn)
		if tree2 is None:
			self.insert(key, val)
			return
		if key is None:
			return
		if self.root is None and tree2.root is None:
			self.insert(key, val)
			return
		if self.root is None:
			tree2.insert(key, val)
			self.root = tree2.root
			self.min = tree2.min
			self.max = tree2.max
			self.tree_size = tree2.tree_size
			return
		if tree2.root is None:
			self.insert(key, val)
			return
		new_size = self.tree_size + tree2.tree_size + 1
		#figure out bigger higher
		bigger = self.root if self.root.key > key else tree2.root
		smaller = self.root if self.root.key < key else tree2.root
		higher = self.root if self.root.height > tree2.root.height else tree2.root
		lower = self.root if self.root.height < tree2.root.height else tree2.root
		k = lower.height
		#find k-most height
		new_node = AVLNode(key, val)
		new_node.height = k + 1
		curr = higher
		if higher == bigger:
			while curr.height > k:
				curr = curr.left
			if curr.parent is not None:
				curr.parent.left = new_node
			new_node.right = curr
			new_node.left = smaller
			new_node.parent = curr.parent
			curr.parent = new_node
			smaller.parent = new_node
		else:#higher = smaller
			while curr.height > k:
				curr = curr.right
			if curr.parent is not None:
				curr.parent.right = new_node
			new_node.right = bigger
			new_node.left = curr
			new_node.parent = curr.parent
			curr.parent = new_node
			bigger.parent = new_node
		#rebalance
		self.rebalance(new_node)
		#root updating
		curr = new_node
		while curr.parent is not None:
			curr = curr.parent
		self.root = curr
		# min-max assign
		self.set_min()
		self.set_max()
		self.tree_size = new_size

	"""Sets the minimum node in the AVL tree."""
	def set_min(self): # Time complexity: O(logn)
		curr = self.root
		while curr is not None and curr.left.is_real_node():
			curr = curr.left
		self.min = curr

	"""Sets the maximum node in the AVL tree."""
	def set_max(self): # Time complexity: O(logn)
		curr = self.root
		while curr is not None and curr.right.is_real_node():
			curr = curr.right
		self.max = curr

	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node): # Time complexity: O(logn)
		if node is None:
			return
		smaller = AVLTree()
		bigger = AVLTree()
		if node.left.is_real_node():
			smaller.root = node.left
			smaller.root.parent = None
		else:
			smaller.root = None
		if node.right.is_real_node():
			bigger.root = node.right
			bigger.root.parent = None
		else:
			bigger.root = None
		#start going up
		curr = node
		while curr.parent is not None:
			if curr == curr.parent.right:
				left_son_of_parent = AVLTree()
				left_son_of_parent.root = curr.parent.left
				left_son_of_parent.root.parent = None
				smaller.join(left_son_of_parent, curr.parent.key, curr.parent.value)
			if curr == curr.parent.left:
				right_son_of_parent = AVLTree()
				right_son_of_parent.root = curr.parent.right
				right_son_of_parent.root.parent = None
				bigger.join(right_son_of_parent, curr.parent.key, curr.parent.value)
			curr = curr.parent
		#return
		smaller.set_min()
		smaller.set_max()
		bigger.set_min()
		bigger.set_max()
		return smaller, bigger

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self): # Time complexity: O(n)
		in_order = []
		def in_order_helper(node):
			if node.is_real_node():
				in_order_helper(node.left)
				in_order.append((node.key, node.value))
				in_order_helper(node.right)
		in_order_helper(self.root)
		return in_order

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
	def size(self): # Time complexity: O(n)
		return self.tree_size

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root

	"""Inserts a new root node into the AVL tree with the given key and value.

	@type key: int
	@param key: key of the new root node
	@type val: string
	@param val: value of the new root node
	@rtype: (AVLNode, int, int)
	@returns: a 3-tuple (x, e, h) where x is the new root node,
	e is the number of edges (always 1 for root insertion),
	and h is the number of PROMOTE cases during the AVL rebalancing (always 0 for root insertion)
	"""
	def insert_root(self, key, val):
		self.root = AVLNode(key, val)
		self.root.height = 0
		self.max = self.root
		self.min = self.root
		virtual_left = AVLNode(None, None)
		virtual_left.parent = self.root
		virtual_right = AVLNode(None, None)
		virtual_right.parent = self.root
		self.root.left = virtual_left
		self.root.right = virtual_right
		return self.root, 1, 0

	"""Inserts a new node into the AVL tree at the specified location.

	@type where_to_insert: AVLNode
	@param where_to_insert: the node where the new node should be inserted
	@type edges: int
	@param edges: the number of edges on the path to the insertion point
	@type key: int
	@param key: the key of the new node
	@type val: string
	@param val: the value of the new node
	@rtype: (AVLNode, int, int)
	@returns: a 3-tuple (x, e, h) where x is the new node,
	e is the number of edges on the path to the new node,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert_de_facto(self, where_to_insert, edges, key, val): # Time complexity: O(logn)
		where_to_insert.key = key
		where_to_insert.value = val
		left_node = AVLNode(None, None)
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
		#promoting and balancing
		h = self.rebalance(where_to_insert.parent)
		#return
		return where_to_insert, edges, h
