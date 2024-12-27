import re
import typing as t
from logging import NullHandler
from logging import getLogger
from pathlib import Path

from ansiblelint.constants import LINE_NUMBER_KEY
from ansiblelint.errors import MatchError
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
from ansible_lint_custom_strict_naming import is_registered_key

logger = getLogger(__name__)
logger.addHandler(NullHandler())

ID = f"{base_name}<{Path(__file__).stem}>"
DESCRIPTION = """
Variables in roles or tasks should have a `<role_name>_role__` or `<role_name>_tasks__` prefix.
"""

UnmatchedType = bool | list[MatchError]


class VarNamePrefix(AnsibleLintRule):
    id = ID
    description = DESCRIPTION
    tags: t.ClassVar[list[str]] = ["formatting"]  # pyright: ignore[reportIncompatibleVariableOverride]

    @t.override
    def matchtask(self, task: Task, file: Lintable | None = None) -> UnmatchedType:
        match task.action:
            case "ansible.builtin.set_fact":
                return self._match_task_for_set_fact_module(task, file)
            case "ansible.builtin.include_role":
                return self._match_task_for_include_role_module(task, file)
            case "ansible.builtin.include_tasks":
                return self._match_task_for_include_tasks_module(task, file)
            case _:
                return False

    def _match_task_for_set_fact_module(self, task: Task, file: Lintable | None = None) -> bool | list[MatchError]:
        """`ansible.builtin.set_fact`"""
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
                # roles/<role_name>/tasks/<role_task>.yml
                prefixes = [f"{get_role_name_from_role_tasks_file(file)}_role__{p_}__" for p_ in VarPrefixMap[prefix_kind]]
            case StrictFileType.TASKS_FILE:
                # <not_roles>/**/tasks/<some_tasks>.yml
                prefixes = [f"{get_tasks_name_from_tasks_file(file)}_tasks__{p_}__" for p_ in VarPrefixMap[prefix_kind]]
            case StrictFileType.UNKNOWN:
                return False

        return [
            self.create_matcherror(
                message="Variables in 'set_fact' should have the following format: " + ", ".join(prefixes) + ".",
                lineno=task.get(LINE_NUMBER_KEY),
                filename=file,
            )
            for key in task.args.keys()
            if not any(key.startswith(prefix) for prefix in prefixes)
        ]

    def _match_task_for_include_role_module(self, task: Task, file: Lintable | None = None) -> bool | list[MatchError]:
        """`ansible.builtin.include_role`'s vars"""

        if (task_vars := task.get("vars")) is None:
            return False
        if (role_name := task.args.get("name")) is None:
            return False

        # check vars
        prefix_kind = VarPrefixKind.arg
        regexes = [re.compile(f"^{role_name}_role__args$")] + [re.compile(f"^{role_name}_role__{p_}__[a-z0-9_]+") for p_ in VarPrefixMap[prefix_kind]]

        def validate_key_name(key: str):
            """keyが条件を満たすか"""
            if is_registered_key(key):
                return True
            if any(reg.match(key) is not None for reg in regexes):
                return True
            return False

        return [
            self.create_matcherror(
                message="Variable name in 'include_role' should have the following format: " + ", ".join(regex.pattern for regex in regexes) + ".",
                lineno=task_vars.get(LINE_NUMBER_KEY),
                filename=file,
            )
            for key in task_vars.keys()
            if not validate_key_name(key)
        ]

    def _match_task_for_include_tasks_module(self, task: Task, file: Lintable | None = None) -> bool | list[MatchError]:
        """`ansible.builtin.include_tasks`'s vars"""

        if (task_vars := task.get("vars")) is None:
            return False
        if (role_name := task.args.get("name")) is None:
            return False

        # check vars
        prefix_kind = VarPrefixKind.arg
        regexes = [re.compile(f"^{role_name}_tasks__args$")] + [re.compile(f"^{role_name}_tasks__{p_}__[a-z0-9_]+") for p_ in VarPrefixMap[prefix_kind]]

        def validate_key_name(key: str):
            """keyが条件を満たすか"""
            if is_registered_key(key):
                return True
            if any(reg.match(key) is not None for reg in regexes):
                return True
            return False

        return [
            self.create_matcherror(
                message="Variable name in 'include_tasks' should have the following format: " + ", ".join(regex.pattern for regex in regexes) + ".",
                lineno=task_vars.get(LINE_NUMBER_KEY),
                filename=file,
            )
            for key in task_vars.keys()
            if not validate_key_name(key)
        ]
