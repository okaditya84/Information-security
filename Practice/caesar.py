
def caesar_cipher(key, plaintext):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                ciphertext += chr((ord(char) - 65 + key) % 26 + 65)
            else:
                ciphertext += chr((ord(char) - 97 + key) % 26 + 97)
        else:
            ciphertext += char
    return ciphertext

def caesar_decrypt(key, ciphertext):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                plaintext += chr((ord(char) - 65 - key) % 26 + 65)
            else:
                plaintext += chr((ord(char) - 97 - key) % 26 + 97)
        else:
            plaintext += char
    return plaintext

key = int(input("Enter the key: "))
plaintext = input("Enter the plaintext: ")

ciphertext = caesar_cipher(key, plaintext)
print("Ciphertext:", ciphertext)

decrypted_text = caesar_decrypt(key, ciphertext)
print("Decrypted Text:", decrypted_text)
