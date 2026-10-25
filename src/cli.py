import argparse
import json
import sys

def parse_arguments():
    """
    Parses command-line arguments for the Vantage application.
    Returns the parsed arguments object.
    """
    parser = argparse.ArgumentParser(
        prog="vantage",
        description="Vantage: Instant network data retrieval and geolocation."
    )

    # Adding an optional argument for a specific IP.
    # If left blank, your API will likely check the user's current IP.
    parser.add_argument(
        "-i", "--ip",
        type=str,
        help="Target IP address to inspect. Leave blank to check your own network.",
        default=None
    )

    return parser.parse_args()


def display_result(data: dict):
    """
    Formats and prints the successful API response as clean, readable JSON.
    """
    # The indent=4 ensures the terminal output is human-readable
    formatted_json = json.dumps(data, indent=4)
    print(formatted_json)


def display_error(error_message: str):
    """
    Handles terminal output for errors, sending them to standard error (stderr).
    """
    print(f"Vantage Error: {error_message}", file=sys.stderr)