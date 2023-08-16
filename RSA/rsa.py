import pickle
import gzip
import yaml
import rsa


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


def prsa():
    while True:
        print("Operation Modes:\n1. Encrypt and Sign\n2. Decrypt and Verify\n3. Go Back")
        choice = input('Choice: ')

        if choice == '1':
            path = input('Enter path to plaintext file: ')
            with open(path, 'r') as p:
                plaintext = p.read()

            privateKey, publicKey = loadKeys()
            ciphertext = encrypt(plaintext, publicKey)
            signature = sign(plaintext, privateKey)

            with open('ciphertext.pkl', 'wb') as f:
                pickle.dump((ciphertext, signature), f)

            with open('ciphertext.pkl', 'rb') as f:
                with gzip.open('ciphertext.gz', 'wb') as g:
                    g.write(f.read())

            print('File encrypted and stored in ciphertext.pkl and ciphertext.gz')

        elif choice == '2':
            try:
                path = input('Enter path to zipped ciphertext file: ')
                with gzip.open(path, 'rb') as f:
                    ciphertext, signature = pickle.load(f)

                privateKey, publicKey = loadKeys()
                plaintext = decrypt(ciphertext, privateKey)
                verification = verify(plaintext, signature, publicKey)
                if plaintext and verification:
                    print('\nSuccessfully decrypted and stored in secret.txt\n')
                    with open('secret.txt', 'w') as s:
                        s.write('=============== SIGNATURE VERIFIED ===============\n\n')
                        s.write(plaintext)
                        s.write('\n=============== SIGNATURE VERIFIED ===============')
                else:
                    print('\nDecryption failed.\n')

            except FileNotFoundError:
                print('No encrypted data found.\n')

        elif choice == '3' or choice.lower() == 'exit':
            print('Thank you for using Pickle RSA')
            break

        else:
            print('Invalid choice.\n')


def yrsa():
    while True:
        print("Operation Modes:\n1. Encrypt and Sign\n2. Decrypt and Verify\n3. Go Back")
        choice = input('Choice: ')

        if choice == '1':
            path = input('Enter path to plaintext file: ')
            with open(path, 'r') as p:
                plaintext = p.read()

            privateKey, publicKey = loadKeys()
            ciphertext = encrypt(plaintext, publicKey)
            signature = sign(plaintext, privateKey)
            with open('ciphertext.txt', 'w') as f:
                yaml.dump({'Ciphertext': ciphertext, '\nSignature': signature}, f)

            print('File encrypted and stored in ciphertext.txt\n')

        elif choice == '2':
            try:
                path = input('Enter path to ciphertext file: ')
                with open(path, 'r') as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    ciphertext = data['Ciphertext']
                    signature = data['\nSignature']

                privateKey, publicKey = loadKeys()
                plaintext = decrypt(ciphertext, privateKey)
                verification = verify(plaintext, signature, publicKey)
                if plaintext and verification:
                    print('\nSuccessfully decrypted and stored in secret.txt\n')
                    with open('secret.txt', 'w') as s:
                        s.write('=============== SIGNATURE VERIFIED ===============\n\n')
                        s.write(plaintext)
                        s.write('\n=============== SIGNATURE VERIFIED ===============')
                else:
                    print('\nDecryption failed.\n')

            except FileNotFoundError:
                print('No encrypted data found.\n')

        elif choice == '3' or choice.lower() == 'exit':
            print('Thank you for using Yaml RSA')
            break

        else:
            print('Invalid choice.\n')


def main():
    while True:
        print('Welcome to RSA Encryption\nPlease choose your option:')
        print('1. Generate RSA Keys\n2. Zipped Pickled RSA\n3. YAML RSA\n4. Exit')
        typ_choice = input('Type (1/2/3/4): ')
        if typ_choice == '1':
            prsa()
        elif typ_choice == '2':
            yrsa()
        elif typ_choice == '3':
            generateKeys()
            print('Keys generated and stored in keys/publicKey.pem and keys/privateKey.pem\n')
        elif typ_choice == '4' or typ_choice.lower() == 'exit':
            print('Thank you for using this program. Goodbye!')
            break
        else:
            print('Invalid input')


if __name__ == "__main__":
    main()
