class Sample:
    def __init__(self, speaker, article, section, embedding=None, embedding_type=None):
        self.speaker = speaker
        self.article = article
        self.section = section
        if embedding is not None and embedding_type is not None:
            self.embedding = embedding
            self.embedding_type = embedding_type
