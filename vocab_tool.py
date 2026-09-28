import csv

def load_vocab(csv_path):
    """读取csv生词表，返回词汇列表（字典形式）"""
    vocab_list = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vocab_list.append(row)
    return vocab_list

def group_by_pos(vocab_list):
    """按词性分组，key=词性，value=对应单词列表"""
    pos_groups = {}
    for item in vocab_list:
        pos = item["词性"]
        if pos not in pos_groups:
            pos_groups[pos] = []
        pos_groups[pos].append(item)
    return pos_groups

def generate_exercise(vocab_list, out_file="练习.txt"):
    """按词性分组输出，写入练习.txt"""
    total = len(vocab_list)
    pos_groups = group_by_pos(vocab_list)
    lines = []
    lines.append(f"生词总数量：{total}")
    lines.append("=" * 35)

    for pos, word_list in pos_groups.items():
        lines.append(f"\n【词性：{pos}】共 {len(word_list)} 个词")
        for word_info in word_list:
            lines.append(f"HSK{word_info['HSK等级']} | {word_info['词汇']}：{word_info['释义']}")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"生词总数量：{total}")
    for pos, word_list in pos_groups.items():
        print(f"  {pos}: {len(word_list)} 个")
    print(f"✅ 文件已生成：{out_file}")

if __name__ == "__main__":
    vocab_data = load_vocab("data/生词表.csv")
    generate_exercise(vocab_data) 