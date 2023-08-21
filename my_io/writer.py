# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/19 0:33
@Author  : Fei Wang
@File    : writer
@Software: PyCharm
@Description: 
"""

import json
import yaml


def write_list_to_txt(file_path: str, data: list):
    """
    Write a list to a text file, with each item written on a separate line.

    Args:
        file_path (str): The path to the output text file.
        data (list): The list of items to be written to the file.

    Raises:
        TypeError: If the `data` parameter is not a list.
        IOError: If there is an error while writing to the file.
    """
    if not isinstance(data, list):
        raise TypeError("`data` parameter must be a list.")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in data:
                file.write(str(item) + '\n')
    except IOError:
        raise IOError(f"Error writing to file '{file_path}'.")


def save_dict_to_yaml(file_path: str, data: dict):
    """
    Save a dictionary to a YAML file.

    Args:
        file_path (str): The path to the output YAML file.
        data (dict): The dictionary to be saved.

    Raises:
        TypeError: If the `data` parameter is not a dictionary.
        IOError: If there is an error while writing to the file.
    """
    if not isinstance(data, dict):
        raise TypeError("`data` parameter must be a dictionary.")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, sort_keys=False)
    except IOError:
        raise IOError(f"Error writing to file '{file_path}'.")


def save_dict_to_json(file_path: str, data: dict):
    """
    Save a dictionary to a JSON file.

    Args:
        file_path (str): The path to the output JSON file.
        data (dict): The dictionary to be saved.

    Raises:
        TypeError: If the `data` parameter is not a dictionary.
        IOError: If there is an error while writing to the file.
    """
    if not isinstance(data, dict):
        raise TypeError("`data` parameter must be a dictionary.")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except IOError:
        raise IOError(f"Error writing to file '{file_path}'.")


def save_list_to_jsonl(file_path: str, data: list):
    """
    Save a list of dictionaries to a JSONL (JSON Lines) file.

    Args:
        file_path (str): The path to the output JSONL file.
        data (list): The list of dictionaries to be saved.

    Raises:
        TypeError: If the `data` parameter is not a list of dictionaries.
        IOError: If there is an error while writing to the file.
    """
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise TypeError("`data` parameter must be a list of dictionaries.")

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for item in data:
                file.write(json.dumps(item, ensure_ascii=False) + '\n')
    except IOError:
        raise IOError(f"Error writing to file '{file_path}'.")

