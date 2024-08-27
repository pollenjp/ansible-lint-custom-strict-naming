# Standard Library
from enum import Enum

# Third Party Library
from ansiblelint.constants import FILENAME_KEY
from ansiblelint.constants import LINE_NUMBER_KEY
from ansiblelint.file_utils import Lintable

base_name = "ansible-lint-custom-strict-naming"


class StrictFileType(Enum):
    PLAYBOOK_FILE = "playbook_file"
    TASKS_FILE = "tasks_file"  # "**/tasks/<some_tasks>.yml"
    ROLE_TASKS_FILE = "role_tasks"  # "roles/<role_name>/tasks/<some_tasks>.yml"
    UNKNOWN = "unknown"


def detect_strict_file_type(file: Lintable) -> StrictFileType | None:
    # Get current role name or task name
    match file.kind:
        case "playbook":
            return StrictFileType.PLAYBOOK_FILE
        case "tasks":
            if file.path.parents[2].name == "roles":  # roles/<role_name>/tasks/<some_tasks>.yml
                return StrictFileType.ROLE_TASKS_FILE
            else:  # playbooks/tasks/some_task.yml
                return StrictFileType.TASKS_FILE
        case _:
            return StrictFileType.UNKNOWN


def get_role_name_from_role_tasks_file(file: Lintable) -> str:
    return f"{file.path.parents[1].name}"


def get_tasks_name_from_tasks_file(file: Lintable) -> str:
    return f"{file.path.stem}"


def is_registered_key(key: str) -> bool:
    return key in {
        FILENAME_KEY,
        LINE_NUMBER_KEY,
    }
