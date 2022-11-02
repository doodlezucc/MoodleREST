import os
import subprocess
import sys
from typing import List

def exec(cmd: List[str], cwd: str, print_out = True):
    with open("log", "wb") as f:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
        for c in iter(lambda: process.stdout.read(1), b""):
            if print_out:
                sys.stdout.buffer.write(c)
            f.write(c)
    
        code = process.wait()
        if print_out:
            print(f"{cmd[0]} exited with code {code}")
    
    with open("log", "r") as f:
        return f.read()

def git_clone_shallow(repo: str, dest: str):
    exec(["git", "clone", "--depth", "1", "--no-single-branch", repo, dest])

def get_git_branches(cwd: str):
    stdout = exec(["git", "--no-pager", "branch", "-r", "--no-color"], cwd=cwd, print_out=False)
    branches = [s.strip() for s in stdout.splitlines()]
    return branches

def branch_to_version(br: str):
    ver = br[br.index("_") + 1:]
    ver = ver[0:ver.index("_")]

    def semver(s):
        return '.'.join(s)

    if ver.startswith("4"):
        return semver(ver)
    return semver([ver[0], ver[1:]])

def stable_moodle_branches(branches: List[str]):
    return {branch_to_version(br): br for br in branches if "MOODLE" in br}

def git_checkout(branch: str, cwd):
    print(f'Applying branch "{branch}"')
    exec(["git", "checkout", branch], cwd=cwd, print_out=False)

def extract_api(branch, cwd):
    git_checkout(branch, cwd)
    print("Extracting Web Service API (soon)")

def main():
    dirpath = "moodle"

    if not os.path.exists(dirpath):
        git_clone_shallow("git://git.moodle.org/moodle.git", dirpath)
    
    branches = get_git_branches(dirpath)
    stable = stable_moodle_branches(branches)
    pick = "3.9"

    if pick not in stable:
        raise f"Version {pick} not available"
    
    branch = stable[pick]
    extract_api(branch, dirpath)

main()