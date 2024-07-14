from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
from sklearn.metrics import accuracy_score
import torch

# 加载预训练模型tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

# 加载预训练模型 (weights)
config = BertConfig.from_pretrained('bert-base-chinese')
config.num_labels = 3
model = BertForSequenceClassification.from_pretrained('bert-base-chinese',config=config)

# 加载微调后的模型参数
model.load_state_dict(torch.load('bert_cla.ckpt',map_location=torch.device('cpu')))

# 输入文本和实际标签
input_text = ["你好，世界", "今天天气不错"]
labels = torch.tensor([0, 1])  # The labels for the two sentences

# 使用tokenizer对输入文本进行编码
input_ids = tokenizer(input_text, padding=True, truncation=True, max_length=512, return_tensors='pt')['input_ids']

# 使用模型进行预测
outputs = model(input_ids)

# 获取预测结果
predictions = torch.argmax(outputs.logits, dim=-1)

# 计算准确率
accuracy = accuracy_score(labels, predictions)

print(f'Accuracy: {accuracy}')