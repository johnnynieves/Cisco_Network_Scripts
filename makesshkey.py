#!/bin/usr/env python3
from os import system


def main():
    print('#' * 20 + ' Making you ssh key ' + '#' * 20 + '\n')
    print('I will need some info from you before i can make your ssh keys\n')
    selection = int(input('Please enter type of key: 0 rsa | 1 ed25519: '))
    if not selection:
        make_key("rsa")
    elif selection:
        make_key("ed25519")


def make_key(key_type):
    random_ness = int(
        input('Please enter a random number between 50 and 1000: '))
    save_location = input(
        'Where would you like to save your keys: [Press "Enter" for Default .ssh/]')
    account = input('Account name ie. "you@outlook.com" or "you@github.com" ')

    if save_location == '':
        save_location = f'~/.ssh/{key_type}'
    else:
        save_location = f'{save_location}/{key_type}'
    system(
        f'ssh-keygen -b 4096 -a {random_ness} -t {key_type} -f {save_location} -C {account}')


if __name__ == "__main__":
    main()
