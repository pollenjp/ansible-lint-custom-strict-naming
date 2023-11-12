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
from ansible_lint_custom_strict_naming import get_role_name_from_role_tasks_file
from ansible_lint_custom_strict_naming import get_tasks_name_from_tasks_file

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
            case "ansible.builtin.include_role":
                return match_task_for_include_role_module(task, file)
            case "ansible.builtin.include_tasks":
                return match_task_for_include_tasks_module(task, file)
            case _:
                return False


def match_task_for_set_fact_module(task: Task, file: Lintable | None = None) -> bool | str:
    """`ansible.builtin.set_fact`"""
    if file is None:
        return False
    if (file_type := detect_strict_file_type(file)) is None:
        return False

    prefix: str
    match file_type:
        case StrictFileType.PLAYBOOK_FILE:
            prefix = "var__"
        case StrictFileType.ROLE_TASKS_FILE:
            # roles/<role_name>/tasks/<some_tasks>.yml
            prefix = f"{get_role_name_from_role_tasks_file(file)}_role__var__"
        case StrictFileType.TASKS_FILE:
            # <not_roles>/**/tasks/<some_tasks>.yml
            prefix = f"{get_tasks_name_from_tasks_file(file)}_tasks__var__"
        case StrictFileType.UNKNOWN:
            return False

    for key in task.args.keys():
        if not key.startswith(prefix):
            return f"Variables should have a '{prefix}' prefix."
    return False


def match_task_for_include_role_module(task: Task, file: Lintable | None = None) -> bool | str:
    """`ansible.builtin.include_role`'s vars"""

    if (task_vars := task.get("vars")) is None:
        return False
    if (role_name := task.args.get("name")) is None:
        return False

    # check vars
    prefix = f"{role_name}_role__arg__"
    for key in task_vars.keys():
        if not key.startswith(f"{prefix}"):
            return f"Variables in 'include_role' should have a '{prefix}' prefix."
    return False


def match_task_for_include_tasks_module(task: Task, file: Lintable | None = None) -> bool | str:
    """`ansible.builtin.include_tasks`'s vars"""

    if (task_vars := task.get("vars")) is None:
        return False
    if (role_name := task.args.get("name")) is None:
        return False

    # check vars
    prefix = f"{role_name}_tasks__arg__"
    for key in task_vars.keys():
        if not key.startswith(f"{prefix}"):
            return f"Variables in 'include_tasks' should have a '{prefix}' prefix."
    return False
