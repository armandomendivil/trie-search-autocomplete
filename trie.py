from pymongo import MongoClient, InsertOne, UpdateOne
import json

client = MongoClient("mongodb+srv://dev:Demo123!@cluster0.tstvjvs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["itj"]
collection = db["movies"]
# collection.drop()

class Node:
    def __init__(self, id = "", key = ""):
        self._id = id
        self.key = key
        self.children = {}
        self.isWord = False
        self.word = ""
        self.rank = 0
        self.url = ""

    def to_dict(self):
        return {
            "_id": self._id,
            "key": self.key,
            "isWord": self.isWord,
            "word": self.word,
            "rank": self.rank,
            "children": {k: v.to_dict() for k, v in self.children.items()},
            "url": self.url
        }

class Trie:
    def __init__(self):
        self.root = Node()
    
    def insert_bulk(self, word, url):
        prefix = ""
        ops = []
        nodes_cache = {}

        for i, c in enumerate(word):
            prefix += c

            if prefix not in nodes_cache:
                node = collection.find_one({"_id": prefix})
                if not node:
                    node_doc = {
                        "_id": prefix,
                        "key": c,
                        "children": {},
                        "isWord": False,
                        "word": "",
                        "rank": 0,
                        "url": ""
                    }
                    ops.append(InsertOne(node_doc))
                    nodes_cache[prefix] = node_doc
                else:
                    nodes_cache[prefix] = node
            
            if i > 0:
                parent_prefix = prefix[:-1]
                parent_node = nodes_cache[parent_prefix]
                if c not in parent_node["children"]:
                    parent_node["children"][c] = prefix

                    # Agregar update para padre (actualiza solo al final)
                    ops.append(UpdateOne({"_id": parent_prefix}, {"$set": {"children": parent_node["children"]}}))

        ops.append(UpdateOne({"_id": word}, {"$set": {"isWord": True, "word": word, "url": url}}))

        if ops:
            collection.bulk_write(ops)


    def insert(self, word: str, url) -> None:
        prefix = ""
        for i, c in enumerate(word):
            prefix += c
            node = collection.find_one({"_id": prefix})

            if not node:
                # Crear nodo nuevo
                node_doc = {
                    "_id": prefix,
                    "key": c,
                    "children": {},
                    "isWord": False,
                    "word": "",
                    "rank": 0
                }
                collection.insert_one(node_doc)
            if i > 0:
                # Actualizar el padre para que apunte a este nodo
                parent_prefix = prefix[:-1]
                parent_node = collection.find_one({"_id": parent_prefix})
                if c not in parent_node["children"]:
                    parent_node["children"][c] = prefix
                    collection.update_one({"_id": parent_prefix}, {"$set": {"children": parent_node["children"]}})

        # Al final marcar el último nodo como palabra completa
        collection.update_one({"_id": word}, {"$set": {"isWord": True, "word": word, "url": url}})
    
    # DFS
    def traverse(self, root):
        if not root:
            return
        
        for child in root["children"]:
            self.traverse(collection.find_one({ "_id": root["children"][child] }))
        
        if root["isWord"]:
            self.out.append({ "title": root["word"], "rank": root["rank"], "url": root["url"]})

    def search(self, word):
        id = word[0]
        root = collection.find_one({ "_id":  id })
        self.out = []
        prefix = [id]

        if not root:
            return []

        # for c in word[1:]:
        #     prefix.append(c)
        #     id = "".join(prefix)
        #     if c not in root["children"]:
        #         return []
        #     root = collection.find_one({ "_id": id })

        root = collection.find_one({ "_id": word })

        if not root:
            return []

        if root["isWord"]:
            collection.update_one(
                { "_id": root["_id"] },
                { "$set": { "rank": root["rank"] + 1 } }
            )
        
        self.traverse(root)
        return self.out

# data = []
# with open("movies.json", "r") as file:
#     data = json.load(file)


# print(data[0])

# trie = Trie()
# counter = 1
# for d in data:
#     trie.insert_bulk(d["title"], d["url"])
#     print(counter, d["title"])
    # counter += 1

# trie = Trie()
# trie.insert(data[0]["title"], data[0]["url"])


#     movies = []

# with open("movies.txt", "r") as file:
#     for line in file:
#         line = line.strip()
#         if line:
#             movies.append(json.loads(line))

# with open("movies.json", "w") as out_file:
#     json.dump(movies, out_file, indent=2)

# print("Converted to movies.json")

# trie = Trie()
# trie.insert("matrix")
# trie.insert("matrix 2")
# trie.insert("matrix 3")
# print(trie.search("matri"))
# words = ["twitter", "twitch", "twilight", "twin peak", "beer", "best", "bet"]
# for w in words:
#     trie.insert(w)

# trie.search('twitch')
# trie.search('twitch')
# trie.search('twitch')
# trie.search('twitch')
# trie.search('twitch')

# trie.search('twitter')
# trie.search('twitter')
# trie.search('twitter')

# print(
#     trie.search("tw")
# )