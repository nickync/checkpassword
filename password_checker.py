import requests
import hashlib
import pandas as pd
import sys

# hashing the passoword
def hashed_password(password):
    password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()   
    global first5, remaining
    first5, remaining = password[:5], password[5:]
    # remaining = password[5:]
    return create_dataset(first5)
    
# creating result dataset
def create_dataset(first5):
    response = requests.get('https://api.pwnedpasswords.com/range/'+ first5)
    if response.status_code == 200:
        data = {'hash':[line.split(':')[0] for line in response.text.splitlines()],
                'count':[line.split(':')[-1] for line in response.text.splitlines()]}
        global dataset
        dataset = pd.DataFrame(data)
        return dataset
    else:
        return print(f'error {response.status_code}')
        
# checking pwned result
def check_pwned(password):
    hashed_password(password)
    for hash in dataset.iloc[:,0]:
        if hash == remaining:
            count = dataset.loc[dataset['hash'] == hash, 'count'].values
            return print(f'Your password has been found {int(count)} times. Change it!!! Dumbass!!!')

    else:
        print('Great. Your password is safe and sound.')

# check multiple passwords
def main(passwords):
    for password in passwords:
        check_pwned(password)


main(sys.argv[1:])