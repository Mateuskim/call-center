from server import Server
from op import Operator

def main():
    operatorA = Operator('A')
    operatorB = Operator('B')
    Server().cmdloop()


if __name__ == '__main__':
    main()