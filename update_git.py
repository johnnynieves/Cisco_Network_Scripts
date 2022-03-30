import os
from getpass import getpass


def main():

    user = 'johnny.nieves@live.com'
    name = 'johnnynieves'
    os.system(f'git config --global user.email "{user}"')
    os.system(f'git config --global user.name "{name}"')
    
    os.system('git status')
    os.system('git add .')
    os.system('git status')
    comment = input('Please enter your update comment: ')
    os.system(f'git commit -m "{comment}"')
    os.system('git push')


if __name__ == "__main__":
    main()
