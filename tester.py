import math
from AVLTree import AVLTree
import random

def count_flips(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count

def f1(arr, q):
    if q in [1, 3]:
        return build_AVL(arr, q)
    return count_flips(arr)

def f2(arr, q):
    new_arr = arr[::-1]
    if q in [1, 3]:
        return build_AVL(new_arr, q)
    return count_flips(new_arr)

def f3(arr, q):
    new_arr = []
    for elem in arr:
        new_arr.append(elem)
    random.shuffle(new_arr)
    if q in [1, 3]:
        return build_AVL(new_arr, q)
    return count_flips(new_arr)

def f4(arr, q):
    new_arr = []
    for elem in arr:
        new_arr.append(elem)
    for i in range(len(new_arr) - 1):
        r = random.random()
        if (r < 0.5):
            tmp = new_arr[i]
            new_arr[i] = new_arr[i + 1]
            new_arr[i + 1] = tmp
    if q in [1, 3]:
        return build_AVL(new_arr, q)
    return count_flips(new_arr)

def build_AVL(arr, q):
    tree = AVLTree()
    promotes = 0
    for elem in arr:
        if q == 3:
            promotes += tree.finger_insert(elem, "")[1]
        else:
            promotes += tree.finger_insert(elem, "")[2]
    return promotes

def do_20(arr, x, q):
    avg = 0
    for i in range(20):
        if x == 3:
            avg += f3(arr, q)
        if x == 4:
            avg += f4(arr, q)
    return avg / 20

def do_question(q, arrays):
    x = 10 if q != 2 else 5
    what = ["Cost of balancing", "Number of switches", "Cost of searching"]
    for i in range(x):
        print("i = " + str(i + 1) + ", n = " + str(len(arrays[i])) + ":")
        print(what[q - 1] + " in Ordered/Reversed/Random/Switch Adjacent: ", end=" ")
        orr, rev, rnd, adj = str(f1(arrays[i], q)), str(f2(arrays[i], q)), str(do_20(arrays[i], 3, q)), str(do_20(arrays[i], 4, q))
        print(orr + " " + rev + " " + rnd + " " + adj)


def do_question_naive(q, arrays):
    x = 10 if q != 2 else 5
    what = ["Cost of balancing", "Number of switches", "Cost of searching"]
    for i in range(x):
        print("i = " + str(i + 1) + ", n = " + str(len(arrays[i])) + ":")
        print(what[q - 1] + " in ordered array: " + str(f1(arrays[i], q)))
        print(what[q - 1] + " in reversed array: " + str(f2(arrays[i], q)))
        print(what[q - 1] + " in random array: " + str(do_20(arrays[i], 3, q)))
        print(what[q - 1] + " in random switched adjacent array: " + str(do_20(arrays[i], 4, q)))


def test():
    arrays = [[] for i in range(10)]
    for i in range(10):
        n = 111 * (2 ** (i + 1))
        for j in range(n):
            arrays[i].append(j)
    for i in range(3):
        print("Question " + str(i + 1))
        # do_question(i + 1, arrays)
        do_question_naive(i + 1, arrays)

def finger_test():
    tree = AVLTree()
    test_data = [44, 85, 167, 133]
    for element in test_data:
        tree.finger_insert(element, "")
        print_tree(tree.root)

def print_tree(root, indent="", pointer="Root: "):
	if root is not None:
		print(indent + pointer + str(root.key))

		if root.left or root.right:
			if root.left:
				print_tree(root.left, indent + "    ", "L--- ")
			else:
				print(indent + "    L--- None")

			if root.right:
				print_tree(root.right, indent + "    ", "R--- ")
			else:
				print(indent + "    R--- None")

if __name__ == "__main__":
    # expected results in 3
    # for i in range(10):
    #     sum = 0
    #     n = 111 * (2 ** (i + 1))
    #     for j in range(n):
    #         logi = 0 if j==0 else math.floor(math.log2(j))
    #         sum += logi + 1
    #     print(sum)
    test()
    # finger_test()
