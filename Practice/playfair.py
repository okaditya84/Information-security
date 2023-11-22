class PlayfairCipher:
    def _init_(self):
        self.length = 0
        self.table = []

    def start(self):
        key = self.parse_string(input("Enter the key for Playfair cipher: "))
        while key == "":
            print("Key cannot be empty. Please enter a valid key.")
            key = self.parse_string(input())

        self.table = self.cipher_table(key)

        plaintext = self.parse_string(input('Enter the plaintext to be encipher:' ))
        while plaintext == "":
            print("Plaintext cannot be empty. Please enter a valid plaintext.")
            plaintext = self.parse_string(input())

        ciphertext = self.cipher(plaintext)
        decoded_output = self.decode(ciphertext)

        self.key_table(self.table)
        self.print_results(ciphertext, decoded_output)

    def parse_string(self, parse):
        parse = parse.upper()
        parse = ''.join(filter(str.isalpha, parse))
        parse = parse.replace("J", "I")
        return parse

    def cipher_table(self, key):
        playfair_table = [['' for _ in range(5)] for _ in range(5)]
        key_string = key + "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        print(playfair_table)
        # for i in range(5):
        #     for j in range(5):
        #         playfair_table[i][j] = ""
        # print(playfair_table,"hiii")                

        for k in range(len(key_string)):
            repeat = False
            used = False
            for i in range(5):
                for j in range(5):
                    if playfair_table[i][j] == key_string[k]:
                        repeat = True
                    elif playfair_table[i][j] == "" and not repeat and not used:
                        playfair_table[i][j] = key_string[k]
                        used = True
        return playfair_table

    def cipher(self, plaintext):
        self.length = (len(plaintext) // 2) + (len(plaintext) % 2)

        for i in range(self.length - 1):
            if plaintext[2 * i] == plaintext[2 * i + 1]:
                plaintext = plaintext[:2 * i + 1] + 'X' + plaintext[2 * i + 1:]
                self.length = (len(plaintext) // 2) + len(plaintext) % 2

        digraph = [plaintext[2 * j:2 * j + 2] for j in range(self.length)]
        print(digraph)
        out = ""
        enc_digraphs = self.encode_digraph(digraph)

        for k in range(self.length):
            out += enc_digraphs[k]

        return out
 
    def encode_digraph(self, di):
        encipher = [""] * self.length

        for i in range(self.length):
            if len(di[i]) < 2:
                di[i] += 'X'
            a = di[i][0]
            b = di[i][1]
            r1, c1 = self.get_point(a)
            r2, c2 = self.get_point(b)

            if r1 == r2:
                c1 = (c1 + 1) % 5
                c2 = (c2 + 1) % 5
            elif c1 == c2:
                r1 = (r1 + 1) % 5
                r2 = (r2 + 1) % 5
            else:
                c1, c2 = c2, c1

            encipher[i] = self.table[r1][c1] + self.table[r2][c2]

        return encipher

    def decode(self, ciphertext):
        decoded = ""

        for i in range(len(ciphertext) // 2):
            a = ciphertext[2 * i]
            b = ciphertext[2 * i + 1]
            r1, c1 = self.get_point(a)
            r2, c2 = self.get_point(b)

            if r1 == r2:
                c1 = (c1 + 4) % 5
                c2 = (c2 + 4) % 5
            elif c1 == c2:
                r1 = (r1 + 4) % 5
                r2 = (r2 + 4) % 5
            else:
                c1, c2 = c2, c1

            decoded += self.table[r1][c1] + self.table[r2][c2]

        return decoded

    def get_point(self, c):
        for i in range(5):
            for j in range(5):
                if c == self.table[i][j][0]:
                    return i, j

    def key_table(self, print_table):
        print("Playfair Cipher Key Matrix:")
        print()

        for i in range(5):
            for j in range(5):
                print(print_table[i][j], end=" ")
            print() 
        print()

    def print_results(self, ciphertext, decoded):
        print("Encrypted Message: ", ciphertext)
        print()
        print("Decrypted Message: ", decoded)

if __name__ == "__main__":
    PlayfairCipher().start()



