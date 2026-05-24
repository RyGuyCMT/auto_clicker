import os
from auto_clicker import Clicker_Main


def main():
    """Entry point for the auto-clicker application"""
    try:
        clicker = Clicker_Main()
        clicker.run()
    except BaseException:
        os.environ["PYTHONINSPECT"] = "1"
        raise


if __name__ == "__main__":
    main()
