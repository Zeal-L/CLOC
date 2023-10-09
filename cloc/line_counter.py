"""该模块用于分析给定文件的代码行数、注释行数和空行数"""


class LineCounter:
    """该类用于分析给定文件的代码行数、注释行数和空行数"""

    def __init__(self, lang) -> None:
        """初始化 LineCounter 对象

        Args:
            lang: 语言对象
        """
        self.lang = lang
        self.code_lines = 0
        self.comment_lines = 0
        self.blank_lines = 0
        self.in_multi_comment = False

    ############################################################

    def count_lines(self, file_path: str) -> dict[str, int]:
        """分析给定文件的代码行数、注释行数和空行数

        Args:
            file_path: 文件路径

        Returns:
            dict[str, int]: 统计结果，包括代码行数、注释行数和空行数
        """
        lines = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                self._count_line(line)
                lines += 1
        return {
            "lines": lines,
            "code": self.code_lines,
            "comments": self.comment_lines,
            "blanks": self.blank_lines,
        }

    ############################################################

    def _count_line(self, line: str) -> None:
        """分析单行代码

        Args:
            line: 单行代码
        """
        line = line.strip()

        if not line:
            self.blank_lines += 1
            return

        if self.in_multi_comment:
            self.comment_lines += 1
            if line.endswith(self.lang.multi_comment_end):
                self.in_multi_comment = False
            return

        if line.startswith(self.lang.single_comment):
            self.comment_lines += 1
            return

        if line.startswith(self.lang.multi_comment_start):
            self.comment_lines += 1
            if not line.endswith(self.lang.multi_comment_end):
                self.in_multi_comment = True
            return

        self.code_lines += 1
