from os.path import join, dirname

async def get_file_path(file_name):
    return join(dirname(__file__), file_name)
