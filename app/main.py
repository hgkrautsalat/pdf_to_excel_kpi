from time import sleep

def test_function() -> None:
    print("This is a test function.")
    sleep(10)
    print("Test function completed.")
    sleep(1)
    return None


def main() -> None:
    # check_update()
    test_function()
    return None


if __name__=="__main__":
    main()
