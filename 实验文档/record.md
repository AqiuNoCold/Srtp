# 实验记录



## 实验环境

Linux server2.researchsn.io 3.10.0-1160.105.1.el7.x86_64 #1 SMP Thu Dec 7 15:39:45 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux

NVIDIA-SMI 535.104.05             Driver Version: 535.104.05   CUDA Version: 12.2.      NVIDIA GeForce RTX 4080 * 2

```python
#Anaconda 3 (necessary only)
jinja2 = 3.1.3
accelerate = 0.32.1
huggingface-hub = 0.23.4
matplotlib = 3.7.2
matplotlib-inline = 0.1.6
numpy = 1.24.4
pandas = 1.4.4
tensorboard = 2.14.0
tensorboardx = 2.6.2.2
tensorboard-data-server = 0.7.2
tokenizers = 0.19.1
torch = 2.2.1
tqdm = 4.65.0
transformers = 4.42.3
```

## 新闻情感分类

### 数据集：

CCF 互联网情感分析大赛新闻三分类数据集



## 新闻文本分类

### 数据集：

![截屏2024-07-14 16.59.16](../../实验数据记录/截屏2024-07-14%2016.59.16.png)

目前处在对数据集进行预处理的阶段



### 模型选择

google-bert/[bert-base-chinese](https://huggingface.co/google-bert/bert-base-chinese)