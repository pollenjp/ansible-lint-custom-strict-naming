# Standard Library
import typing as t
from logging import NullHandler
from logging import getLogger
from pathlib import Path

# Third Party Library
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.utils import Task

# First Party Library
from ansible_lint_custom_strict_naming import StrictFileType
from ansible_lint_custom_strict_naming import base_name
from ansible_lint_custom_strict_naming import detect_strict_file_type
from ansible_lint_custom_strict_naming import get_role_name_from_role_tasks_file
from ansible_lint_custom_strict_naming import get_tasks_name_from_tasks_file

logger = getLogger(__name__)
logger.addHandler(NullHandler())

prefix_format = ""

# ID = f"{base_name}<{Path(__file__).stem}>"
ID = f"{base_name}<{Path(__file__).stem}>"
DESCRIPTION = """
Variables defined by register should have a prefix,
like 'var__', '<role_name>_role__var__', or '<tasks_name>_tasks__var__'.
"""


class RegisterPrefix(AnsibleLintRule):
    id = ID
    description = DESCRIPTION
    tags: t.ClassVar[list[str]] = ["formatting"]  # pyright: ignore[reportIncompatibleVariableOverride]

    def matchtask(self, task: Task, file: Lintable | None = None) -> bool | str:
        if (task_result := task.get("register")) is None:
            return False

        if file is None:
            return False
        if (file_type := detect_strict_file_type(file)) is None:
            return False

        prefix: str
        match file_type:
            case StrictFileType.PLAYBOOK_FILE:
                prefix = "var__"
            case StrictFileType.ROLE_TASKS_FILE:
                prefix = f"{get_role_name_from_role_tasks_file(file)}_role__var__"
            case StrictFileType.TASKS_FILE:
                prefix = f"{get_tasks_name_from_tasks_file(file)}_tasks__var__"
            case StrictFileType.UNKNOWN:
                return False

        if not task_result.startswith(prefix):
            return f"Variables defined by 'register' should have a '{prefix}' prefix."

        return False
