# -*- coding: utf-8 -*-
"""
@Time    : 2023/8/22 22:05
@Author  : Fei Wang
@File    : project_init
@Software: PyCharm
@Description: 
"""
import os
from typing import Dict
from pathlib import Path
from loguru import logger
from wandb import init as wandb_init


def __init_dir(config: Dict[str, str]) -> Path:
    """
    根据给定的配置参数创建输出目录并初始化项目所需的子目录。

    Args:
        config (dict): 包含配置参数的字典。
            - 'output_dir' (str): 输出目录的基础路径。
            - 'project_name' (str): 项目名称。
            - 'group_name' (str): 组名称。
            - 'run_name' (str): 运行名称。

    Returns:
        Path: 输出目录的路径。
    """
    output_dir = Path(
        "/".join([
            config['output_dir'],
            config['project_name'],
            config['group_name'],
            config['run_name'],
        ])
    )

    project_dirs = ['model', 'cache', 'checkpoints', 'onnx']
    for dir_name in project_dirs:
        (output_dir / dir_name).mkdir(parents=True, exist_ok=True)

    return output_dir


def __init_log(config: Dict[str, str], output_dir: Path) -> None:
    """
    根据给定的配置参数和输出目录初始化日志记录器。

    Args:
        config (dict): 包含配置参数的字典。
            - 'rotation' (str): 日志文件的轮转方式。
            - 'compression' (str): 日志文件的压缩方式。
        output_dir (Path): 输出目录的路径。

    Returns:
        None
    """
    logger.add(
        output_dir / 'cache' / 'train.log',
        rotation=config['rotation'],
        compression=config['compression'],
    )


def init_project(config: Dict[str, any]) -> Path:
    """
    根据给定的配置参数初始化项目。

    Args:
        config (dict): 包含配置参数的字典。

    Returns:
        Path: 输出目录的路径。
    """
    output_dir = __init_dir(config)

    __init_log(config['log'], output_dir)

    if config['project_info']['use_wandb'] == 1:
        wandb_init(
            project=config['project_name'],
            group=config['group_name'],
            name=config['run_name'],
            dir=str(output_dir),
        )
    else:
        os.environ['WANDB_DISABLED'] = 'true'
    return output_dir
