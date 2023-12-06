class NounObject:
    def __init__(self, noun):
        self.noun = noun
        self.associated_nouns = []
        self.associated_verbs = []

    def to_dict(self):
        return {
            'noun': self.noun,
            'associated_nouns': self.associated_nouns,
            'associated_verbs': self.associated_verbs
        }
