# Standard Library
from enum import Enum

# Third Party Library
from ansiblelint.file_utils import Lintable

base_name = "ansible-lint-custom-strict-naming"


class StrictFileType(Enum):
    TASKS_FILE = "tasks_file"  # "**/tasks/<some_tasks>.yml"
    ROLE_TASKS_FILE = "role_tasks"  # "roles/<role_name>/tasks/<some_tasks>.yml"


def detect_strict_file_type(file: Lintable) -> StrictFileType | None:
    # Get current role name or task name
    match file.kind:
        case "tasks":
            if file.path.parents[2] == "roles":  # roles/<role_name>/tasks/<some_tasks>.yml
                return StrictFileType.ROLE_TASKS_FILE
            else:  # playbooks/tasks/some_task.yml
                return StrictFileType.TASKS_FILE
        case _:
            return None
