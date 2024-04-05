class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    tokens = []

    # Look ahead n tokens and return its value
    def peek(self, n=0):
        return self.tokens[n]

    # Consume n tokens and shrink the tokens list
    def consume(self, n=1):
        self.tokens = self.tokens[n::]