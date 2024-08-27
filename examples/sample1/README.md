# sample1

## sample output

```sh
make lint
```

```log.txt
ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'var__' prefix.
playbooks/debug.yml:8 Task/Handler: Set vars (playbooks/)

fqcn[action-core]: Use FQCN for builtin module actions (set_fact).
playbooks/debug.yml:11 Use `ansible.builtin.set_fact` or `ansible.legacy.set_fact` instead.

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'var__' prefix.
playbooks/debug.yml:14 Task/Handler: Set vars (playbooks/)

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_role__var__' prefix.
playbooks/roles/sample/tasks/main.yml:2 Task/Handler: Set vars (roles/)

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_role__var__' prefix.
playbooks/roles/sample/tasks/main.yml:5 Task/Handler: Set vars (roles/)

fqcn[action-core]: Use FQCN for builtin module actions (set_fact).
playbooks/roles/sample/tasks/main.yml:8 Use `ansible.builtin.set_fact` or `ansible.legacy.set_fact` instead.

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_role__var__' prefix.
playbooks/roles/sample/tasks/main.yml:11 Task/Handler: Set vars (roles/)

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_tasks__var__' prefix.
playbooks/tasks/sample.yml:2 Task/Handler: Set vars (tasks/)

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_tasks__var__' prefix.
playbooks/tasks/sample.yml:5 Task/Handler: Set vars (tasks/)

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_tasks__var__' prefix.
playbooks/tasks/sample.yml:8 Task/Handler: Set vars (tasks/)

ansible-lint-custom-strict-naming<var_name_prefix>: Variables in 'set_fact' should have a 'sample_tasks__var__' prefix.
playbooks/tasks/sample.yml:11 Task/Handler: Set vars (tasks/)
```
