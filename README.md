# ansible-lint-custom-strict-naming

## Rules

### var_name_prefix

- [x] `<role_name>_role__` , `<task_name>_task__`

  - | prefix                | Variables defined in |
    | :-------------------- | :------------------- |
    | `<role_name>_role__`  | `roles/tasks/`       |
    | `<role_name>_tasks__` | `<not_roles>/tasks/` |

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

    | var                       | description                                                                           |
    | :------------------------ | :------------------------------------------------------------------------------------ |
    | `var__fizz`               | defined in playbook by `ansible.builtin.set_fact` or `register`                       |
    | `some_role__var__fizz`    | defined in `roles/tasks` by `ansible.builtin.set_fact` or `register`                  |
    | `some_role__const__fizz`  | defined by `ansible.builtin.include_role`'s vars key and not changed in `roles/tasks` |
    | `some_tasks__var__fizz`   | defined in `tasks` by `ansible.builtin.set_fact` or `register`                        |
    | `some_tasks__const__fizz` | defined by `ansible.builtin.include_role`'s vars key and not changed in `tasks`       |

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

### Why double underscores?

- Single underscore (`_`) is used to separate words. Double underscores (`__`) are used to separate chunks for readability.
- examples
  - `var__send_message__user_id`
  - `var__send_message__content`
  - `some_role__const__app_config__name`
  - `some_role__const__app_config__token`
  - `some_role__const__app_config__version`
