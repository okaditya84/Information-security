#include <bits/stdc++.h>
using namespace std;

string encrypt(string text, int rails)
{
    char railMatrix[rails][text.length()];
    for (int i = 0; i < rails; i++)
    {
        for (int j = 0; j < text.length(); j++)
        {
            railMatrix[i][j] = '.';
        }
    }

    int row = 0;
    int direction = 1; // 1 for moving down, -1 for moving up

    for (int i = 0; i < text.length(); i++)
    {
        railMatrix[row][i] = text[i];

        if (row == 0)
        {
            direction = 1;
        }
        else if (row == rails - 1)
        {
            direction = -1;
        }

        row += direction;
    }

    string encryptedText = "";
    for (int i = 0; i < rails; i++)
    {
        for (int j = 0; j < text.length(); j++)
        {
            if (railMatrix[i][j] != '.')
            {
                encryptedText += railMatrix[i][j];
            }
        }
    }

    return encryptedText;
}

string decrypt(string text, int rails)
{
    char railMatrix[rails][text.length()];
    for (int i = 0; i < rails; i++)
    {
        for (int j = 0; j < text.length(); j++)
        {
            railMatrix[i][j] = '.';
        }
    }

    int row = 0;
    int direction = 1;

    for (int i = 0; i < text.length(); i++)
    {
        railMatrix[row][i] = '*';

        if (row == 0)
        {
            direction = 1;
        }
        else if (row == rails - 1)
        {
            direction = -1;
        }

        row += direction;
    }

    int index = 0;
    for (int i = 0; i < rails; i++)
    {
        for (int j = 0; j < text.length(); j++)
        {
            if (railMatrix[i][j] == '*' && index < text.length())
            {
                railMatrix[i][j] = text[index++];
            }
        }
    }

    string decryptedText = "";
    row = 0;
    direction = 1;

    for (int i = 0; i < text.length(); i++)
    {
        decryptedText += railMatrix[row][i];

        if (row == 0)
        {
            direction = 1;
        }
        else if (row == rails - 1)
        {
            direction = -1;
        }

        row += direction;
    }

    return decryptedText;
}

int main()
{
    string text;
    int rails;

    cout << "Enter the text to encrypt: ";
    getline(cin, text);

    cout << "Enter the number of rails: ";
    cin >> rails;

    string encryptedText = encrypt(text, rails);
    cout << "Encrypted: " << encryptedText << endl;

    string decryptedText = decrypt(encryptedText, rails);
    cout << "Decrypted: " << decryptedText << endl;

    return 0;
}
