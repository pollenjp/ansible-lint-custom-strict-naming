import typing as t
from logging import NullHandler
from logging import getLogger
from pathlib import Path

from ansiblelint.constants import LINE_NUMBER_KEY
from ansiblelint.errors import MatchError
from ansiblelint.file_utils import Lintable
from ansiblelint.rules import AnsibleLintRule
from ansiblelint.utils import Task
from ansiblelint.yaml_utils import nested_items_path
from jinja2.environment import Environment

from ansible_lint_custom_strict_naming import StrictFileType
from ansible_lint_custom_strict_naming import VarPrefixKind
from ansible_lint_custom_strict_naming import VarPrefixMap
from ansible_lint_custom_strict_naming import base_name
from ansible_lint_custom_strict_naming import detect_strict_file_type
from ansible_lint_custom_strict_naming import get_role_name_from_role_tasks_file

logger = getLogger(__name__)
logger.addHandler(NullHandler())


ID = f"{base_name}<{Path(__file__).stem}>"
DESCRIPTION = """
Variables used in jinja template should have a prefix.
"""

UnmatchedType = bool | list[MatchError]


class VarNamePrefixInTemplate(AnsibleLintRule):
    id = ID
    description = DESCRIPTION
    tags: t.ClassVar[list[str]] = ["experimental"]  # pyright: ignore[reportIncompatibleVariableOverride]

    @t.override
    def matchtask(  # noqa: C901, PLR0912
        self,
        task: Task,
        file: Lintable | None = None,
    ) -> bool | list[MatchError]:
        if file is None:
            return False
        if (file_type := detect_strict_file_type(file)) is None:
            return False

        result: list[MatchError] = []
        # "playbook",
        # "rulebook",
        # "meta",  # role meta
        # "meta-runtime",
        # "tasks",  # includes pre_tasks, post_tasks
        # "handlers",  # very similar to tasks but with some specifics
        # # https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-roles-and-collections-from-the-same-requirements-yml-file
        # "requirements",
        # "role",  # that is a folder!
        # "yaml",  # generic yaml file, previously reported as unknown file type
        # "ansible-lint-config",
        # "sanity-ignore-file",  # tests/sanity/ignore file
        # "plugin",
        # "",  # unknown file type
        match file_type:
            case StrictFileType.PLAYBOOK_FILE:
                # TODO:
                return result
            case StrictFileType.ROLE_TASKS_FILE:
                # <role_name>__args.xxx.yyy
                # <role_name>__arg__<const|global|var>__
                role_name = get_role_name_from_role_tasks_file(file)
                # FIXME: ignore some values
                prefixes = ["ansible_", f"{role_name}__args", *[f"{role_name}__{p_}__" for p_ in VarPrefixMap[VarPrefixKind.arg]]]

                for _k, v, _path in nested_items_path(
                    data_collection=task,
                ):
                    if isinstance(v, str):
                        j2_env: Environment = Environment(trim_blocks=False)
                        is_in_block = False
                        is_first_var = True
                        for lineno, token_type, token_value in j2_env.lex(v):
                            match token_type:
                                case "variable_begin":
                                    is_in_block = True
                                case "variable_end":
                                    is_in_block = False
                                    is_first_var = True
                                case "name" if is_in_block and is_first_var:  # 変数名取得
                                    is_first_var = False
                                    if not any(token_value.startswith(prefix) for prefix in prefixes):
                                        result.append(
                                            self.create_matcherror(
                                                message="Variables used in role should have the following format: "
                                                + ", ".join([f"'{prefix}'" for prefix in prefixes])
                                                + ".",
                                                lineno=task.get(LINE_NUMBER_KEY) + lineno,
                                                filename=file,
                                                tag=ID,
                                            )
                                        )
                                case _:
                                    pass
                return result
            case _:
                return result
