import jimmy_script

if __name__ == "__main__":
    while True:
        expr = input("jimmy-script > ")
        result, error = jimmy_script.execute(expr, "<stdin>")
        if error:
            print(error)
        else:
            print(result)
