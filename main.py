import sys
import pyfiglet
from cloc import Cloc, LANGUAGES
from argparse import ArgumentParser
from rich import print as pprint


if __name__ == "__main__":
    # 初始化命令行参数解析器
    parser = ArgumentParser(description="Count lines of code in a project.")
    parser.add_argument(
        "-l", "--language", type=str, help="the language to count, e.g. c, ruby"
    )
    parser.add_argument(
        "-w",
        "--max-workers",
        type=int,
        default=8,
        help="the max workers to count, default is 8",
    )
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    parser.add_argument("directory", type=str, nargs="?", help="the directory to count")

    # 解析命令行参数
    args = parser.parse_args()
    if args.version:
        ascii_art = pyfiglet.figlet_format("CLOC", font="slant")
        pprint(f"[bold red]{ascii_art}[/bold red]")
        pprint("[bold red]Version: [/bold red][bold yellow]0.0.1[/bold yellow]")
        pprint("[bold red]Author: [/bold red][bold yellow]Zeal-L[/bold yellow]")

        sys.exit(0)

    if not args.directory and not args.version:
        parser.print_help()
        pprint("\nerror: the following arguments are required: directory")
        sys.exit(1)

    if args.language:
        lang = LANGUAGES.get(args.language)
        if not lang:
            pprint(
                f"[bold red]error: Language [yellow]{args.language}[/yellow] is not supported[/bold red]"
            )
            pprint("[bold red]Supported languages are:[/bold red]", end=" ")
            pprint("[bold yellow]" + ", ".join(LANGUAGES.keys()) + "[/bold yellow]")
            sys.exit(1)
    else:
        parser.print_help()
        pprint("[bold red]error: -l LANGUAGE is required[/bold red]")
        sys.exit(1)

    if args.max_workers < 1 or args.max_workers > 128:
        pprint(
            "[bold red]error: MAX_WORKERS must be a number between 1 and 128[/bold red]"
        )
        sys.exit(1)

    # 统计代码行数
    stats = Cloc(lang, args.max_workers).run(args.directory)

    # 打印统计结果
    header = "-" * 59
    header += "\n{:>6} {:>12} {:>12} {:>12} {:>12}".format(
        "Files", "Lines", "Code", "Comments", "Blanks"
    )
    header += "\n" + "-" * 59

    data = "\n{:>6} {:>12} {:>12} {:>12} {:>12}".format(
        stats["files"],
        stats["lines"],
        stats["code"],
        stats["comments"],
        stats["blanks"],
    )
    data += "\n" + "-" * 59

    print(header + data)
