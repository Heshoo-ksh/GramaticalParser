class NounObject:
    def __init__(self, noun):
        self.noun = noun
        self.associated_verbs = []
        self.associated_nouns = []

    def add_associated_verb(self, verb):
        self.associated_verbs.append(verb)

    def add_associated_noun(self, noun):
        self.associated_nouns.append(noun)

    def to_dictionary(self):
        return {
            "noun": self.noun,
            "associated_nouns": self.associated_nouns,
            "associated_verbs": self.associated_verbs
        }
