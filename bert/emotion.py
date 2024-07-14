#细粒度情感分析数据集
#https://huggingface.co/datasets/Falah/sentiments-dataset-381-classes
import pymysql
import torch
import torch.nn.functional as F
import json
from collections import Counter
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, BertConfig
import pandas as pd
def load_jsondata(datas, max_len):
    dataset_list = []
    dataset = datas['Abstract']
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    for item in dataset:
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
        dataset_list.append(item)
    return dataset_list

if __name__ == '__main__':
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='$wyh666$',
                           db='spider')
    cursor = conn.cursor()
    cursor.execute('SELECT id, url FROM spider_db')
    rows = cursor.fetchall()

    # 统计每个URL出现的次数
    url_counter = Counter(row[1] for row in rows)

    # 对于出现次数大于1的URL，删除它们，只保留一个
    for url, count in url_counter.items():
        if count > 1:
            # 查询所有具有相同URL的行
            cursor.execute('SELECT id FROM spider_db WHERE url = %s', (url,))
            ids = [row[0] for row in cursor.fetchall()]
            # 保留第一个id，删除其他的id
            for id in ids[1:]:
                # 删除具有相同URL但id不同的行
                print(f"Deleting row with id {id}")
                cursor.execute('DELETE FROM spider_db WHERE id = %s AND origin = %s', (id, "Baidu"))
    # 提交事务
    conn.commit()
    df = pd.read_sql('SELECT * FROM spider_db WHERE Positive is NULL', conn)
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM spider_db WHERE id = 4')
    # datas = list(cursor.fetchall())
    datasets = load_jsondata(df, 150)
    config = BertConfig.from_pretrained('bert-base-chinese')
    config.num_labels = 3
    model = BertForSequenceClassification.from_pretrained('bert-base-chinese', config=config)
    model.cpu()
    print('开始加载训练完成的model...')
    model.load_state_dict(torch.load('bert_cla.ckpt', map_location=torch.device('cpu')))
    print('开始测试...')
    model.eval()
    results = []
    for data in datasets:
        data_list = list(json.loads(data))
        text_tensor = torch.tensor(data_list).unsqueeze(0).cpu()
        with torch.no_grad():
            outputs = model(text_tensor, labels=None)
            pre = outputs[0].argmax(dim=1)
            prob = F.softmax(outputs[0], dim=1)
            results.append([pre.item(), prob[0][0].item(), prob[0][1].item(), prob[0][2].item()])
    for i in range(len(results)):
        processed_result = (results[i][1], results[i][2], results[i][3], df['id'][i])
        update_sql = "UPDATE spider_db SET Positive = %s, Neutral = %s, Negative = %s WHERE id = %s"
        cursor.execute(update_sql, processed_result)
    conn.commit()
    cursor.close()
    # for result in results:
    #     print(result)
    #     update_sql = "UPDATE spider_db set POSTIVE = %s where id=%s"