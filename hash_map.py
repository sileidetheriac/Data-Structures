# Course: CS261 - Data Structures
# Assignment: 5
# Student: Sileide De Freitas Theriac
# Description: Program contains an implementation of a HashMap class.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        TODO: Write this implementation
        Method clears the content of the hash map. It does not change underlying hash table
        capacity.
        """

        for i in range(self.capacity):                  # Loop through array.
            bucket = self.buckets.get_at_index(i)       # To access LinkedList inside bucket.
            if bucket.head is not None:                 # Check for the occupied buckets.
                cur_size = self.buckets[i].length()     # Store amount of elements inside buckets.
                bucket.head = None                      # Make head equals None, automatically removing all other nodes.
                self.size -= cur_size                   # Update number of elements in hash table.

        pass

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        Method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        idx_in_array = abs(self.hash_function(key)) % self.capacity     # Hash function to compute index.

        linked_lst = self.buckets[idx_in_array]                         # To reach LinkedList inside buckets.

        if linked_lst.head is None:                                     # If bucket is empty, return None.
            return None
        else:
            for _ in range(linked_lst.length()):                        # Loop through LinkedList inside bucket.
                if linked_lst.contains(key):                            # Find matching key.
                    return linked_lst.contains(key).value               # Return associated value.
                return None                                             # Return None if key is not in table.

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        Method updates the key / value pair in the hash map. If a given key already exists in
        the hash map, its associated value should be replaced with the new value. If a given key is
        not in the hash map, a key / value pair should be added.
        """

        idx_in_array = abs(self.hash_function(key)) % self.capacity     # Hash function to compute index.

        linked_lst = self.buckets[idx_in_array]                         # To reach LinkedList inside buckets.

        if linked_lst.head is None:                                     # If bucket is empty, add Node.
            linked_lst.insert(key, value)
            self.size += 1                                              # Update number of elements.
            return
        for _ in range(linked_lst.length()):                            # If bucket already contains one or more nodes.
            if not linked_lst.contains(key):                            # If key is not in table, add the Node.
                linked_lst.insert(key, value)
                self.size += 1                                          # Update number of elements.
            if linked_lst.contains(key):                                # If key was already there.
                linked_lst.contains(key).value = value                  # Then, simply update its value.
        pass

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        Method removes the given key and its associated value from the hash map. If a given
        key is not in the hash map, the method does nothing (no exception needs to be raised).
        """
        idx_in_array = abs(self.hash_function(key)) % self.capacity     # Hash function to compute index.

        linked_lst = self.buckets[idx_in_array]                         # To reach LinkedList inside buckets.

        if linked_lst.head is None:                                     # If bucket is empty, just return.
            return
        else:
            for _ in range(linked_lst.length()):                        # Loop through LinkedList inside bucket.
                if linked_lst.contains(key):                            # If key is found, remove the Node.
                    linked_lst.remove(key)
                    self.size -= 1                                      # Update number of elements.

        pass

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        Method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.
        """
        idx_in_array = abs(self.hash_function(key)) % self.capacity     # Hash function to compute index.

        linked_lst = self.buckets[idx_in_array]                         # To reach LinkedList inside buckets.

        if linked_lst.head is None:                                     # If bucket is empty, then key is not there.
            return False
        else:
            for _ in range(linked_lst.length()):                        # Loop through LinkedList inside bucket.
                if linked_lst.contains(key):                            # If key is found, return True.
                    return True
                return False                                            # If key is not there, return False.

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        Method returns a number of empty buckets in the hash table.
        """

        empty_buckets = 0                                               # To keep track of number of empty buckets.
        for i in range(self.capacity):                                  # Loop through array.
            bucket = self.buckets.get_at_index(i)                       # To reach LinkedList inside bucket.
            if bucket.head is None:                                     # If there is no Node in the bucket.
                empty_buckets += 1                                      # Add 1 to count.

        return empty_buckets

    def table_load(self) -> float:
        """
        TODO: Write this implementation
        Method returns the current hash table load factor.
        """
        # The load factor of a hash table is the average number of elements in each bucket.
        # Total number of elements stored in the table divided by the number of buckets.
        load_factor = self.size / self.capacity
        return load_factor

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        Method changes the capacity of the internal hash table. All existing key / value pairs
        must remain in the new hash map and all hash table links must be rehashed. If
        new_capacity is less than 1, this method should do nothing.
        """
        if new_capacity < 1:            # If new_capacity is less than 1, method should do nothing.
            return

        new_table = DynamicArray()                  # Create new array.

        for _ in range(new_capacity):
            new_table.append(LinkedList())          # Add new buckets to array containing LinkedLists.

        for i in range(self.capacity):              # Loop through old hash table.
            if self.buckets[i].head is not None:    # Go into each filled bucket and rehashed all elements.
                for j in self.buckets[i]:
                    # Re-compute the hash function for each element with the new number of buckets.
                    idx_new_table = abs(self.hash_function(j.key)) % new_capacity
                    new_table[idx_new_table].insert(j.key, j.value)

        self.capacity = new_capacity                # Make new capacity the current capacity.
        self.buckets = new_table                    # Make the class HashMap buckets equal new table.

        pass

    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        Method returns a DynamicArray that contains all keys stored in your hash map. The
        order of the keys in the DA does not matter.
        """
        key_arr = DynamicArray()                    # Create new Dynamic Array to store all keys.

        for i in range(self.capacity):              # Loop through current table.
            if self.buckets[i].head is not None:    # If bucket is filled.
                for j in self.buckets[i]:
                    key_arr.append(j.key)           # Add all keys to new Dynamic array.

        return key_arr


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
