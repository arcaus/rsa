import pickle, gzip, rsa, os


def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(2048)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))


def loadKeys(key='all'):
    publicPath = 'keys/publicKey.pem'
    privatePath = 'keys/privateKey.pem'
    if key == 'all':
        with open(publicPath, 'rb') as p:
            publicKey = rsa.PublicKey.load_pkcs1(p.read())
        with open(privatePath, 'rb') as p:
            privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        return privateKey, publicKey
    elif key == 'public':
        with open(publicPath, 'rb') as p:
            publicKey = rsa.PublicKey.load_pkcs1(p.read())
        return publicKey
    elif key == 'private':
        with open(privatePath, 'rb') as p:
            privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        return privateKey


def encrypt(plaintext, key):
    return rsa.encrypt(plaintext.encode(), key)


def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode()
    except:
        return False


def sign(plaintext, key):
    return rsa.sign(plaintext.encode(), key, 'SHA-256')


def verify(plaintext, signature, key):
    try:
        return rsa.verify(plaintext.encode(), signature, key, ) == 'SHA-256'
    except:
        return False



def main():
    while True:
        print('Welcome to RSA Encryption\nPlease choose your option:')
        print('1. Generate RSA Keys\n2. Use RSA Encryption \n3. Use RSA Decryption\n4. Exit')
        choice = input('Choice: ')

        if choice == '1':
            generateKeys()
            print('Keys generated and stored in keys/publicKey.pem and keys/privateKey.pem\n')

        elif choice == '2':
            path = input('Enter path to plaintext file: ')
            with open(path, 'r') as p:
                plaintext = p.read()

            privateKey, publicKey = loadKeys()
            ciphertext = encrypt(plaintext, publicKey)
            signature = sign(plaintext, privateKey)

            with open('encrypted_text.pkl', 'wb') as f:
                pickle.dump((ciphertext, signature), f)

            with open('encrypted_text.pkl', 'rb') as f:
                with gzip.open('encrypted_text.gz', 'wb') as g:
                    g.write(f.read())

            os.remove('encrypted_text.pkl')

            print('File encrypted and stored in encrypted_text.gz')

        elif choice == '3':
            path = input('Enter path to zipped encrypted file: ')
            try:
                with gzip.open(path, 'rb') as f:
                    ciphertext, signature = pickle.load(f)

                privateKey, publicKey = loadKeys()
                plaintext = decrypt(ciphertext, privateKey)
                verification = verify(plaintext, signature, publicKey)
                if plaintext and verification:
                    print('\nSuccessfully decrypted and stored in decrypted_message.txt\n')
                    with open('decrypted_message.txt', 'w') as s:
                        s.write('**SIGNATURE VERIFIED**\n\n')
                        s.write(plaintext)
                else:
                    print('\nDecryption failed.\n')

            except FileNotFoundError:
                print('No encrypted data found.\n')

        elif choice == '4' or choice.lower() == 'exit':
            print('Thank you for using RSA Encryption.')
            break

        else:
            print('Invalid choice.\n')



if __name__ == "__main__":
    main()
  
