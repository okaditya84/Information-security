
def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key_index = 0
    for char in plaintext:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            key_index += 1
            shift = ord(key_char.upper()) - ord('A')
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            ciphertext += encrypted_char
        else:
            ciphertext += char
    return ciphertext

def vigenere_decrypt(ciphertext, key):
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            key_char = key[key_index % len(key)]
            key_index += 1
            shift = ord(key_char.upper()) - ord('A')
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext += decrypted_char
        else:
            plaintext += char
    return plaintext

# Get user input
plaintext_or_ciphertext = input("Enter the plaintext or ciphertext: ")
key = input("Enter the key: ")

# Encrypt or decrypt based on user input
if plaintext_or_ciphertext.isalpha():
    ciphertext = vigenere_encrypt(plaintext_or_ciphertext, key)
    print("Ciphertext:", ciphertext)
else:
    plaintext = vigenere_decrypt(plaintext_or_ciphertext, key)
    print("Plaintext:", plaintext)
