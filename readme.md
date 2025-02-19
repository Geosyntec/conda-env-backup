# Backup Your Conda Envs

Is your computer storage consumed by a prodigious quantity of `conda` envs?
Are you preparing to receive a new machine and need to configure it with the same environments as your current machine?
Have you _maybe_ forgotten to save a conda env file with every project-related python script you've ever created via
`conda env export --no-builds > my-project.yaml`

You **should** be doing that last one, but in all these cases this script can help save bacon.

## Usage

First, don't try this tool if you're not using `conda`... instead start using `conda` by going [here](https://github.com/Geosyntec/conda_init) and following the getting started guide.
Then, use git to clone this repository to a directory on your computer.
We recommend either $USERNAME/Documents or somewhere in your OneDrive folder.
Just put it somewhere memorable so that when you need to find it later you know where it is.

**Setup With `git`**

```
cd <path/to/your-dir-from-previous-step>
git clone git@github.com:Geosyntec/conda-env-backup.git
cd conda-env-backup
```

**Setup Without `git`**

It's recommended you learn how to use `git`, but it's not required to use this backup tool.

1. Download this project as a .zip file by clicking on the green `<> Code` button and selecting 'Download ZIP'.
2. Extract the zip and place it in the directory where you want to save your backups.
3. Open this project in your terminal so you can run python commands.

**Save Conda Environment Backups**

Run the script with no arguments to save a backup of all[^1] the conda envs on your machine:

```
python backup_conda_envs.py
```

This command will create a \_backups directory in the current working directory (if it doesn't already exist) and then use todays date and the current system platform to create a sub-directory named for todays env backups.

After this command is run the directory tree should be similar to:

```
.
├── _backups
│   └── 2025-02-19-nt
│       ├── base_conda.txt
│       ├── base_conda_builds.txt
│       ├── base_conda_hist.txt
│       ├── base_pip.txt
│       └── ...
├── backup_conda_envs.py
├── readme.md
└── tree.txt
```

It's also possible to just create a backup for one or more env by passing them as arguments to the script.

```
python backup_conda_envs.py base proj1-env proj2-env
```

[^1]: There's no way for me to know if you've done something weird like install ArcGISPro or something... any environment not listed in `conda env list` will not be backed up by this script.

## Restoring Your Environments After Backing up

All the backups are stored as plain text.
This is how pip expects to get its requirements files, but it's not how conda expects its env files.

If you know you want to use the full conda env as-is for the restore, simply copy the backup to your project directory and change the extension to '.yml' rather than '.txt' and run
`conda env create -f environment.yml`.

If you're not sure, the backups provided can help you get going on reconstructing a working environment.

**\*\_conda.txt** -- these files contain all the packages in the environment and their version numbers. These files also include packages that were installed with `pip`.
This is good for using as the as-is restore file mentioned above.

**\*\_conda_builds.txt** -- these files contain the most amount of detail about the env, including the specific conda build of each package.
This is good for debugging but not for building fresh clones of older environments.

**\*\_conda_hist.txt** -- these files contain the least amount of detail about the env and include only the list of packages you deliberately installed from the commandline with a `conda install <package>` command.
This is good for keeping it simple but you'll need to chase down the appropriate versions of those packages.

**\*\_pip.txt** -- these files contain the `pip list --format freeze` contents for this environment.
This is good for some envs where `pip` and `conda` disagree about what's installed.
It's also useful if your project relied more on `pip` than on `conda`, since you can use it as your requirements.txt file and install everything with `pip install -r <env>_pip.txt`
