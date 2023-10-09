"""
该模块用于获取指定目录下的所有文件
"""

from re import search
from os import walk, path


class FileHandler:
    """该类用于获取指定目录下的所有文件"""

    def __init__(self, lang) -> None:
        """初始化FileHandler对象

        Args:
            lang (str): 语言类型
        """
        self.lang = lang

    ############################################################

    def get_files(self, directory) -> list[str]:
        """获取指定目录下的所有文件

        Args:
            directory (str): 目录路径

        Returns:
            list[str]: 文件路径列表
        """
        files = []
        for root, _, filenames in walk(directory):
            files.extend(
                path.join(root, filename)
                for filename in filenames
                if search(r"\.(" + "|".join(self.lang.extensions) + ")$", filename)
            )
        return files
