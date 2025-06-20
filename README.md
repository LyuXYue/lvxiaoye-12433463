# 密码子使用偏好比较分析项目

## 项目概述
本项目通过生物信息学方法，系统比较了人类、小鼠和酿酒酵母的密码子使用偏好模式。研究分析了物种间密码子选择的相似性与差异性，探讨了进化过程中的保守机制和适应性分化。研究包含四种可视化分析：密码子使用比例比较、物种间相关性分析、密码子偏好熵值计算和密码子频率分布特征分析。

## 文件结构
codon_usage_analysis/
├──data/#原始数据
│└──combined_codon_data.xlsx

├──scripts/#分析代码
│└──codon_analysis.py

├──results/#分析结果图表
│├──L_codon_usage.png#亮氨酸密码子使用柱状图
│├──human_mouse_correlation.png#人鼠相关性散点图
│├──codon_entropy_heatmap.png#熵值热图
│└──frequency_distribution.png#频率分布箱线图
├──processed_codon_data.csv#处理后的数据
├──requirements.txt#依赖库列表
└──README.md#项目说明文件

## 快速开始指南

### 1. 环境配置
确保安装以下Python库：
```bash
pip install pandas matplotlib seaborn openpyxl numpy
```

### 2. 运行分析
将数据文件combined_codon_data.xlsx放在项目根目录，然后运行：
```bash
python scripts/codon_analysis.py
```

### 3. 查看结果
L_codon_usage.png：亮氨酸密码子使用比例比较；
human_mouse_correlation.png：人类与小鼠密码子频率相关性；
codon_entropy_heatmap.png：密码子偏好熵值热图；
frequency_distribution.png：密码子频率分布箱线图。


## 数据来源
来自[Kazusa密码子数据库]()的人类、小鼠、酿酒酵母的密码子三联体(Triplet)、对应氨基酸(Amino Acid)使用比例(Fraction)、使用频率(Frequency)、出现次数(Number)、物种(Species)


## 分析方法
1.数据处理
使用pandas读取和清洗Excel数据
提取关键字段：密码子、氨基酸、使用比例、频率和物种

2.密码子偏好分析
用比例计算：同义密码子在氨基酸中的相对使用频率
香农熵计算：量化密码子偏好强度
```python
  def calculate_entropy(freqs):
      freqs = np.array(freqs)
      freqs = freqs[freqs > 0]  # 移除零值
      if len(freqs) <= 1:
          return 0.0
      freqs = freqs / freqs.sum()  # 标准化
      return -np.sum(freqs * np.log2(freqs))
```
3.可视化方法 	
柱状图分析特定氨基酸的同义密码子使用比例
散点图分析人类与小鼠密码子频率相关性
热图分析密码子偏好熵值分布
箱线图分析密码子频率整体分布

## 关键结果展示
亮氨酸密码子使用比例：人类和小鼠高度偏好CUG密码子(>40%)；酵母偏好UUG密码子(29%)；所有物种极少使用UUA密码子
![亮氨酸密码子使用比较](results/L_codon_usage.png)

人类-小鼠密码子频率相关性：极强正相关(r=0.99)；回归线接近理想对角线(y=x)
![人类小鼠相关性](results/human_mouse_correlation.png)

密码子偏好熵值热图：色氨酸(W)和甲硫氨酸(M)熵值=0(完全保守)；精氨酸(R)在所有物种中熵值最高；酵母整体熵值比哺乳动物高32%
![熵值热图](results/codon_entropy_heatmap.png)

密码子频率分布：人类和小鼠分布相似(中位数17%)；酵母分布范围更广(IQR:18-32%)
![频率分布](results/frequency_distribution.png)

依赖库：pandas(数据处理)、numpy(数值计算)、matplotlib(基础可视化)、seaborn(高级可视化)、openpyxl(Excel文件读取)

## 结论
哺乳动物保守性：人类和小鼠密码子使用高度相似(r>0.99)
酵母适应性：更均匀的密码子使用(高熵值)适应环境变化
功能约束：必需氨基酸(W/M)完全保守，多密码子氨基酸(R/L)分化进化
