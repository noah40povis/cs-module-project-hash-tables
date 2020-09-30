class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def get_key(self):
        return self.key
    
    def get_value(self):
        return self.value 
    
    def get_next(self):
        return self.next 
    
    def set_next(self, entry):
        self.next = entry 
    
    def set_value(self, value):
        self.value = value 


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        # create a fixed array 
        self.bucket_array = [None for i in range(capacity)]
        #state the capacity of array 
        self.capacity = MIN_CAPACITY
        #use this count for put and delete 
        self.number_of_items = 0 


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.bucket_array)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        #The load factor is a measure of how full the hash table 
        # is allowed to get before its capacity is automatically increased.
        return self.number_of_items / self.capacity


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        fnv_offset = 14695981039346656037 #offset_basis- from Wikipedia
        fnv_prime = 1099511628211 #FNV_prime- from Wikipedia
        hash = fnv_offset
        key_utf8 = key.encode()

        for byte in key_utf8:
            hash = hash ^ byte
            hash = hash ^ fnv_prime
        return hash


    def djb2(self, key):
        hash = 5381 
        byte_array = key.encode('utf-8')

        for byte in byte_array:
            hash = ((hash * 33) ^ byte) % 0x100000000 
        return hash 


    def hash_index(self, key): #DO THIS 
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        return self.djb2(key) % self.capacity

    def put(self, key, value): #do this 
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        # index = self.hash_index(key)
        # entry = HashTableEntry(key, value)
        # storage = self.bucket_array[index]
        # self.count =+ 1

        # if storage:
        #     self.bucket_array[index] = entry 
        #     self.bucket_array[index].next = storage
        # else:
        #     self.bucket_array[index] = entry 
        if self.get_load_factor() > .7:
            self.resize(self.capacity * 2)
        
        index = self.hash_index(key)
        entry = HashTableEntry(key, value)
        self.number_of_items += 1 

        if self.bucket_array[index] == None:
            self.bucket_array[index] = entry 
        
        else: 
            current_node = self.bucket_array[index]
            while current_node != None:
                #is the key currently in that node is alrady there overwrite it 
                if current_node.get_key() == key:
                    current_node.set_value(value)
                    return
                # if there is nothing next set the next to the new entry 
                elif current_node.get_next() == None:
                    current_node.set_next(entry)
                    # 
                current_node = current_node.get_next() 
        



    def delete(self, key): #do this 
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # remove the value stored with the given key 
        if self.get(key):
            index = self.hash_index(key)
            current_node = self.bucket_array[index]
            prev_entry = None
        else: 
            print(f"Warning: Tried to delete a value from HashTable but no value exists for key: '{key}'")

        while current_node != None: 
            if current_node.get_key() == key: 
                self.number_of_items -= 1 
                if prev_entry == None: 
                    current_node.set_value(None)
                else: 
                    prev_entry.set_next(current_node.get_next())
            
            prev_entry = current_node
            current_node = current_node.get_next()
        
        if self.get_load_factor() < 0.2:
            new_capacity = self.capacity // 2
            if new_capacity < MIN_CAPACITY:
                self.resize(MIN_CAPACITY)
            else:
                self.resize(new_capacity)

    def get(self, key): #do this 
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        #retrieve the value stored with the given key 
        index = self.hash_index(key)
        entry = self.bucket_array[index]
        if entry is None: 
            return None 
        while entry != None:
            if entry.get_key() == key:
                return entry.get_value()
            entry = entry.get_next()
        return None 



    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        #create variable for old array 
        old_array = self.bucket_array
        self.bucket_array = [None] * new_capacity
        self.capacity = new_capacity

        for index in range(len(old_array)):
            current_node = old_array[index]
            while current_node != None:
                self.put(current_node.get_key(), current_node.get_value())
                current_node = current_node.get_next()        



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

#Stretch: When load factor decreases below `0.2`, automatically rehash
#the table to half its previous size, down to a minimum of 8 slots.