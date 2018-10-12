import argparse

def get_args(arg_input = None):
    """
    Gets the arguments for the rocks-quarry server. By default pulls from
    argv, but may use a user-provided list.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", help = "The port on which to listen", type = int, default = 80)
    parser.add_argument("--data-dir", help = "The location at which to persist data", type = str, default="./data")
    return parser.parse_args(arg_input)
