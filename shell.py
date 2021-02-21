import jimmy_script
import pyfiglet
from printy import printy


def print_notice():
    with open("banner_notice.txt") as f:
        lines = f.readlines()
        for line in lines:
            printy("{:^66}".format(line.strip()), "y")
        print()


def print_banner():
    banner = pyfiglet.figlet_format("Jimmy  Script")
    print(banner)
    print(" " + "-" * 65)
    print_notice()
    print(" " + "-" * 65)
    print()


if __name__ == "__main__":
    print_banner()
    while True:
        expr = input("jimmy-script > ")
        if expr.strip().lower() == "exit":
            print("Goodbye!")
            exit(0)

        result, error = jimmy_script.execute(expr, "<stdin>")
        if error:
            print(error)
        else:
            print(result) if result is not None else None
