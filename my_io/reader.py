# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/19 0:02
@Author  : Fei Wang
@File    : reader
@Software: PyCharm
@Description:
"""

import json
import yaml


def yaml_reader(file_path: str) -> dict:
    """
    Read and parse a YAML file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: A dictionary representing the content of the YAML file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error while parsing the YAML file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def json_reader(file_path: str) -> dict:
    """
    Read and parse a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary representing the content of the JSON file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If there is an error while parsing the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def jsonl_reader(file_path: str) -> list:
    """
    Read and parse a JSONL (JSON Lines) file.

    Args:
        file_path (str): The path to the JSONL file.

    Returns:
        list: A list of dictionaries representing the content of the JSONL file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the JSONL file is empty or contains invalid JSON.
    """
    data = list()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    raise ValueError(f"Error while parsing JSON at line: {line}") from e

    if not data:
        raise ValueError("Empty JSONL file.")

    return data


def txt_reader(file_path: str) -> str:
    """
    Read and return the content of a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The content of the text file as a string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an error while reading the text file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except IOError:
        raise IOError(f"Error reading file '{file_path}'.")

    return content.strip()




