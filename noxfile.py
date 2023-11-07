# Standard Library
import typing as t
from pathlib import Path

# Third Party Library
import nox
from nox.sessions import Session

src_dir: Path = Path(__file__).parent / "src"
python_code_path_list: t.List[str] = [
    f"{src_dir}",
    "noxfile.py",
]
assert all(isinstance(path, str) for path in python_code_path_list)
env_common: dict[str, str] = {
    "PYTHONPATH": f"{src_dir}",
}
nox_tmp_dir: Path = Path(__file__).parent / ".nox_tmp"
python_version_list: list[str] = ["3.11"]


class SessionKwargs(t.TypedDict, total=False):
    env: dict[str, str]
    success_codes: list[int]


def install_requirements(session: Session, dev: bool = False) -> None:
    session.install("--upgrade", "pip")
    session.run("pip", "-V")
    session.install("-r", f"requirements{'-dev' if dev else ''}.lock")


def load_requirements_dict(dev: bool = False) -> dict[str, str]:
    requirements_txt = Path(f"requirements{'-dev' if dev else ''}.lock")
    requirements_dict = {}
    with open(requirements_txt, "rt") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(("#", "-")):
                continue
            package, version = line.split("==")
            requirements_dict[package] = version
    return requirements_dict


@nox.session(python=python_version_list)
def format(session: Session) -> None:
    env: dict[str, str] = {}
    env.update(env_common)
    kwargs: SessionKwargs = {"env": env, "success_codes": [0, 1]}

    install_requirements(session)
    requirements_dev_dict = load_requirements_dict(dev=True)
    packages = ["autoflake8", "isort", "black"]
    session.install(*[f"{package}=={requirements_dev_dict[package]}" for package in packages])
    session.run(
        "autoflake8",
        "--in-place",
        "--recursive",
        "--remove-unused-variables",
        "--in-place",
        "--exit-zero-even-if-changed",
        *python_code_path_list,
        **kwargs,
    )
    session.run("isort", *python_code_path_list, **kwargs)
    session.run("black", *python_code_path_list, **kwargs)


@nox.session(python=python_version_list)
def lint(session: Session) -> None:
    env: dict[str, str] = {}
    env.update(env_common)
    kwargs: SessionKwargs = {"env": env}

    install_requirements(session, dev=True)  # mypy may require dev packages

    session.run("flake8", "--statistics", "--count", "--show-source", *python_code_path_list, **kwargs)
    session.run("autoflake8", "--check", "--recursive", "--remove-unused-variables", *python_code_path_list, **kwargs)
    session.run("isort", "--check", *python_code_path_list, **kwargs)
    session.run("black", "--check", *python_code_path_list, **kwargs)
    session.run("mypy", "--check", "--no-incremental", *python_code_path_list, **kwargs)


@nox.session(python=python_version_list)
def test(session: Session) -> None:
    env: dict[str, str] = {}
    env.update(env_common)
    kwargs: SessionKwargs = {"env": env}

    install_requirements(session)
    requirements_dev_dict = load_requirements_dict(dev=True)
    packages = ["pytest"]
    session.install(*[f"{package}=={requirements_dev_dict[package]}" for package in packages])

    session.run("pytest", **kwargs)
