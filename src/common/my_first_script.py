import logging

logging.getLogger().setLevel(logging.DEBUG)

from . import config


def _my_first_script(argA, argB):
    return {
        "argA": argA,
        "argB": argB,
    }


def main():
    import argparse

    script_parser = argparse.ArgumentParser(
        prog="my_first_script",
        description="my_first_script script",
    )

    script_parser.add_argument(
        "-a",
        "--argA",
        action="store",
        metavar="arg1",
        help="my_first_script argA",
        required=True,
    )

    script_parser.add_argument(
        "-b",
        "--argB",
        action="store",
        metavar="color",
        help="my_first_script color",
        required=True,
    )

    result = _my_first_script(**vars(script_parser.parse_args()))

    # Example how to access config toml file
    logging.debug(config)

    # Using **vars() to convert Namespace to dict
    logging.debug(result)

    return result


if __name__ == "__main__":
    main()
