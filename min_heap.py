# Course: CS261 - Data Structures
# Assignment: 5
# Student: Sileide De Freitas Theriac
# Description: Program contains an implementation of a MinHeap class.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        TODO: Write this implementation
        Method adds a new object to the MinHeap maintaining heap property.
        """
        self.heap.append(node)                          # Add node to the end of array.
        last_elem_idx = self.heap.length() - 1

        while last_elem_idx > 0:                        # Track index.
            if self.heap[last_elem_idx] < self.heap[(last_elem_idx - 1) // 2]:
                # If last node is smaller than parent node, swap them.
                self.heap.swap(last_elem_idx, ((last_elem_idx - 1) // 2))
            last_elem_idx = (last_elem_idx - 1) // 2    # Adjust node index.
        pass

    def get_min(self) -> object:
        """
        TODO: Write this implementation
        Method returns an object with a minimum key without removing it from the heap. If
        the heap is empty, the method raises a MinHeapException.
        """
        if self.is_empty():                     # If the heap is empty, the method raises a MinHeapException.
            raise MinHeapException

        min_val = self.heap.get_at_index(0)     # First node will always be the smallest in a min heap.

        return min_val

    def remove_min(self) -> object:
        """
        TODO: Write this implementation
        Method returns an object with a minimum key and removes it from the heap. If the
        heap is empty, the method raises a MinHeapException.
        """
        if self.is_empty():                             # If heap is empty, raise a MinHeapException.
            raise MinHeapException

        root = self.get_min()                           # Store min value.

        if self.heap.length() == 1:                     # If heap has only one element.
            self.heap.pop()                             # Remove the element and return it.
            return root

        self.heap[0] = self.heap.pop()                  # Make last element the first, then remove last element.

        replacement = 0                                 # Index of root.

        while replacement * 2 +1 <= self.heap.length()-1:

            if (replacement * 2) +2 > self.heap.length()-1:      # Check for out of bounds.
                smaller_child = (replacement * 2) +1
            else:
                if self.heap[(replacement * 2) +1] <= self.heap[(replacement * 2) +2]:      # If left child is smaller.
                    smaller_child = (replacement * 2) +1
                else:
                    smaller_child = (replacement * 2) +2          # If right child is smaller.
            if self.heap[replacement] > self.heap[smaller_child]:       # Compare value between replacement and child.
                self.heap.swap(replacement, smaller_child)        # Swap elements if replacement is larger.
            replacement = smaller_child                           # Adjust replacement new index.

        return root

    def build_heap(self, da: DynamicArray) -> None:
        """
        TODO: Write this implementation
        Method receives a dynamic array with objects in any order and builds a proper
        MinHeap from them. Current content of the MinHeap is lost. Runtime complexity of this implementation
        must be O(N).
        """
        new_arr = DynamicArray()                # Create new array.

        for i in range(da.length()):
            new_arr.append(da[i])               # Move contents of input array to new array.

        self.heap = new_arr                     # Heap now equal new array.

        idx = (self.heap.length() // 2) - 1         # To maintain heap property, begin checking in middle of array.
        tracker = (self.heap.length() // 2) - 1     # To help keep track of index.

        # Similar to remove_min method. Starting in the middle, check if parent is smaller than child. Swap as needed.
        while idx * 2 + 1 <= self.heap.length() - 1:
            flag = False                                # Flag changes to True when a swap happens.
            if (idx * 2) + 2 > self.heap.length() - 1:  # Check for out of bounds.
                smaller_child = (idx * 2) + 1
            else:
                if self.heap[(idx * 2) + 1] <= self.heap[(idx * 2) + 2]:  # If left child is smaller.
                    smaller_child = (idx * 2) + 1
                else:
                    smaller_child = (idx * 2) + 2       # If right child is smaller.
            if self.heap[idx] > self.heap[smaller_child]:  # Compare value between node and child.
                flag = True
                self.heap.swap(idx, smaller_child)  # Swap elements if replacement is larger.

            if flag:                        # If there was a swap between node and child, adjust node index.
                idx = smaller_child
                if (idx * 2) + 1 > self.heap.length() - 1:      # If there are no children.
                    tracker -= 1
                    idx = tracker           # Adjust node index to one node less.
                    if tracker < 0:         # Loop must stop once index is smaller than zero.
                        break
            else:                           # If no swap, then move to one node less.
                tracker -= 1
                idx = tracker
                if tracker < 0:             # Loop must stop once index is smaller than zero.
                    break

        pass


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)


    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())


    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())


    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
