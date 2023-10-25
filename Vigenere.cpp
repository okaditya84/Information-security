#include <iostream>
#include <string>
using namespace std;

string vigenereEncrypt(const string &plainText, const string &key)
{
    string encryptedText = "";
    for (int i = 0, j = 0; i < plainText.length(); ++i)
    {
        char plainChar = plainText[i];
        char keyChar = key[j % key.length()];

        if (isalpha(plainChar))
        {
            char base = isupper(plainChar) ? 'A' : 'a';
            char encryptedChar = (plainChar + keyChar - 2 * base) % 26 + base;
            encryptedText += encryptedChar;
            ++j;
        }
        else
        {
            encryptedText += plainChar;
        }
    }
    return encryptedText;
}

string vigenereDecrypt(const string &encryptedText, const string &key)
{
    string decryptedText = "";
    for (int i = 0, j = 0; i < encryptedText.length(); ++i)
    {
        char encryptedChar = encryptedText[i];
        char keyChar = key[j % key.length()];

        if (isalpha(encryptedChar))
        {
            char base = isupper(encryptedChar) ? 'A' : 'a';
            char decryptedChar = (encryptedChar - keyChar + 26) % 26 + base;
            decryptedText += decryptedChar;
            ++j;
        }
        else
        {
            decryptedText += encryptedChar;
        }
    }
    return decryptedText;
}

int main()
{
    string plainText, key;

    cout << "Enter the plaintext: ";
    getline(cin, plainText);

    cout << "Enter the key: ";
    getline(cin, key);

    string encryptedText = vigenereEncrypt(plainText, key);
    string decryptedText = vigenereDecrypt(encryptedText, key);

    cout << "\nEncrypted Text: " << encryptedText << endl;
    cout << "Decrypted Text: " << decryptedText << endl;

    return 0;
}
