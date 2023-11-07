# Standard Library
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

logger = getLogger(__name__)
logger.addHandler(NullHandler())

prefix_format = ""

# ID = f"{base_name}<{Path(__file__).stem}>"
ID = f"{base_name}<{Path(__file__).stem}>"
DESCRIPTION = """
Variables in roles or tasks should have a `<role_name>_role__` or `<role_name>_tasks__` prefix.
"""


class VarNamePrefix(AnsibleLintRule):
    id = ID
    description = DESCRIPTION
    tags = ["productivity"]

    def matchtask(self, task: Task, file: Lintable | None = None) -> bool | str:
        match task.action:
            case "ansible.builtin.set_fact":
                return match_task_for_set_fact_module(task, file)
            case _:
                return False


def match_task_for_set_fact_module(task: Task, file: Lintable | None = None) -> bool | str:
    """`ansible.builtin.set_fact`"""
    if file is None:
        return False
    if (file_type := detect_strict_file_type(file)) is None:
        return False

    match file_type:
        case StrictFileType.ROLE_TASKS_FILE:
            return match_tasks_for_role_tasks_file(task, file) or False
        case StrictFileType.TASKS_FILE:
            return match_tasks_for_tasks_file(task, file) or False
        case _:
            raise NotImplementedError


def match_tasks_for_role_tasks_file(task: Task, file: Lintable) -> str | None:
    prefix_format = f"{file.path.parents[1].name}_role__"
    for key in task.args.keys():
        if not key.startswith(prefix_format):
            return f"Variables in role should have a `{prefix_format}` prefix."
    return None


def match_tasks_for_tasks_file(task: Task, file: Lintable) -> str | None:
    # roles/<role_name>/tasks/<some_tasks>.yml
    prefix_format = f"{file.path.stem}_tasks__"
    for key in task.args.keys():
        if not key.startswith(prefix_format):
            return f"Variables in role should have a `{prefix_format}` prefix."
    return None
