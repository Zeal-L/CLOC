"""
该模块提供Cloc类，用于统计目录下的代码行数
"""

from os.path import isdir
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, wait
from .file_handler import FileHandler
from .line_counter import LineCounter


class Cloc:
    """这是一个统计代码行数的类"""

    def __init__(self, lang, max_workers=8) -> None:
        """初始化Cloc对象

        Args:
            lang (str): 语言类型
            max_workers (int): 最大线程数，默认为8
        """
        self.stats = {"files": 0, "lines": 0, "code": 0, "comments": 0, "blanks": 0}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lang = lang
        self.file_handler = FileHandler(lang)
        self.lock = Lock()

    ############################################################

    def run(self, directory) -> dict[str, int]:
        """统计目录下的代码行数

        Args:
            directory (str): 目录路径

        Returns:
            dict[str, int]: 统计结果，包括文件数、总行数、代码行数、注释行数、空行数
        """
        if not isdir(directory):
            raise NotADirectoryError(f"{directory} 不是一个目录")
        files = self.file_handler.get_files(directory)
        self.stats["files"] = len(files)
        return self._count_lines(files)

    ############################################################

    def _count_lines(self, files) -> dict[str, int]:
        """统计文件列表中的代码行数, 利用了线程池来提高效率

        Args:
            files (list[str]): 文件路径列表

        Returns:
            dict[str, int]: 统计结果，包括文件数、总行数、代码行数、注释行数、空行数
        """
        futures = [
            self.executor.submit(self._count_lines_in_file, file) for file in files
        ]
        wait(futures)
        return self.stats

    ############################################################

    def _count_lines_in_file(self, file) -> None:
        """统计单个文件的代码行数

        Args:
            file (str): 文件路径
        """
        file_stats = LineCounter(self.lang).count_lines(file)
        if (
            file_stats["lines"]
            != file_stats["code"] + file_stats["comments"] + file_stats["blanks"]
        ):
            raise ValueError(f"{file} 的统计结果有误")
        with self.lock:
            self.stats["lines"] += file_stats["lines"]
            self.stats["code"] += file_stats["code"]
            self.stats["comments"] += file_stats["comments"]
            self.stats["blanks"] += file_stats["blanks"]
