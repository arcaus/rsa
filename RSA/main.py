import pickle
import gzip
import rsa


def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('keys/publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('keys/privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))


def loadKeys():
    with open('keys/publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('keys/privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey


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
        print("Operation Modes:\n1. Encrypt and Sign\n2. Decrypt and Verify\n3. Exit")
        choice = input('Choice: ')

        if choice == '1':
            path = input('Enter path to plaintext file: ')
            with open(path, 'r') as p:
                plaintext = p.read()

            generateKeys()
            privateKey, publicKey = loadKeys()

            ciphertext = encrypt(plaintext, publicKey)
            signature = sign(plaintext, privateKey)

            # Store ciphertext and signature in a file using pickle
            with open('ciphertext.pkl', 'wb') as f:
                pickle.dump((ciphertext, signature), f)

            with open('ciphertext.pkl', 'rb') as f:
                with gzip.open('ciphertext.gz', 'wb') as g:
                    g.write(f.read())

            print('File encrypted and stored in ciphertext.pkl')

        elif choice == '2':
            try:
                path = input('Enter path to zipped ciphertext file: ')
                with gzip.open(path, 'rb') as f:
                    ciphertext, signature = pickle.load(f)

                privateKey, publicKey = loadKeys()

                plaintext = decrypt(ciphertext, privateKey)
                verification = verify(plaintext, signature, publicKey)
                if plaintext and verification:
                    print('\nDecryption successful.\n')
                    with open('secret.txt', 'w') as s:
                        s.write('=============== SIGNATURE VERIFIED ===============\n')
                        s.write(plaintext)
                        s.write('\n=============== SIGNATURE VERIFIED ===============')
                else:
                    print('\nDecryption failed.\n')

            except FileNotFoundError:
                print('No encrypted data found.\n')

        elif choice == '3' or choice.lower() == 'exit':
            print('Thank you for using this program. Goodbye!')
            break

        else:
            print('Invalid choice.\n')


if __name__ == "__main__":
    main()
