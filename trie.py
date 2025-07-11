from lru_cache import LRUCache
from lfu_cache import LFUCache
# cache = LRUCache(3)
cache = LFUCache(3)

class Node:
    def __init__(self, key = ""):
        self.key = key
        self.children = {}
        self.isWord = False
        self.word = ""
        self.rank = 0
        self.url = ""

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word: str, url: str) -> None:
        word = word.lower()
        root = self.root

        for c in word:
            if c not in root.children:
                root.children[c] = Node()
            
            root = root.children[c]
        
        root.isWord = True
        root.word = word
        root.url = url
    
    # DFS
    def traverse(self, root):
        if not root:
            return
        
        for child in root.children:
            self.traverse(root.children[child])
        
        if root.isWord:
            self.out.append({ "word": root.word, "rank": root.rank, "url": root.url})

    def search(self, word):
        word = word.lower()
        root = self.root

        if not word.strip():
            return []
        
        if cache.get(word) != -1:
            print("DATA FROM CACHE")
            return cache.get(word)

        self.out = []

        for c in word:
            if c not in root.children:
                return []
            root = root.children[c]

        if root.isWord:
            root.rank += 1
        
        self.traverse(root)
        cache.put(word, self.out)
        return self.out
