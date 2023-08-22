# -*- coding: utf-8 -*-
"""
@Time    : 2023/8/22 22:07
@Author  : Fei Wang
@File    : torch_bert_classification
@Software: PyCharm
@Description: 
"""
import torch
from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, BertTokenizer
from .utils import id2label_reader, logits2score


class TorchBertClassification(object):
    """
    分类推断类，用于加载模型和进行推断。

    参数：
    model_path: str, 模型的路径。
    tokenizer_path: str, 分词器的路径。
    id2label_path: str, id到标签的映射文件路径。
    task_type: str, 任务类型，可选值为 const.TASK_TYPE_CLASSIFICATION 中的一种。
    device: str, 设备名称，可选值为 "cuda" 或 "cpu"。
    batch_size: int, 推断的批次大小。
    max_seq_length: int, 输入序列的最大长度。
    """

    def __init__(
            self,
            model_path: str,
            tokenizer_path: str,
            id2label_path: str,
            task_type: str = "multiclass",
            device: str = "cuda",
            batch_size: int = 64,
            max_seq_length: int = 512,
    ):
        super(TorchBertClassification, self).__init__()
        self.__task_type = task_type
        self.__model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.__tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        self.__id2label = id2label_reader(id2label_path)
        self.__device = device
        self.__batch_size = batch_size
        self.__max_seq_length = max_seq_length

        self.__model.to(self.__device)

    def infer(self, inputs: list):
        """
        执行推断操作。

        参数：
        inputs: list, 输入文本列表，每个元素是一个字典，包含 "text" 字段表示文本内容。

        返回：
        result: dict, 推断结果的字典。
            - "logits": list, 每个批次的logits列表。
            - "list_scores": list, 分类得分列表。
            - "list_labels": list, 预测标签列表。
        """
        data_batch = [inputs[i:i + self.__batch_size] for i in range(0, len(inputs), self.__batch_size)]
        self.__model.eval()
        outputs = list()
        with torch.no_grad():
            for batch in tqdm(data_batch, desc="Classification Inference", leave=False):
                text_batch = [ele["text"] for ele in batch]
                encoding = self.__tokenizer.batch_encode_plus(
                    text_batch,
                    padding="max_length",
                    truncation=True,
                    max_length=self.__max_seq_length,
                    return_tensors="pt"
                ).to(self.__device)
                output = self.__model(
                    encoding["input_ids"],
                    token_type_ids=encoding["token_type_ids"],
                    attention_mask=encoding["attention_mask"],
                    return_dict=True
                )
                outputs.append(output.logits)
        list_scores, list_labels = logits2score(torch.cat(outputs, 0), self.__task_type, self.__id2label)
        return {
            "logits": outputs,
            "list_scores": list_scores,
            "list_labels": list_labels,
        }
