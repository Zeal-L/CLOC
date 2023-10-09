"""
该文件包含Language类，用于存储有关的信息
"""


class Language:
    """语言类，用于存储不同编程语言的语法信息"""

    def __init__(
        self, extensions, single_comment, multi_comment_start, multi_comment_end
    ) -> None:
        """初始化Language对象

        Args:
            extensions (list[str]): 该语言的文件后缀名
            single_comment (str): 单行注释符
            multi_comment_start (str): 多行注释开始符
            multi_comment_end (str): 多行注释结束符
        """
        self.extensions = extensions
        self.single_comment = single_comment
        self.multi_comment_start = multi_comment_start
        self.multi_comment_end = multi_comment_end

    ############################################################

    @staticmethod
    def c_constructor() -> "Language":
        """用于构建C语言的Language对象的静态方法

        Returns:
            Language: C语言的Language对象
        """
        return Language(["c", "cpp", "cc"], "//", "/*", "*/")

    ############################################################

    @staticmethod
    def ruby_constructor() -> "Language":
        """用于构建Ruby语言的Language对象的静态方法

        Returns:
            Language: Ruby语言的Language对象
        """
        return Language(["rb"], "#", "=begin", "=end")


# 语言字典，用于存储不同编程语言的Language对象
LANGUAGES = {
    "c": Language.c_constructor(),
    "ruby": Language.ruby_constructor(),
}
