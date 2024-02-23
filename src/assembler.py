import sys

def main():
    # print(f"Arguments List: {sys.argv}")
    file1tokens = tokenize(sys.argv[1])
    print(file1tokens)

# tokenize(file)
#   file - path of the file to tokenize
# returns tokens[]
def tokenize(file):
    tokens = []
    with open(file, "r") as f:
        # Read file into variable array F
        F = f.readlines()

        # method for removing newlines as the lines in the file is populated into the tokens array
        stripnewline = lambda x: x.strip("\n")

        # populates tokens array
        tokens = [(stripnewline(F[i])) for i in range(len(F))]

        # filters out any empty lines in the token list
        tokens = list(filter(lambda x: x != '', tokens))
    return tokens

if __name__ == "__main__":
    main()