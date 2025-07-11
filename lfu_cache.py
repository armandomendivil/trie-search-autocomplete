from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_to_val_freq = {}  # key -> (value, freq)
        self.freq_to_keys = defaultdict(OrderedDict)  # freq -> OrderedDict of keys
        self.min_freq = 0

    def get(self, key: str) -> list[str]:
        if key not in self.key_to_val_freq:
            return -1

        value, freq = self.key_to_val_freq[key]
        # Remove key from current freq group
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1

        # Add key to higher freq group
        self.freq_to_keys[freq + 1][key] = None
        self.key_to_val_freq[key] = (value, freq + 1)
        return value

    def put(self, key: str, value: list[str]) -> None:
        if self.capacity == 0:
            return

        if key in self.key_to_val_freq:
            # Update value and frequency
            self.key_to_val_freq[key] = (value, self.key_to_val_freq[key][1])
            self.get(key)  # promote frequency
            return

        if len(self.key_to_val_freq) >= self.capacity:
            # Evict least frequently used key
            lfu_keys = self.freq_to_keys[self.min_freq]
            evict_key, _ = lfu_keys.popitem(last=False)
            if not lfu_keys:
                del self.freq_to_keys[self.min_freq]
            del self.key_to_val_freq[evict_key]

        # Insert new key with freq 1
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

        


# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)