# project-euler-problem-fetcher

Grabs project euler problems and saves them into a file in the current directory.
The project text will be found at the top of the file nested amidst a multiline
comment block of your specified language.

# Usage
```
usage: fetch_problem.py [-h] [--problem PROBLEM] [--language {python,julia,haskell,cpp,java}]

Download and prepare a specified Project Euler problem.

options:
  -h, --help            show this help message and exit
  --problem PROBLEM     Problem number you wish to download.
  --language {python,julia,haskell,cpp,java}
                        Programming language you would like to use
```

# Contributing
Adding support for your own lanugage is easy.

1. Add the langauge name to `ACCEPTED_LANGUAGES`.

2. Add a case in `format_comment` that formats the multiline comment for the desired language.

3. Add a case in `format_dest` that formats the filenam for the desired language.
