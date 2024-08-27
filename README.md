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

## var_name_prefix

### `<role_name>_role__` , `<task_name>_tasks__`

- | prefix                | Variables defined in       |
  | :-------------------- | :------------------------- |
  | `<role_name>_role__`  | `roles/<role_name>/tasks/` |
  | `<role_name>_tasks__` | `<not_roles>/**/tasks/`    |

- In ansible-lint, `var-naming[no-role-prefix]` require to use `<role_name>_` as prefix. But it is not enough to avoid name collision or search defined position. So, I add `_role__` or `_tasks__` to the prefix.

### `var__`, `const__`

- `var__` prefix
  - Variables dynamically defined by `ansible.builtin.set_fact` or `register`
- `const__` prefix
  - Variables dynamically defined by `ansible.builtin.set_fact` or `register`
  - Variables statically defined in such like inventory's vars, group_vars, host_vars and etc.

### Vars in `tasks/<name>.yml` or `roles/<name>/tasks/main.yml`

- `<name>_role__var__` prefix
  - These variables are dynamically defined in `roles/<name>/tasks/main.yml`.
- `<name>_role__const__` prefix
  - These variables are defined in `roles/<name>/vars/main.yml` and shouldn't be changed dynamically.
- `some_role__arg__` prefix
  - These variables are defined by `ansible.builtin.include_role`'s `vars` key and shouldn't be changed dynamically.
- `some_role__args`

  - These variables are defined by `ansible.builtin.include_role`'s `vars` key and shouldn't be changed dynamically.

    ```yaml
    - name: Sample
      ansible.builtin.include_role:
        name: some_role
      vars:
        some_role__arg__key1: value1
        some_role__arg__key2: value2
    ```

  - This is useful when you want to send vars as dict.

    ```yaml
    - name: Sample
      ansible.builtin.include_role:
        name: some_role
      vars:
        some_role__args:
          key1: value1
          key2: value2
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

## Docs

### Articles

- [ansible-lint のカスタムルールを利用して Ansible 内での変数命名規則を縛ってみた話](https://zenn.dev/pollenjp/articles/2023-12-03-ansible-lint-custom-strict-naming)
