import typing as t
from logging import NullHandler
from logging import getLogger
from pathlib import Path

from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.utils import Task

from ansible_lint_custom_strict_naming import StrictFileType
from ansible_lint_custom_strict_naming import VarPrefixKind
from ansible_lint_custom_strict_naming import VarPrefixMap
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
    version_changed: t.ClassVar[str] = "24.10.0"  # pyright: ignore[reportIncompatibleVariableOverride]

    @t.override
    def matchtask(self, task: Task, file: Lintable | None = None) -> bool | str:
        register_val: str | None
        if (register_val := task.get("register")) is None:
            return False

        if file is None:
            return False
        if (file_type := detect_strict_file_type(file)) is None:
            return False

        prefixes: list[str]
        prefix_kind = VarPrefixKind.var
        match file_type:
            case StrictFileType.PLAYBOOK_FILE:
                prefixes = [f"{p_}__" for p_ in VarPrefixMap[prefix_kind]]
            case StrictFileType.ROLE_TASKS_FILE:
                prefixes = [f"{get_role_name_from_role_tasks_file(file)}_role__{p_}__" for p_ in VarPrefixMap[prefix_kind]]
            case StrictFileType.TASKS_FILE:
                prefixes = [f"{get_tasks_name_from_tasks_file(file)}_tasks__{p_}__" for p_ in VarPrefixMap[prefix_kind]]
            case StrictFileType.UNKNOWN:
                return False

        if all(not register_val.startswith(prefix) for prefix in prefixes):
            # if does not meet any of the prefixes, return error message
            return "Variables defined by 'register' should have one of the following prefixes: " + ", ".join(prefixes)

        return False
