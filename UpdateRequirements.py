import logging
from operator import contains
import os
import sys


try:
    import pipreqs.pipreqs as pipreqs
    import piptools.scripts.compile as pipCompile
except ImportError:
    print(
        "pipreqs, piptools or requests are not installed. Please install them using 'pip install pipreqs piptools requests'"
    )


def main(args: list[str]):
    encoding: str = (
        args[args.index("--encoding") + 1] if contains(args, "--encoding") else "utf-8"
    )

    candidates = pipreqs.get_pkg_names(
        pipreqs.get_all_imports(
            os.path.abspath(os.curdir),
            encoding=encoding,
        )
    )
    candidates.remove("pipreqs")
    candidates.remove("piptools")

    local = pipreqs.get_import_local(candidates, encoding=encoding)
    # check if candidate name is found in
    # the list of exported modules, installed locally
    # and the package name is not in the list of local module names
    # it add to difference
    difference = [
        candidate
        for candidate in candidates
        if candidate.lower()
        not in [y for candidate in local for y in candidate["exports"]]
        and candidate.lower() not in [candidate["name"] for candidate in local]
    ]
    
    # sort imports based on lowercase name of package, similar to `pip freeze`.
    imports = sorted(
        local + pipreqs.get_imports_info(difference), key=lambda x: x["name"].lower()
    )

    pipreqs.generate_requirements_file("requirements.in", imports, "~=")


class WithoutStdout:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr


if __name__ == "__main__":
    with WithoutStdout():
        logging.disable()
        main(sys.argv)
        pipCompile.cli()
