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

本文中所用的数据集清华NLP组提供的THUCNews新闻文本分类数据集的一个子集（原始的数据集大约74万篇文档，训练起来需要花较长的时间）。 本次训练使用了其中的体育, 财经, 房产, 家居, 教育, 科技, 时尚, 时政, 游戏, 娱乐10个分类，每个分类6500条，总共65000条新闻数据。每个分类6500条，总共65000条新闻数据。数据集划分如下： cnews.train.txt: 训练集(50000条) cnews.val.txt: 验证集(5000条) cnews.test.txt: 测试集(10000条)

数据集的格式为文本格式

```txt
体育 鲍勃库西奖归谁属？ NCAA最强控卫是坎巴还是弗神新浪体育讯如今，本赛季的NCAA进入到了末段，......
教育	留美学子安全手册：多渠道了解信息赴美准备1.多渠道了解信息知己知彼，百战不殆......
```

首先需要将训练文本和测试文本处理为csv格式，通过\t分割label和context，之后设置10列，使用one_hot编码。获得处理后的csv文件如下：

| 体育 | 财经 | 房产 | 家居 | 教育 | 科技 | 时尚 | 时政 | 游戏 | 娱乐 | content                                                      |
| ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ------------------------------------------------------------ |
| 1    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 0    | 鲍勃库西奖归谁属？ NCAA最强控卫是坎巴还是弗神新浪体育讯如今，本赛季的NCAA进入到了末段，...... |
| 0    | 0    | 0    | 0    | 1    | 0    | 0    | 0    | 0    | 0    | 留美学子安全手册：多渠道了解信息赴美准备1.多渠道了解信息知己知彼，百战不殆...... |

之后我们可以通过datasets库中的load_dataset()函数对csv文件直接进行读取，从而加载数据集。分别对 cnews.train.txt: 训练集(50000条)和cnews.test.txt: 测试集(10000条)分别进行处理，从而得到训练集和验证集，进而训练模型。

### 模型选择

google-bert/[bert-base-chinese](https://huggingface.co/google-bert/bert-base-chinese)

该模型已针对中文进行了预训练，训练和随机输入掩蔽已独立应用于词片段（如原始 BERT 论文中所述）。

- **开发者：** HuggingFace 团队
- **模型类型：**填充蒙版
- **语言：**中文
- **父模型：**有关 BERT 基础模型的更多信息，请参阅[BERT 基础无大小写模型。](https://huggingface.co/bert-base-uncased)

### 训练过程

**训练参数**

- **type_vocab_size:** 2
- **vocab_size:** 21128
- **num_hidden_layers:** 12
- **num_labels：** 10
- **batch_size：** 8

```shell
#run.sh
NCCL_IB_DISABLE=1 \
NCCL_P2P_DISABLE=1 \
CUDA_VISIBLE_DEVICES=0,1 \
TOKENIZERS_PARALLELISM=false \
python train.py
```

**训练集**:THUCNews新闻文本分类数据集的一个子集

**评估**:

- **F1_score:** 精确率 (Precision) 和召回率 (Recall) 的调和平均数。
- **Roc_auc:** 以假正率 (False Positive Rate) 为横轴，真正率 (True Positive Rate) 为纵轴绘制的曲线。AUC (Area Under Curve) 是 ROC 曲线下的面积。
- **Accuracy:** 正确预测的样本数占总样本数的比例。
- **Loss：**模型训练过程中的损失。

### 结果

<img src="eval_accuracy_vs_checkpoint.png" alt="eval_accuracy_vs_checkpoint" style="zoom:50%;" /><img src="eval_f1_vs_checkpoint.png" alt="eval_f1_vs_checkpoint" style="zoom:50%;" />

<img src="eval_loss_vs_checkpoint.png" alt="eval_loss_vs_checkpoint" style="zoom:50%;" /><img src="eval_roc_auc_vs_checkpoint.png" alt="eval_roc_auc_vs_checkpoint" style="zoom:50%;" /><img src="loss_vs_checkpoint.png" alt="loss_vs_checkpoint" style="zoom:50%;" />



从eval_loss可以看出，随着训练步数的增加，模型逐渐出现过拟合现象，因此，通过选择eval_accuracy最高的值来选择训练模型的选取。

最终选取eval_accuracy 最大值为 0.9679，对应的 checkpoint 是 14000.0，作为模型输出。

![截屏2024-07-29 14.11.12](截屏2024-07-29 14.11.12.png)


## 多模态文本-图片识别

### 数据集：

MUGE（Multimodal Understanding and Generation Evaluation Benchmark）是由阿里巴巴达摩院智能计算实验室联合浙江大学和阿里云天池平台共同发布的大规模中文多模态评测基准。它旨在推动多模态领域的研究和发展，特别是预训练和下游任务应用等方面。MUGE拥有目前最大规模的中文多模态评测数据集，覆盖了包括图文描述、基于文本的图像生成、跨模态检索等多种类型的任务。

数据集的组织如下图所示：\
${dataset_name} \
    ├── train_imgs.tsv      \
    ├── train_texts.jsonl    \
    ├── valid_imgs.tsv \
    ├── valid_texts.jsonl \
    ├── test_imgs.tsv \
    └── test_texts.jsonl 

其中train/valid/test_img.tsv包括图片ID与推按内容，train/valid/test_tests.jsonl包含文本ID，文本内容以及与该文本匹配的图片id列表

### 模型选择：
CLIP（Contrastive Language–Image Pre-training）是一种多模态学习模型，由OpenAI在2021年提出。CLIP模型通过对比学习的方式，学习图像与文本之间的关联性。它能够将图像和文本映射到同一个连续的向量空间中，使得相似的图像和文本在向量空间中彼此接近

CLIP模型的架构通常包括两个主要部分：一个图像编码器和一个文本编码器。图像编码器用于提取图像特征；文本编码器用于处理文本数据。这两个编码器的输出被映射到同一个向量空间，并通过对比学习的方式进行优化。

本项目的模型使用CLIP模型的中文版本Chinese-CLUP，使用大规模中文数据进行训练（~2亿图文对），旨在帮助用户快速实现中文领域的图文特征&相似度计算、跨模态检索、零样本图片分类等任务。具体使用的模型参数与规模如下表所示：

|模型规模|参数量|视觉侧骨架|视觉侧参数量|文本侧骨架|文本侧参数量|分辨率|
|-|-|-|-|-|-|-|
| CN-CLIPViT-L/14 | 406M | ViT-L/14 | 304M | RoBERTa-wwm-Base | 102M | 224 |


### 训练过程

**训练参数**

- **warmup:** 100
- **batch_size:** 64
- **valid_batch_size:** 64
- **learning_rate:** 5e-5
- **weight_decay:** 0.001
- **max_epochs:** 3
- **vision_model:** ViT-B-16
- **text_model:** RoBERTa-wwm-ext-base-chinese

**训练集**: MUGE数据集

**评估**:

- **Text_to_Image:** 正确预测的样本数占总样本数的比例。
- **Valid_Loss:** 模型训练过程中的损失。

### 结果


