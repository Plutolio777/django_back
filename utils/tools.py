import os
import tarfile
import py7zr
import zipfile

from django_back import settings


def media_path_to_url(media_path):
    # 确保路径在MEDIA_ROOT内
    media_root = settings.MEDIA_ROOT
    if not os.path.abspath(media_path).startswith(os.path.abspath(media_root)):
        raise ValueError("文件不在MEDIA_ROOT目录下")

    # 计算相对路径
    relative_path = os.path.relpath(media_path, media_root)

    # 转换路径分隔符为URL格式
    relative_path = relative_path.replace(os.path.sep, '/')

    # 拼接URL
    return settings.MEDIA_URL + relative_path


def try_unzip_files(input_dir: str, output_dir=None):
    """
    解压指定目录中的所有支持的压缩文件

    Args:
        input_dir: 需要扫描的输入目录路径

    Returns:
        包含 (原始文件名, 解压路径) 的元组列表

    Raises:
        ValueError: 如果输入路径无效
    """
    # 验证输入路径
    if not os.path.exists(input_dir):
        raise ValueError(f"目录不存在: {input_dir}")
    if not os.path.isdir(input_dir):
        raise ValueError(f"路径不是目录: {input_dir}")

    # 遍历目录中的所有文件
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        # 跳过子目录和非文件项
        if not os.path.isfile(file_path):
            continue

        try:
            # 处理 ZIP 文件
            if filename.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(output_dir or input_dir)

            # 处理 TAR 及其变种
            elif any(filename.endswith(ext) for ext in ('.tar', '.tar.gz', '.tar.bz2')):

                # 确定压缩格式
                mode_dict = {
                    '.tar': 'r',
                    '.tar.gz': 'r:gz',
                    '.tar.bz2': 'r:bz2'
                }
                ext = next(ext for ext in mode_dict if filename.endswith(ext))
                with tarfile.open(file_path, mode_dict[ext]) as tar_ref:
                    tar_ref.extractall(output_dir or input_dir)

            elif filename.endswith('.7z'):
                with py7zr.SevenZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(output_dir or input_dir)

        except (zipfile.BadZipFile, tarfile.ReadError, OSError) as e:
            print(f"[错误] 解压失败 {filename}: {str(e)}")
        except Exception as e:
            print(f"[意外错误] 处理 {filename} 时发生异常: {str(e)}")
