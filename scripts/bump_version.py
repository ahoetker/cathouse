import toml
import typer
from semantic_version import Version

import re
from enum import Enum
from pathlib import Path


class Increment(str, Enum):
    major = "major"
    minor = "minor"
    patch = "patch"


def get_current_version() -> Version:
    with open("pyproject.toml", "r") as f:
        pyproject_data = toml.load(f)
        return Version(pyproject_data["tool"]["poetry"]["version"])


def get_next_version(current_version: Version, increment: Increment) -> Version:
    if increment == Increment.major:
        next_version = current_version.next_major()
    elif increment == Increment.minor:
        next_version = current_version.next_minor()
    else:
        next_version = current_version.next_patch()

    return next_version


def bump_pyproject_version(next_version: Version) -> None:
    with open("pyproject.toml", "r") as f:
        pyproject_data = toml.load(f)

    pyproject_data["tool"]["poetry"]["version"] = str(next_version)
    with open("pyproject.toml", "w") as f:
        toml.dump(pyproject_data, f)


def bump_helm_chart_version(next_version: Version, chart: Path) -> None:
    with chart.open("r") as f:
        lines = f.readlines()

    chart_version_expr = re.compile(r"^version: (\S+.\S+.\S+)")
    app_version_expr = re.compile(r"^appVersion: \"(\S+.\S+.\S+)\"")

    # Parse line-by-line to avoid mangling commented YAML
    for n, line in enumerate(lines):
        match_chart_version = chart_version_expr.match(line)
        match_app_version = app_version_expr.match(line)
        if match_chart_version is not None:
            current_version = match_chart_version[1]
            lines[n] = f"version: {str(next_version)}"
            print(f"Bumped chart version from {current_version} to {next_version}")
        elif match_app_version is not None:
            current_version = match_app_version[1]
            lines[n] = f"appVersion: \"{str(next_version)}\""
            print(f"Bumped chart appVersion from {current_version} to {next_version}")

    with chart.open("w") as f:
        f.writelines(lines)


def main(increment: Increment = Increment.patch, dry_run: bool = False):
    current_version = get_current_version()
    next_version = get_next_version(current_version, increment)
    print(f"Current Version: {current_version}")
    print(f"Proposed Version: {next_version}")

    chart_file = Path("kubernetes/helm/cathouse/Chart.yaml")

    if dry_run is False:
        bump_pyproject_version(next_version)
        print("Bumped package version in pyproject.toml")
        bump_helm_chart_version(next_version, chart_file)
        print(f"Bumped package version in {str(chart_file)}")


if __name__ == "__main__":
    typer.run(main)
