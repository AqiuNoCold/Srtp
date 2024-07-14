import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig, AdamW

import csv
import json
import numpy as np
import pandas as pd

# 超参数
EPOCHS = 5  # 训练的轮数
BATCH_SIZE = 16  # 批大小
MAX_LEN = 300  # 文本最大长度
LR = 1e-5  # 学习率
WARMUP_STEPS = 100  # 热身步骤
T_TOTAL = 1000  # 总步骤

# pytorch的dataset类 重写getitem,len方法
class Custom_dataset(Dataset):
    def __init__(self, dataset_list):
        self.dataset = dataset_list

    def __getitem__(self, item):
        text = self.dataset[item][1]
        label = self.dataset[item][2]

        return text, label

    def __len__(self):
        return len(self.dataset)


# 加载数据集
def load_jsondata(filepath, max_len):
    dataset_list = []
    data = pd.read_json(filepath, encoding='utf-8')
    dataset = data['Abstract']
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    count = 0
    for item in dataset:
        #if(count <= 10):
        #    print("json item start", item)

        item = item.replace(' ', '')
        num = max_len - len(item)
        if num < 0:
            item = item[:max_len]
            item = tokenizer.encode(item)
            num_temp = max_len - len(item)
            if num_temp > 0:
                for _ in range(num_temp):
                    item.append(0)
            # 在开头和结尾加[CLS] [SEP]
            item = [101] + item + [102]
            item = str(item)
            continue

        for _ in range(num):
            item = item + '[PAD]'
        item = tokenizer.encode(item)
        num_temp = max_len - len(item)
        if num_temp > 0:
            for _ in range(num_temp):
                item.append(0)
        item = [101] + item + [102]
        item = str(item)
        #if(count <= 10):
        #    print("json item end",item)
        #    count += 1
        dataset_list.append(item)
    #print("jsondataset", dataset_list)
    return dataset_list

# 计算每个batch的准确率
def batch_accuracy(pre, label):
    pre = pre.argmax(dim=1)
    correct = torch.eq(pre, label).sum().float().item()
    accuracy = correct / float(len(label))

    return accuracy


if __name__ == "__main__":

    # 生成数据集以及迭代器
    #train_dataset = load_dataset('Train.csv', max_len=MAX_LEN)  # 7337 * 3
    #test_dataset = load_dataset('Test.csv', max_len=MAX_LEN)  # 7356 * 3
    test_dataset = load_jsondata('test.json', 150)

    #train_cus = Custom_dataset(train_dataset)
    #train_loader = DataLoader(dataset=train_cus, batch_size=BATCH_SIZE, shuffle=False)
    # Bert模型以及相关配置
    config = BertConfig.from_pretrained('bert-base-chinese')
    config.num_labels = 3
    model = BertForSequenceClassification.from_pretrained('bert-base-chinese', config=config)
    model.cpu()
    '''
    optimizer = AdamW(model.parameters(), lr=LR, correct_bias=False)
    scheduler = WarmupLinearSchedule(optimizer, warmup_steps=WARMUP_STEPS, t_total=T_TOTAL)

    # optimizer = optim.Adam(model.parameters(), lr=LR)
    
    model.train()
    print('开始训练...')
    for epoch in range(EPOCHS):
        for text, label in train_loader:
            text_list = list(map(json.loads, text))
            label_list = list(map(json.loads, label))

            text_tensor = torch.tensor(text_list).cuda()
            label_tensor = torch.tensor(label_list).cuda()

            outputs = model(text_tensor, labels=label_tensor)
            loss, logits = outputs[:2]
            optimizer.zero_grad()
            loss.backward()
            scheduler.step()
            optimizer.step()

            acc = batch_accuracy(logits, label_tensor)
            print('epoch:{} | acc:{} | loss:{}'.format(epoch, acc, loss))

    torch.save(model.state_dict(), 'bert_cla.ckpt')
    print('保存训练完成的model...')
    '''
    # 测试

    print('开始加载训练完成的model...')
    model.load_state_dict(torch.load('bert_cla.ckpt',map_location=torch.device('cpu')))

    print('开始测试...')
    model.eval()
    test_result = []
    count = 2
    for item in test_dataset:
        text_list = list(json.loads(item))
        text_tensor = torch.tensor(text_list).unsqueeze(0).cpu()

        with torch.no_grad():
            outputs = model(text_tensor, labels=None)
            pre = outputs[0].argmax(dim=1)
            prob = F.softmax(outputs[0], dim=1)
            test_result.append([count, pre.item(), prob[0][0].item(), prob[0][1].item(), prob[0][2].item()])
            count += 1
    # 写入csv文件
    df = pd.DataFrame(test_result)
    df.to_csv('my_test_result.csv', index=False, header=['id', 'label', 'prob0', 'prob1', 'prob2'])

    print('测试完成，快提交结果吧')