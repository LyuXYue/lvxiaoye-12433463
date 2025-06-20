import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 读取Excel数据
file_path = "combined_codon_data.xlsx"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"数据文件 {file_path} 未找到，请确保它在当前目录")

try:
    df = pd.read_excel(file_path, sheet_name="Sheet1")
except Exception as e:
    raise ValueError(f"读取Excel文件失败: {str(e)}")


# 1. 柱状图：比较物种间特定氨基酸的同义密码子使用偏好
def plot_codon_usage_bar(amino_acid):
    plt.figure(figsize=(14, 8))
    subset = df[df['Amino Acid'] == amino_acid]

    if subset.empty:
        print(f"警告: 数据中没有找到氨基酸 '{amino_acid}' 的信息")
        return

    # 确保所有物种数据存在
    species_palette = {'Human': '#4C72B0', 'Mouse': '#55A868', 'Yeast': '#C44E52'}
    ax = sns.barplot(
        x='Triplet',
        y='Fraction',
        hue='Species',
        data=subset,
        palette=species_palette,
        edgecolor='black'
    )

    plt.title(f'{amino_acid} 氨基酸的同义密码子使用偏好', fontsize=18, pad=20)
    plt.xlabel('密码子', fontsize=14)
    plt.ylabel('使用比例 (Fraction)', fontsize=14)
    plt.ylim(0, 1.05)
    plt.legend(title='物种', loc='best', fontsize=12)

    # 添加数据标签
    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(
                f'{height:.2f}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', va='center',
                xytext=(0, 5),
                textcoords='offset points',
                fontsize=10
            )

    plt.tight_layout()
    plt.savefig(f'{amino_acid}_codon_usage.png', dpi=300)
    plt.show()


# 2. 散点图：比较人类和小鼠密码子使用频率
def plot_species_correlation():
    # 创建人类-小鼠数据透视表
    human = df[df['Species'] == 'Human'][['Triplet', 'Frequency']]
    mouse = df[df['Species'] == 'Mouse'][['Triplet', 'Frequency']]
    merged = pd.merge(human, mouse, on='Triplet', suffixes=('_Human', '_Mouse'))

    if merged.empty:
        print("警告: 没有找到足够的数据进行相关性分析")
        return

    # 计算相关系数
    corr_coef = np.corrcoef(merged['Frequency_Human'], merged['Frequency_Mouse'])[0, 1]

    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='Frequency_Human',
        y='Frequency_Mouse',
        data=merged,
        s=100,
        color='#1f77b4',
        edgecolor='w',
        alpha=0.8
    )

    # 添加回归线和相关系数
    sns.regplot(
        x='Frequency_Human',
        y='Frequency_Mouse',
        data=merged,
        scatter=False,
        color='#d62728',
        line_kws={'lw': 2}
    )

    plt.title('人类 vs 小鼠密码子使用频率相关性', fontsize=18, pad=15)
    plt.xlabel('人类密码子使用频率 (%)', fontsize=14)
    plt.ylabel('小鼠密码子使用频率 (%)', fontsize=14)

    # 修复此处括号不匹配的问题
    plt.text(
        0.05, 0.92,
        f'相关系数 r = {corr_coef:.3f}',
        transform=plt.gca().transAxes,
        fontsize=14,
        bbox=dict(facecolor='white', alpha=0.8)
    )  # 这里添加了缺失的右括号

    plt.tight_layout()
    plt.savefig('human_mouse_correlation.png', dpi=300)
    plt.show()


# 3. 热图：密码子偏好熵值比较（不使用SciPy）
def calculate_entropy(freqs):
    """计算密码子使用偏好的熵值"""
    freqs = np.array(freqs)
    freqs = freqs[freqs > 0]  # 移除零值
    if len(freqs) <= 1:
        return 0.0  # 只有一个密码子时熵为0
    freqs = freqs / freqs.sum()  # 标准化
    return -np.sum(freqs * np.log2(freqs))


def plot_codon_entropy_heatmap():
    # 计算每个氨基酸-物种组的熵值
    entropy_data = []
    for (aa, species), group in df.groupby(['Amino Acid', 'Species']):
        if len(group) > 1:  # 只考虑有多个密码子的氨基酸
            freqs = group['Fraction'].values
            ent = calculate_entropy(freqs)
            entropy_data.append([aa, species, ent])

    if not entropy_data:
        print("警告: 没有足够的数据计算熵值")
        return

    entropy_df = pd.DataFrame(entropy_data, columns=['Amino Acid', 'Species', 'Entropy'])

    # 数据透视
    pivot_df = entropy_df.pivot(index='Amino Acid', columns='Species', values='Entropy')

    plt.figure(figsize=(14, 10))
    ax = sns.heatmap(
        pivot_df,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar_kws={'label': '密码子偏好熵值'},
        linewidths=0.5,
        annot_kws={"size": 10}
    )

    plt.title('不同物种氨基酸密码子偏好熵值比较', fontsize=18, pad=20)
    plt.xlabel('物种', fontsize=14)
    plt.ylabel('氨基酸', fontsize=14)
    cbar = ax.collections[0].colorbar
    cbar.set_label('熵值 (bits)', fontsize=12)

    plt.tight_layout()
    plt.savefig('codon_entropy_heatmap.png', dpi=300)
    plt.show()


# 4. 箱线图：密码子频率分布比较
def plot_frequency_distribution():
    plt.figure(figsize=(12, 8))
    species_order = ['Human', 'Mouse', 'Yeast']

    sns.boxplot(
        x='Species',
        y='Frequency',
        data=df,
        order=species_order,
        palette={'Human': '#4C72B0', 'Mouse': '#55A868', 'Yeast': '#C44E52'},
        showfliers=False,
        width=0.6
    )

    # 添加数据点
    sns.stripplot(
        x='Species',
        y='Frequency',
        data=df,
        order=species_order,
        color='black',
        alpha=0.3,
        size=4,
        jitter=True
    )

    plt.title('密码子使用频率分布比较', fontsize=18, pad=15)
    plt.xlabel('物种', fontsize=14)
    plt.ylabel('使用频率 (%)', fontsize=14)

    plt.tight_layout()
    plt.savefig('frequency_distribution.png', dpi=300)
    plt.show()


# 主程序
if __name__ == "__main__":
    print("开始密码子使用偏好分析...")

    # 检查数据列是否存在
    required_columns = ['Triplet', 'Amino Acid', 'Fraction', 'Frequency', 'Species']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"错误: 数据文件中缺少必要的列: {', '.join(missing_cols)}")
    else:
        print("数据加载成功，开始生成图表...")
        plot_codon_usage_bar('L')  # 亮氨酸有6个密码子，适合比较
        plot_species_correlation()
        plot_codon_entropy_heatmap()
        plot_frequency_distribution()

        # 保存处理后的数据到CSV
        df.to_csv('processed_codon_data.csv', index=False)
        print("分析完成! 图表已保存到当前目录")