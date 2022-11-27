import uuid


def get_rnd_file_name_by_content_type(content_type):
    return '.'.join([uuid.uuid4().hex, content_type.split("/")[-1]])