# Working with Git

This documentation on working with Git does not include a general introduction to Git or an instruction to install Git. <!-- Please refert to {LINK} for more information. --> THe following file describe specific resources for using Git with the ETDataset repository.

- A [**glossary**](#glossary-of-git-commands) of useful Git commands.
- A [**step-by-step guide**](#how-to-commit-and-push-changes-from-your-machine-to-github) for how to commit and push changes from your machine to Git.
- A guide on how to resolve [**merge conflicts**](#merge-conflicts-and-troubleshooting).


## Glossary of Git commands

`ls`
lists the files in your current directory

`ls -a`
lists all files in your current directory

`cd`
change directory. E.g. `cd etdataset/analyses` will put you inside the analyses folder on etdataset.

`cd ..`
this will move you up one directory level.

`git branch`
`git branch -a`
displays a list of branches (remote and local)

`git clone git@github.com:quintel/etdataset.git`
Clones (saves) the etdataset repository to your local machine. The new files will be saved in your current working directory, so make sure you are in the right place before executing this line.

`git up`
This command ensures that you have all the latest commits synched with your local machine.

`bundle install`
Installs and updates gemfiles. Makes sure that all required tools and softare is installed.

`git status`
give a list of files that have been changed.

`git diff <file>`
the command `git diff` will generate a list of what has changed within files or between commits. If you specify a file, only the changes in that particular file will be displayed. Usually, you can only do a git diff on a text file, binary files cannot be version controlled in that manner. It is possible to set up a git diff for excel files, see [QI technical readme.md](https://github.com/quintel/etdataset/blob/master/QI%20technical%20readme.md).

`git checkout -b branch_name`
this will create a new branch called "branch_name". You will automatically 'switch' onto that new branch (i.e. check out that branch).

`git checkout branch_name`
switches onto the branch called "branch_name".

`git branch -d branch_name`
deletes the branch called "branch_name". You will loose all un-pushed commits on that branch.

`git reset --soft HEAD^`
Undo the last commit. You are left with your working directory before the commit, with your changes stashed. Also see http://stackoverflow.com/questions/927358/how-to-undo-the-last-git-commit

`git push -f origin <SHA>:master` **Use carefully!!**
resetting the origin branch back to a certain commit. This is a force push - think twice and use cautiously. also see: http://stackoverflow.com/questions/3012929/can-i-undo-the-last-git-push


## How to commit and push changes from your machine to GitHub

Run `git up` on all relevant repositories (ETDataset and ETSource).

#### 1. Create a new branch in your local repository and make sure you are on that branch

    (master) git branch newbranch
    (master) checkout newbranch

Or in one go:

    (master) git checkout -b newbranch

To see your branches:

    (master) git branch -a

#### 2. Make your changes to files (Excel files OR CSV input/output files)

Observe which changes have been made:

    git status

Stage files for commit:

    git add
    git add -u

Commit the staged files with a verbose commit message:

    git commit -m "type your message here. Be verbose. You MUST explain all relevant changes that are introduced with this commit"

Rules on commit messages are described in a [separate section](https://github.com/quintel/etdataset/#rules-code-of-conduct). If your commit message does not meet these standards, you pull request cannot be considered.

#### 3. Push your changes to remote repository. Note how you have to explicitly name a remote branch to push to.

After committing, you can push *your* branch to the central repository on Github. You can push after each commit, if you want to.

    git push

Since your new branch does likely not yet exist remotely, you are prompted to use

    (newbranch) git push --set-upstream origin newbranch

  You will see something like this:

    Counting objects: 9, done.
    Delta compression using up to 4 threads.
    Compressing objects: 100% (3/3), done.
    Writing objects: 100% (5/5), 350.52 KiB, done.
    Total 5 (delta 1), reused 0 (delta 0)
    To git@github.com:quintel/Etdataset.git
    * [new branch]      newbranch -> newbranch
    Branch newbranch set up to track remote branch newbranch from origin by
    rebasing.

#### 4. Go to GitHub and create a pull request for you new branch.
  The `compare and review` button is easy. Otherwise, go  to `Pull requests` and take it from there.
  Pull requests need to contain decent request messages to be considered. ASSIGN SOMEBODY from the Quintel team to review your request.
  If you have been assigned, you will need to pull the changes to your local repository and switch branches to review the changes.

    (master) git up
    (master) git checkout name_of_newbranch

  Reviewers may ask you to commit and push additional changes to newbranch before approving the merge request. You and the reviewer can exchange comments much like when discussing issues.

#### 5. After merge is complete, delete the branch on GitHub
To delete it from your local repository do:

    (master) git branch -D newbranch


## Merge conflicts and troubleshooting

Inevitably, changes to the same Excel file will lead to merge conflicts, as Git cannot determine the exact changes to binary files. How do you get yourself out of this mess without losing your changes (or those of your colleague)?

In principle, using pull request as described above should avoid most conflicts. You will likely encounter a merging conflict when trying to merge a pull request that involves files that are changed on the two branches. In that case, Git will tell you that a pull request cannot be merged autmatically.

When you encounter a merge conflict that involves binary files (.xlsx), do <b>not</b> follow the help that github offers in the pull request. Instead
- Go to your terminal, `git up` the master branch and the branch you want to merge it with. Let's call it "new_branch".
- make sure that you checkout the master branch
- `git merge new_branch` (merge the new_branch into master)
- you will see a warning like:

>
warning: Cannot merge binary files: .... (HEAD vs. new_branch)
  ...
  Automatic merge failed; fix conflicts and then commit the result.

- If you want to keep the file that lives on the new_branch, type: `git checkout --theirs <file name>`. It is important that you specify the file name that you want to checkout.
- `git status`
- checkout the file that is conflicted (see if you checked out the correct version). You might want to use: `git checkout --theirs`
- `git add .`
- `git commit –m "message"`
- `git push`

#### Other useful commands:

To merge (and quit merging) branches:

    git merge
    git merge --abort

To rebase (and undo a rebase in case of a conflict):

    git rebase
    git rebase --abort

After aborting, you are left with the binary file from origin and back where you started merging. To get your hands on your own binary, you will probably want to checkout that file for that commit.

After you have resolved the issue you can rebase:

    git rebase --continue

Get back a specific file from an older commit or separate branch without changes to your history:

    git checkout <hash>/<branch>/<HEAD~1> path file
    git commit -am "commit msg"

Note that you do not need to stage the file. This just adds an additional commit, which can be pushed as normal.

Get back a specific file from an older commit and change your local history:

    git reset <hash> --hard

This you can only push by force:

    git push --force

This can seriously screw up things on the remote repository and will earn you few friends. **Think again, if you believe this is what you want to do.**
