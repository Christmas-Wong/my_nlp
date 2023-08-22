# -*- coding: utf-8 -*-
"""
@Time    : 2023/8/22 22:07
@Author  : Fei Wang
@File    : utils
@Software: PyCharm
@Description: 
"""
import json
import torch


def list2multilabel(labels: list, id2label: dict, default_label: str = "无"):
    """Convert Onehot Coding into Multi-Labels

    Args:
        labels: Onehot Coding
        id2label: Mapping Relationship between Labels and Numbers
        default_label: Default Label

    Returns:
        Multi-Labels split by ","

    """
    result = [id2label[index] for index, ele in enumerate(labels) if ele == 1]
    # if predict None of labels, match default label
    if len(result) < 1:
        result.append(default_label)

    return ",".join(result)


def bind_score(model_result: list, id2label: dict) -> list:
    """Bind Score to Label

    Args:
        model_result (list) : Predict Result of Model
        id2label (dict) : Mapping Relationship between Labels and Numbers

    Returns:
        List of Scores

    """
    result = list()
    for index, ele in enumerate(model_result):
        result.append(
            {
                "label": id2label[index],
                "score": float(ele),
            }
        )

    return result


def __multiclass_logits2score(logits: torch.Tensor, id2label: dict) -> tuple:
    list_scores = [bind_score(ele, id2label) for ele in logits.softmax(dim=1).cpu().detach().numpy().tolist()]
    list_labels = [id2label[ele] for ele in logits.softmax(dim=1).argmax(dim=1).cpu().detach().numpy()]
    return list_scores, list_labels


def __multilabel_logits2score(logits: torch.Tensor, id2label: dict) -> tuple:
    sigmoid = logits.sigmoid().detach().cpu().numpy()
    pred_code = (sigmoid > 0.5).astype(int)
    list_scores = [bind_score(ele, id2label) for ele in sigmoid.tolist()]
    list_labels = [list2multilabel(ele, id2label) for ele in pred_code.tolist()]
    return list_scores, list_labels


def logits2score(logits: torch.Tensor, task_type: str, id2label: dict) -> tuple:
    """Build Score from logits

    Args:
        logits: Logits
        task_type: Type of task type
        id2label: Dictionary of id to label

    Returns:
        list_scores & list_labelse

    """
    switch_func = {
        "multiclass": __multiclass_logits2score,
        "multilabel": __multilabel_logits2score,
    }
    return switch_func[task_type](logits, id2label)


def id2label_reader(file_path: str) -> dict:
    """
    从文件中读取id到标签的映射关系，并返回一个字典。

    Args:
        file_path (str): 文件路径。

    Returns:
        dict: id到标签的映射关系的字典。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        result = json.load(f)

    output = {}
    for k, v in result.items():
        output[int(k)] = v
    return output