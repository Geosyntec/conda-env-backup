import os
from pathlib import Path
import sys
import subprocess
from datetime import datetime


def ensure_path(path: str | Path):
    path = Path(path)

    if len(path.suffixes) == 0:
        path.mkdir(parents=True, exist_ok=True)
    else:
        pdir = path.parent
        pdir.mkdir(parents=True, exist_ok=True)

    return path


def get_envs():
    """Returns list of environment names"""
    ls = subprocess.Popen("conda info --envs", stdout=subprocess.PIPE, shell=True)
    envs = []
    for line in ls.stdout.readlines():  # type: ignore
        cleanline = line.decode().strip()
        if "#" not in cleanline and cleanline != "":
            envs.append(cleanline.split()[0])

    return envs


def export_env(env):
    """Saves a conda env and a pip freeze in a folder with todays date.

    Parameters
    ----------
    env : string
        name of the conda environment that will be exported to text file.

    Returns
    -------
    None : saves a .txt file for `conda env export` and `pip freeze`

    """

    folder = ensure_path(f"./_backups/{datetime.now().strftime('%Y-%m-%d')}-{os.name}")

    pip_file = folder.resolve() / "{}_pip.txt".format(env)
    conda_file = folder.resolve() / "{}_conda.txt".format(env)
    conda_file_hist = folder.resolve() / "{}_conda_hist.txt".format(env)
    conda_file_builds = folder.resolve() / "{}_conda_builds.txt".format(env)

    start = "start /b cmd.exe /c" if os.name == "nt" else ""
    end = "" if os.name == "nt" else "&"
    cmd = (
        '{start} conda env export -n {env} --no-build > "{conda_file}" &'
        '{start} conda env export -n {env} --no-build --from-history> "{conda_file_hist}" &'
        '{start} conda env export -n {env} > "{conda_file_builds}" &'
        '{start} conda run -n {env} pip list --format=freeze > "{pip_file}" {end}'
    ).format(
        start=start,
        env=env,
        pip_file=pip_file,
        conda_file=conda_file,
        conda_file_hist=conda_file_hist,
        conda_file_builds=conda_file_builds,
        end=end,
    )

    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) > 0:
        for arg in args:
            print("processing: ", arg)
            export_env(arg)
    else:
        for arg in get_envs():
            print("processing: ", arg)
            export_env(arg)

    print("complete.")
