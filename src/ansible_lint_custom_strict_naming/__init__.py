from enum import Enum
from pathlib import Path

from ansiblelint.app import get_app
from ansiblelint.constants import FILENAME_KEY
from ansiblelint.constants import LINE_NUMBER_KEY
from ansiblelint.file_utils import Lintable

base_name = "ansible-lint-custom-strict-naming"


class VarPrefixKind(Enum):
    arg = "arg"  # role's arguments
    const = "const"  # constants
    global_ = "global"  # global variables
    var = "var"  # dynamic variables


VarPrefixMap: dict[VarPrefixKind, tuple[str, ...]] = {
    VarPrefixKind.arg: ("arg", "a"),
    VarPrefixKind.const: ("const", "c"),
    VarPrefixKind.global_: ("global", "g"),
    VarPrefixKind.var: ("var", "v"),
}


class StrictFileType(Enum):
    PLAYBOOK_FILE = "playbook_file"
    TASKS_FILE = "tasks_file"  # "**/tasks/<some_tasks>.yml"
    ROLE_TASKS_FILE = "role_tasks"  # "roles/<role_name>/tasks/<role_task>.yml"
    UNKNOWN = "unknown"


def detect_strict_file_type(file: Lintable) -> StrictFileType | None:
    # Get current role name or task name
    match file.kind:
        case "playbook":
            return StrictFileType.PLAYBOOK_FILE
        case "tasks":
            roles_path = list(map(Path, get_app(cached=True).runtime.config.default_roles_path))
            if (
                role_candidate_path := file.path.resolve().parents[2]
            ) in roles_path or role_candidate_path.name == "roles":  # roles/<role_name>/tasks/<role_task>.yml
                return StrictFileType.ROLE_TASKS_FILE
            else:  # playbooks/tasks/some_task.yml
                return StrictFileType.TASKS_FILE
        case _:
            return StrictFileType.UNKNOWN


def get_role_name_from_role_tasks_file(file: Lintable) -> str:
    if detect_strict_file_type(file) != StrictFileType.ROLE_TASKS_FILE:
        err_msg = f"file kind is not role_tasks: {file.kind}"
        raise ValueError(err_msg)
    return f"{file.path.resolve().parents[1].name}"


def get_tasks_name_from_tasks_file(file: Lintable) -> str:
    return f"{file.path.stem}"


def is_registered_key(key: str) -> bool:
    return key in {
        FILENAME_KEY,
        LINE_NUMBER_KEY,
    }
