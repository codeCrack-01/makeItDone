from pathlib import Path


def filter_file_name(name_str):
    if name_str is not None:
        return Path(name_str).stem
