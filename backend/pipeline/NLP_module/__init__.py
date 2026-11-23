class text_entity:
    def __init__(self, text):
        self.text = text
        # self.uID = self.generate_unique_id()
        self.chunks = [] #will just hold chunkid 

        # add chunk i

class text_chunk:
    def __init__(self, chunk_id, text):
        self.chunk_id = chunk_id
        self.text = text
        # self.uID = self.generate_unique_id()
