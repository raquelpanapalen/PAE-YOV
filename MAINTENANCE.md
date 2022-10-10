# Maintenance

How to keep up to date the repo. Keep in mind that the submodules point to a
specific commit hash, not to a branch. You can set the branch you want to
follow, but it will just point to the most recent commit (After running the
following commands).

```sh
git pull
git submodule update --recursive --remote --progress
```

An __alternative__ of the above commands is the following. This uses the `git
submodule foreach` command to execute a bash command on each checked out
submodule. For more info on this command read the following [docs](https://mirrors.edge.kernel.org/pub/software/scm/git/docs/git-submodule.html#foreach).
For this command to work the submodule needs to be configured to track a
branch.
```sh
git pull
git submodule foreach -q --recursive 'echo -e "\e[1mUpdating submodule \"$name\"\e[0m"; branch=$(git config -f $toplevel/.gitmodules submodule.$name.branch); git switch $branch; git pull; echo ""'
```

In case you don't want to write/copy this command every time you can add the
following alias to your `.bashrc` file, where `gsu` is the name of the alias
(you can the name change it to whatever you want, just check that it's not a
command or that it's not an other alias name):
```sh
alias gsu=$'git submodule foreach -q --recursive \'echo -e "\e[1mUpdating submodule \"$name\"\e[0m"; branch=$(git config -f $toplevel/.gitmodules submodule.$name.branch); git switch $branch; git pull; echo ""\''
```

An other options is to add a git [alias](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases).
To do so, just execute the following command:
```sh
git config --global alias.sm-update $'submodule foreach -q --recursive \'echo -e "\e[1mUpdating submodule \"$name\"\e[0m"; branch=$(git config -f $toplevel/.gitmodules submodule.$name.branch); git switch $branch; git pull; echo ""\''
```

