from os import scandir
import shutil

def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            yield entry

def find_mp3_files(directory, is_recursive=True):
    files = []

    if is_recursive:
        for file in scantree(directory):
            if file.path.endswith(".mp3"):
                files.append(file.path)
    else:
        with scandir(directory) as entries:
            for file in entries:
                if file.path.endswith(".mp3"):
                    files.append(file.path)
    
    files.sort()
    return files

def copy_directory(in_dir, out_dir):
    shutil.copytree(in_dir, out_dir)
