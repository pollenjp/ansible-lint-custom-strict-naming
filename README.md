# ansible-lint-custom-strict-naming

[![PyPI](https://img.shields.io/pypi/v/ansible-lint-custom-strict-naming)](https://pypi.org/project/ansible-lint-custom-strict-naming/)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/ansible-lint-custom-strict-naming)](https://pypi.org/project/ansible-lint-custom-strict-naming/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Downloads](https://pepy.tech/badge/ansible-lint-custom-strict-naming)](https://pepy.tech/project/ansible-lint-custom-strict-naming)

Ansible is a powerful tool for configuration management.
But it is difficult to maintain the YAML playbook quality.
Variable maintenance is one of the difficult tasks because they can be overwritten unexpectedly,
if you don't care about such like [precedence](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence) and position where variables are defined.

This is a strict rule for variable naming, using [ansible-lint](https://github.com/ansible/ansible-lint).
Strict naming rule is useful to avoid name collision and to search defined position.

## Rules

### var_name_prefix

- [x] `<role_name>_role__` , `<task_name>_tasks__`

  - | prefix                | Variables defined in       |
    | :-------------------- | :------------------------- |
    | `<role_name>_role__`  | `roles/<role_name>/tasks/` |
    | `<role_name>_tasks__` | `<not_roles>/**/tasks/`    |

  - In ansible-lint, `var-naming[no-role-prefix]` require to use `<role_name>_` as prefix. But it is not enough to avoid name collision or search defined position. So, I add `_role__` or `_tasks__` to the prefix.

- [ ] `var__`, `const__`
  - | prefix    | description                                                                             |
    | :-------- | :-------------------------------------------------------------------------------------- |
    | `var__`   | Variables dynamically defined by `ansible.builtin.set_fact` or `register`               |
    | `const__` | Variables statistically defined in such like inventory's vars, group_vars and host_vars |
- [ ] prefix precedence

  - descending order
    - role or task prefix
    - var or const prefix
  - examples

    | var                       | description                                                                                               |
    | :------------------------ | :-------------------------------------------------------------------------------------------------------- |
    | `var__fizz`               | defined in playbook by `ansible.builtin.set_fact` or `register`                                           |
    | `some_role__var__fizz`    | defined in `roles/<role_name>/tasks` by `ansible.builtin.set_fact` or `register`                          |
    | `some_role__arg__fizz`    | defined by `ansible.builtin.include_role`'s `vars` key and shouldn't changed in `roles/<role_name>/tasks` |
    | `some_role__const__fizz`  | defined only in `roles/<role_name>/vars/`.                                                                |
    | `some_tasks__var__fizz`   | defined in `tasks` by `ansible.builtin.set_fact` or `register`                                            |
    | `some_tasks__const__fizz` | defined by `ansible.builtin.include_role`'s vars key and not changed in `tasks`                           |

    ```yaml
    tasks:
      - name: Some task
        ansible.builtin.include_role:
          name: <role_name>
        vars:
          some_role__const__one: value1
          some_role__const__two: value2
    ```

## Others

### Double underscores?

- Single underscore (`_`) is used to separate words. Double underscores (`__`) are used to separate chunks for readability.
- examples
  - `var__send_message__user_id`
  - `var__send_message__content`
  - `some_role__const__app_config__name`
  - `some_role__const__app_config__token`
  - `some_role__const__app_config__version`
