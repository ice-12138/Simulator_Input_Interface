import logging


def mns_logging():
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s",
    )

# filename='app.log', # 日志文件名，如果没有这个参数，日志输出到console
# filemode='w') # 文件写入模式，“w”会覆盖之前的日志，“a”会追加到之前的日志
