# Pull a problem from project euler,
# save it with to a file with the desired programming
# language's file extension.
# when dumping into the file, it will be inserted with the
# comments of the language of choice.

import argparse
import os.path
from requests import Session, Request

from bs4 import BeautifulSoup

ACCEPTED_LANGUAGES = ['python', 'julia', 'haskell', 'cpp', 'java']

def parse_inputs() -> argparse.Namespace:
    """Grabs the inputs.
    """
    parser = argparse.ArgumentParser(
        description='Download and prepare a specified Project Euler problem.'
    )

    parser.add_argument(
        '--problem',
        type=int,
        action='store',
        help="Problem number you wish to download."
    )

    parser.add_argument(
        '--language',
        type=str,
        choices=ACCEPTED_LANGUAGES,
        action='store',
        help="Programming language you would like to use."
    )

    return parser.parse_args()

def fetch_problem_page(problem: int) -> str:
    """Grabs the html of the problem text from the internet.
    """

    session = Session()
    req = Request('GET', f'https://projecteuler.net/problem={problem}')
    prepped = session.prepare_request(req)
    response = session.send(prepped)

    match response.status_code:
        case 200:
            return response.text
        case 403:
            print("You probably need to log in. I dunno, I didn't think you could ever get a 403 here.")
        case _:
            raise RuntimeError("Something funky is going on.")

def extract_problem_text(problem_html: str) -> str:
    """Pull the problem text from the html and returns it
    as a list of strings where each string is another broken up line.
    """

    soup = BeautifulSoup(problem_html, features="html.parser")
    return soup.find_all('div', class_="problem_content")[0].text

def format_comment(language: str, problem_text: str) -> str:
    """Put the problem text in between multiline comments for
    selected language.
    """

    match language:
        case "python":
            return '"""' + problem_text + '"""\n'
        case "julia":
            return '#=' + problem_text + '=#\n'
        case "haskell":
            return '{-' + problem_text + '-}\n'
        case "cpp":
            return '/*' + problem_text + '*/\n'
        case "java":
            return '/*' + problem_text + '*/\n'
        case _:
            raise RuntimeError("Argparse should ensure that we never get here.")

def format_dest(language: str, problem: int) -> str:
    """Format the name of the file where the code will be stored.
    """

    match language:
        case "python":
            return f"p{str(problem)}.py"
        case "julia":
            return f"p{str(problem)}.jl"
        case "haskell":
            return f"p{str(problem)}.hs"
        case "cpp":
            return f"p{str(problem)}.cpp"
        case "java":
            return f"p{str(problem)}.java"
        case _:
            raise RuntimeError("Argparse should ensure that we never get here.")

if __name__ == '__main__':

    print("...")
    args = parse_inputs()
    problem_html = fetch_problem_page(args.problem)
    problem_text = extract_problem_text(problem_html)
    prepped_comment = format_comment(args.language, problem_text)
    dest = format_dest(args.language, args.problem)

    # verify that this does not already exists. Otherwise you could risk
    # saving over previous data.
    if os.path.isfile(dest):
        print("The specified problem is already downloaded!")
        exit(1)

    with open(dest, 'w', encoding='utf-8') as f:
        f.write(prepped_comment)

    print(f"Saved to {dest}")
