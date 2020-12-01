import os


def get_first_model_at(model_dir):
    for entry in os.scandir(model_dir):
        if entry.is_dir():
            return entry.name

    return None
