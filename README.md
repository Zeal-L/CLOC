# cloc -- Count Lines of Code 代码行数统计⼯具

```
   ________    ____  ______
  / ____/ /   / __ \/ ____/
 / /   / /   / / / / /
/ /___/ /___/ /_/ / /___
\____/_____/\____/\____/      by Zeal-L

```

## 项目介绍
- 本项目是一个用Python3开发的简单的代码统计工具，可以统计指定目录下的代码行数、空行数、注释行数
- 目前仅支持 `C/C++` 语言和 `Ruby` 语言, 不过用户可以很方便地添加新的语言支持

## 部署方法
- 运行环境: Python 3.11+, win10 amd64
1. `cd Project-Stats` -- 进入项目目录
2. `pip3 install pipenv` -- 安装pipenv (如已经安装, 可以跳过这一步)
3. `pipenv run pipenv install --dev`  -- 安装依赖
4. `pipenv shell` -- 激活虚拟环境
5. `python main.py -v` -- 输出版本信息

## 卸载方法
1. `pipenv --rm` -- 删除虚拟环境
2. `cd .. && rm -rf Project-Stats/` -- 删除项目目录

## 使用指南
`python main.py [-h] [-l LANGUAGE] [-w MAX_WORKERS] [-v] [directory]`
- `-h`          -- 可选，查看帮助信息
- `-v`          -- 可选，查看版本信息
- `-w`          -- 可选，设置最大工作线程数, 默认为 `8`
- `-l`          -- 必选，选择分析的语言, 可选项: `c`, `ruby`
- `directory`   -- 必选，指定分析的目录

### 用例1
- 分析 `test/cpp-project` 目录下的 `C/C++` 代码, 最大工作线程数为 `8` (默认)
  - `python main.py -l c test/cpp-project`

### 用例2
- 分析 `test/ruby-project` 目录下的 `Ruby` 代码, 最大工作线程数为 `64`
  - `python main.py -l ruby -w 64 test/ruby-project`

## 扩展语言支持
- 只需要在 `cloc/language.py` 文件中的 `Language` 类里添加对应的语言静态构建方法，并且添加到 `LANGUAGES` 字典里即可
- 例如，添加对 `Python` 语言的支持:
```python
@staticmethod
def py_constructor() -> "Language":
    return Language(["py"], "#", "\"\"\"", "\"\"\"")

LANGUAGES = {
    ...,
    "py": Language.py_constructor()
}

```

## 项目结构
- `cloc/` -- 代码统计工具的核心代码
  - `__init__.py` -- 项目初始化文件
  - `cloc.py` -- 代码统计工具的核心逻辑代码
  - `file_handler.py` -- 文件处理类
  - `language.py` -- 存放核心编程语言语法的类
  - `line_counter.py` -- 行数统计分析类
- `test/` -- 测试用例
  - `cpp-project/` -- 用于测试的 `C/C++` 项目
  - `ruby-project/` -- 用于测试的 `Ruby` 项目
- `main.py` -- 程序主入口

## 设计思路
- 本项目的核心代码是 `cloc/cloc.py` 文件，主要实现了一个线程池，用于并发地统计代码行数
- 为了实现更好的可扩展性，专门设计了 `Language` 类来存放核心编程语言的分析语法，用户可以很方便地添加新的语言支持
- 同时还设计了 `FileHandler` 类来处理不同后缀名的文件，用户可以很方便地添加新的文件处理逻辑
- 统计行数和分析的逻辑集中放在了 `cloc/line_counter.py` 文件，用户可以很方便地添加新的行数统计逻辑
  - 目前的设计是就算字符串中包含了注释符号或者多行注释符号，也会被统计为有效代码行数，这样做的更符合逻辑
  - 开源社区的 [cloc](https://github.com/AlDanial/cloc) 在这种情况下是会将字符串中的注释行统计为注释行数，我认为不妥，这有悖 “删除所有注释应当不影响源程序的运行” 这一原则
  - 例如下面这个例子中, 虽然字符串中包含了注释符号，但是这些注释符号并不是真正的注释，而是字符串的一部分，因此我的 `cloc` 不会把这些注释符号统计为注释行数
    ```c
    static char text[1024 * 16] =
        "/*\n"
        " The Pentium F00F bug, shorthand for F0 0F C7 C8,\n"
        " the hexadecimal encoding of one offending instruction,\n"
        " more formally, the invalid operand with locked CMPXCHG8B\n"
        " instruction bug, is a design flaw in the majority of\n"
        " Intel Pentium, Pentium MMX, and Pentium OverDrive\n"
        " processors (all in the P5 microarchitecture).\n"
        "*/\n\n"
        "label:\n"
        "\tlock cmpxchg8b eax\n";
    ```
- 在程序主入口 `main.py` 文件中，我使用了 `argparse` 第三方包来更好解析命令行参数，同时也使用了 `rich` 第三方包来更好地输出错误以及帮助信息