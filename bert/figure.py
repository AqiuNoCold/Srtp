import pandas as pd
import pyecharts.options as opts
import numpy as np
from pyecharts.charts import Line
data = pd.read_csv("result.csv", encoding='utf-8')
line = Line()
line.add_xaxis(data.index.tolist())
line.add_yaxis("loss",data["losses"].tolist(),
        label_opts=opts.LabelOpts(is_show=False),)
line.add_yaxis("accuracy",data["accs"].tolist(),
        label_opts=opts.LabelOpts(is_show=False),)
line.set_global_opts(
    title_opts=opts.TitleOpts(title="损失函数和准确率变化"),
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
)
line.render("caitest折线图.html")