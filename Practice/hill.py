import sys

def encrypt(key, plaintext):
    key_len = len(key)
    if not is_perfect_square(key_len):
        return "Enter a key whose length is a perfect square"
    
    root = int(key_len**0.5)
    key_matrix = [[0] * root for _ in range(root)] 
    k = 0
    for i in range(root):
        for j in range(root):
            key_matrix[i][j] = (ord(key[k]) - ord('a')) % 26
            k += 1
    
    plaintext_len = len(plaintext)
    if root >= plaintext_len:
        for i in range(root - plaintext_len):
            plaintext += 'x'
            plaintext_len += 1 
    plaintext_matrix = [[0] * (plaintext_len//root) for _ in range(root)]
            
    for i in range(plaintext_len//root):
        for j in range(root):
           plaintext_matrix[j][i] = (ord(plaintext[i*root + j]) - ord('a')) % 26
           
    ciphertext = ""
    for i in range(len(plaintext_matrix[0])):
        for j in range(len(plaintext_matrix)):
            ciphertext += chr((multiply_matrices(key_matrix, plaintext_matrix)[j][i] % 26) + ord('a')) 
    return ciphertext

def multiply_matrices(matrix1, matrix2):
    result = [[0] * len(matrix2[0]) for _ in range(len(matrix1))]
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    return result
                
def is_perfect_square(num):
    root = int(num**0.5)
    return root*root == num
    
def decrypt(ciphertext, key):
    # Implementation of decryption
    pass 

choice = int(input("Enter 1 to encrypt, 0 to decrypt: "))

if choice == 1:
    plaintext = input("Enter string to encrypt: ")
    key = input("Enter key: ") 
    print("Encrypted string: ", encrypt(key, plaintext))
    
elif choice == 0:
   ciphertext = input("Enter ciphertext to decrypt: ")
   key = input("Enter key: ")
   decrypt(ciphertext, key)
   
else:
   print("Invalid choice")