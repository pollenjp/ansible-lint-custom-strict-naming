# # Third Party Library
# from ansiblelint.file_utils import Lintable
# from ansiblelint.rules import AnsibleLintRule
# from ansiblelint.utils import Task


# class TaskHasTag(AnsibleLintRule):
#     """Tasks must have tag."""

#     id = "ansible-lint-custom-strict-naming_task-has-tag"
#     description = "Tasks must have tag"
#     tags = ["productivity"]

#     def matchtask(self, task: Task, file: Lintable | None = None) -> bool | str:
#         # If the task include another task or make the playbook fail
#         # Don't force to have a tag
#         if not set(task.keys()).isdisjoint(["include", "fail"]):
#             return False

#         if "tags" not in task:
#             return True

#         return False
