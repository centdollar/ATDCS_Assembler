class Lexer:
    def __init__(self, content):
        self.content = content

    content = ""

    # Trims white space to the left
    def trim_left(self):
        while len(self.content) != 0 and self.content[0].isspace():
            self.content = self.content[1::]

    def chopWhileNotEOL(self):
        while len(self.content) != 0 and self.content[0] != "\n":
            self.content = self.content[1::]
        self.content = self.content[1::]

    # chop the array n elements from the left
    def chop(self, n):
        token = self.content[0:n]
        self.content = self.content[n::]
        return token

    def chopWhileAlphaNum(self):
        n = 0
        while n < len(self.content) and self.content[n].isalnum():
            n += 1
        return self.chop(n)

    def chopWhileNum(self):
        n = 0
        while n < len(self.content) and self.content[n].isnumeric():
            n += 1
        return self.chop(n)

    def chopWileNotEndBrace(self):
        n = 0
        while n < len(self.content) and self.content[n] != "]":
            n += 1
        rVal = self.chop(n)
        self.chop(1)
        return rVal

    def chopWhileDotAlpha(self):
        n = 0
        if n < len(self.content) and self.content[n] == ".":
            n += 1
        while n < len(self.content) and self.content[n].isalpha() and self.content[n] != "\n":
            n += 1
        return self.chop(n)

    def chopWhileEqual(self):
        n = 0
        while n < len(self.content) and self.content[n] == "=":
            n += 1
        return self.chop(n)

    def chopWhileLessThan(self):
        n = 0
        while n < len(self.content) and self.content[n] == "<":
            n += 1
        return self.chop(n)


    def nextToken(self):
        # trim the whitespace 
        self.trim_left()
        if self.content[0:2] == "//":
            self.chopWhileNotEOL()
        self.trim_left()

        if len(self.content) == 0:
            return None

        elif self.content[0] == "m" and self.content[1] == "[":
            if self.content[2:4] == "0x":
                self.content = self.content[2:8] + self.content[9::]
                return self.chopWhileAlphaNum()
            else:
                self.content = self.content[2::]
                return self.chopWileNotEndBrace()

        elif self.content[0:2] == "0x":
            return self.chopWhileAlphaNum()

        elif self.content[0] == "=":
            return self.chopWhileEqual()

        elif self.content[0] == "<":
            return self.chopWhileLessThan()

        elif self.content[0] == ".":
            return self.chopWhileDotAlpha()

        elif self.content[0] == "#":
            self.content = self.content[1::]
            return "#" + self.chopWhileNum()

        elif self.content[0] == "@":
            self.content = self.content[1::]
            return "@" + self.chopWhileAlphaNum()
        elif self.content[0].isalpha():
            return self.chopWhileAlphaNum()

        elif self.content[0].isnumeric():
            return self.chopWhileNum()

        else:
            print(f"Reached invalid token: {self.content}")