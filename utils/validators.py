import os
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_filename(value):
    filename = os.path.basename(value.name)  # 只允许文件名，不允许路径
    if '..' in filename or filename.startswith('/'):
        raise ValidationError("Invalid file name: Path traversal is not allowed.")
    return value


def validate_no_executable_files(value):
    # 禁止上传某些文件类型
    restricted_extensions = ['exe', 'php', 'js', 'bat', 'sh', "css"]
    file_extension = value.name.split('.')[-1].lower()
    if file_extension in restricted_extensions:
        raise ValidationError(f"Files with the extension '{file_extension}' are not allowed.")
    return value



