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
            promotes += tree.insert(elem, "")[1]
            print(promotes)
        else:
            promotes += tree.insert(elem, "")[2]
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
    for i in range(x):
        print("i = " + str(i + 1) + ", n = " + str(len(arrays[i])) + ":")
        print("Cost in ordered array: " + str(f1(arrays[i], q)))
        print("Cost in reversed array: " + str(f2(arrays[i], q)))
        print("Cost in random array: " + str(do_20(arrays[i], 3, q)))
        print("Cost in random switched adjacent array: " + str(do_20(arrays[i], 4, q)))

if __name__ == "__main__":
    arrays = [[] for i in range(10)]
    for i in range(10):
        n = 111 * (2 ** (i + 1))
        for j in range(n):
            arrays[i].append(j)
    for i in range(3):
        print("Question " + str(i + 1))
        do_question(i + 1, arrays)
