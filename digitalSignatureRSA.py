import os
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_key, private_key
def sign_message(private_key, message):
    private_key = serialization.load_pem_private_key(private_key, password=None)
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature
def verify_signature(public_key, message, signature):
    public_key = serialization.load_pem_public_key(public_key)
    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

def encrypt_file(public_key, input_file, output_file):
    public_key = serialization.load_pem_public_key(public_key)
    with open(input_file, 'rb') as f:
        file_data = f.read()
    encrypted_data = public_key.encrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)
def decrypt_file(private_key, input_file, output_file):
    private_key = serialization.load_pem_private_key(private_key, password=None)
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
def main():
    private_key = None
    public_key = None
    while True:
        print("Menu:")
        print("1. Generate Key Pair")
        print("2. Sign a File")
        print("3. Verify Signature")
        print("4. Encrypt File")
        print("5. Decrypt File")
        print("6. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            private_key, public_key, key_pair = generate_key_pair()
            print("Key pair generated.")
            print("Private Key:\n", key_pair.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()).decode('utf-8'))
            print("Public Key:\n", public_key.decode('utf-8'))
        elif choice == "2":
            if private_key is None:
                print("Please generate a key pair first.")
            else:
                input_file = input("Enter the name of the file to sign: ")
                if os.path.exists(input_file):
                    with open(input_file, 'r') as f:
                        message = f.read()
                    signature = sign_message(private_key, message)
                    with open("signature.bin", "wb") as signature_file:
                        signature_file.write(signature)
                    print("Signature generated and saved as signature.bin")
                else:
                    print("File not found.")
        elif choice == "3":
            if public_key is None:
                print("Please generate a key pair first.")
            else:
                input_file = input("Enter the name of the file to verify: ")
                if os.path.exists(input_file):
                    with open(input_file, 'r') as f:
                        message = f.read()
                    with open("signature.bin", "rb") as signature_file:
                        signature = signature_file.read()
                    if verify_signature(public_key, message, signature):
                        print("Signature is valid.")
                    else:
                        print("Signature is not valid.")
                else:
                    print("File not found.")
        elif choice == "4":
            if public_key is None:
                print("Please generate a key pair first.")
            else:
                input_file = input("Enter the name of the file to encrypt: ")
                output_file = input("Enter the name of the encrypted file: ")
                if os.path.exists(input_file):
                    encrypt_file(public_key, input_file, output_file)
                    print("File encrypted and saved.")
                else:
                    print("File not found.")
        elif choice == "5":
            if private_key is None:
                print("Please generate a key pair first.")
            else:
                input_file = input("Enter the name of the file to decrypt: ")
                output_file = input("Enter the name of the decrypted file: ")
                if os.path.exists(input_file):
                    decrypt_file(private_key, input_file, output_file)
                    print("File decrypted and saved.")
                else:
                    print("File not found.")
        elif choice == "6":
            break
if __name__ == "__main__":
    main()

