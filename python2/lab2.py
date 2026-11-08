# Лабораторная работа 2, вариант 10
import csv
import random
import xml.etree.ElementTree as ET
from collections import Counter
def try_read_csv(csv_path, year_column, start_year):
    """
    尝试读取 CSV 文件，依次测试俄语环境常见编码。
    如果某个编码读取成功，就返回解析后的数据和该编码；全部失败则抛出异常。
    :param csv_path: 文件路径
    :param year_column: 存储年份的列名
    :param start_year: 筛选的最小年份
    :return: 筛选后的图书列表，成功读取所用编码
    """
    candidate_encodings = ["cp1251", "utf-8", "koi8-r", "cp866"]  # 俄语环境常用编码列表
    for enc in candidate_encodings:  # 逐个尝试每一种编码
        try:
            filtered_records = []  # 存放筛选完成后的图书记录
            with open(csv_path, "r", encoding=enc, newline="") as file_obj:  # 打开文件，自动关闭
                reader = csv.DictReader(file_obj, delimiter=";")  # 使用分号作为字段分隔符
                for row in reader:  # 遍历文件里每一行
                    raw_year = row.get(year_column, "").strip()  # 获取年份，去除首尾空白
                    try:
                        year = int(raw_year)  # 将年份转为整数
                        if year >= start_year:  # 判断是否满足年份筛选条件
                            filtered_records.append(row)
                    except ValueError:  # 如果无法转成数字，跳过这一行
                        continue
            print(f"✅ 文件 {csv_path} 使用编码：{enc}")
            return filtered_records, enc  # 返回数据和识别到的编码
        except UnicodeDecodeError:  # 当前编码无法解码，继续试下一个
            continue
    raise RuntimeError("所有候选编码都无法读取该文件！")  # 全部编码失败，抛出错误
def get_currency_dictionary(xml_file_path):
    """
    读取 currency.xml，构造字典：货币名称 → 货币代码。
    :param xml_file_path: xml 文件路径
    :return: 货币映射字典
    """
    tree = ET.parse(xml_file_path)  # 解析 XML 文件
    root = tree.getroot()  # 获取 XML 的根节点
    currency_map = dict()  # 创建字典保存货币信息
    for valute in root.findall("Valute"):  # 遍历每一个货币节点
        name_node = valute.find("Name")  # 获取货币名称节点
        code_node = valute.find("CharCode")  # 获取货币代码节点
        if name_node is not None and code_node is not None:  # 如果两个节点都存在
            currency_name = name_node.text.strip()
            currency_code = code_node.text.strip()
            currency_map[currency_name] = currency_code
    return currency_map
def count_long_titles(book_list, title_column, minimal_length=30):
    """
    统计书名长度超过指定阈值的图书数量。
    :param book_list: 图书数据列表
    :param title_column: 书名列名
    :param minimal_length: 长度阈值
    :return: 符合条件的图书总数
    """
    counter = 0
    for book in book_list:
        title = book.get(title_column, "").strip()
        if len(title) > minimal_length:
            counter += 1
    return counter
def search_books_by_author(book_list, author_column, search_text, max_results=None):
    """
    根据作者名字片段搜索图书，搜索忽略大小写。
    :param book_list: 图书列表
    :param author_column: 作者列名
    :param search_text: 需要查找的关键词
    :param max_results: 返回结果数量上限
    :return: 找到的图书列表
    """
    found_books = []
    query_lower = search_text.lower()  # 将搜索词转为小写
    for book in book_list:
        author = book.get(author_column, "").strip().lower()
        if query_lower in author:
            found_books.append(book)
            if max_results is not None and len(found_books) >= max_results:
                break  # 如果达到数量上限，提前退出循环
    return found_books
def save_random_selection(book_list, author_col, title_col, year_col, output_path, save_encoding, sample_count=20):
    """
    在图书列表里随机选取若干本，写入到文本文件。
    :param book_list: 图书列表
    :param author_col: 作者列名
    :param title_col: 书名列名
    :param year_col: 年份列名
    :param output_path: 输出文件路径
    :param save_encoding: 文件保存编码
    :param sample_count: 需要随机抽取的数量
    :return: 输出文件路径
    """
    sample_size = min(sample_count, len(book_list))  # 防止抽样数量超过总记录数
    selected = random.sample(book_list, sample_size)  # 无放回随机抽取
    with open(output_path, "w", encoding=save_encoding) as out_file:
        for index, book in enumerate(selected, start=1):
            author = book.get(author_col, "Неизвестный автор").strip()
            title = book.get(title_col, "Без названия").strip()
            year_val = book.get(year_col, "????").strip()
            out_file.write(f"{index}. {author}. {title} — {year_val}\n")
    return output_path
def get_unique_publishers(book_list):
    """
    获取所有不重复的出版商名称，并按字母顺序排序。
    :param book_list: 图书列表
    :return: 排序后的出版商列表
    """
    publishers = set()  # 使用集合自动去重
    for book in book_list:
        pub = book.get("Publisher", "").strip()
        if pub:
            publishers.add(pub)
    return sorted(publishers)
def get_most_popular_books(book_list, top_limit=20):
    """
    统计书名出现频次，返回出现最多的若干本书。
    :param book_list: 图书列表
    :param top_limit: 返回数量
    :return: (书名, 出现次数) 的列表
    """
    all_titles = []
    for book in book_list:
        title = book.get("Book-Title", "").strip()
        if title:
            all_titles.append(title)
    return Counter(all_titles).most_common(top_limit)

if __name__ == "__main__":
    XML_PATH = "currency.xml"
    BOOKS_RU_PATH = "books.csv"
    BOOKS_EN_PATH = "books-en.csv"
    # 读取俄文图书，筛选 2018 年及之后出版
    ru_subset, ru_enc = try_read_csv(
        BOOKS_RU_PATH,
        year_column="Год",
        start_year=2018
    )
    # 读取英文图书，筛选 2000 年及之后出版
    en_subset, en_enc = try_read_csv(
        BOOKS_EN_PATH,
        year_column="Year",
        start_year=2000
    )
    # 新增：完整全部英文图书，无年份过滤，用于统计流行书籍
    en_full, _ = try_read_csv(
        BOOKS_EN_PATH,
        year_column="Year",
        start_year=0
    )

    print("=" * 60)
    print("筛选结果：")
    print(f"  俄文 books.csv：保留 2018 年后出版图书，一共 {len(ru_subset)} 本")
    print(f"  英文 books-en.csv：保留 2000 年后出版图书，一共 {len(en_subset)} 本")
    print(f"  英文【全部原始】数据集总记录：{len(en_full)} 本\n")

    # 任务 1：解析 XML 获取货币信息
    print("=" * 60)
    print("1. 货币信息（名称 → 代码）")
    print("=" * 60)
    curr_dict = get_currency_dictionary(XML_PATH)
    for name, code in list(curr_dict.items())[:8]:
        print(f"  {name:35s} → {code}")
    print(f"  一共 {len(curr_dict)} 种货币\n")

    # 任务 2：处理俄文图书
    print("=" * 60)
    print("2. 俄文图书处理结果")
    print("=" * 60)
    ru_long_count = count_long_titles(ru_subset, title_column="Название")
    print(f"  • 书名长度大于 30 的图书数量：{ru_long_count}")
    found_ru = search_books_by_author(
        ru_subset,
        author_column="Автор",
        search_text="Толстой",
        max_results=3
    )
    print(f"  • 搜索作者 'Толстой'，找到前 3 本：")
    for b in found_ru:
        print(f"    {b.get('Автор')} — {b.get('Название')} — {b.get('Год')}")
    ru_output_file = save_random_selection(
        ru_subset,
        author_col="Автор",
        title_col="Название",
        year_col="Год",
        output_path="bibliography_ru.txt",
        save_encoding=ru_enc
    )
    print(f"  • 随机选取的图书已保存到：{ru_output_file}\n")

    # 任务 3：处理英文图书
    print("=" * 60)
    print("3. 英文图书处理结果")
    print("=" * 60)
    en_long_count = count_long_titles(en_subset, title_column="Book-Title")
    print(f"  • 书名长度大于 30 的图书数量：{en_long_count}")
    found_en = search_books_by_author(
        en_subset,
        author_column="Book-Author",
        search_text="Rowling",
        max_results=3
    )
    print(f"  • 搜索作者 'Rowling'，找到前 3 本：")
    for b in found_en:
        print(f"    {b.get('Book-Author')} — {b.get('Book-Title')} — {b.get('Year')}")
    en_output_file = save_random_selection(
        en_subset,
        author_col="Book-Author",
        title_col="Book-Title",
        year_col="Year",
        output_path="bibliography_en.txt",
        save_encoding=en_enc
    )
    print(f"  • 随机选取的图书已保存到：{en_output_file}\n")

    # 任务 4：英文数据集附加任务
    print("=" * 60)
    print("4. 英文数据集附加任务结果")
    print("=" * 60)
    publisher_list = get_unique_publishers(en_subset)
    print(f"  • 不重复出版商总数：{len(publisher_list)}，前 10 家：")
    for pub in publisher_list[:10]:
        print(f"    {pub}")
    print(f"  • 出现频次最高的前 20 本书：")
    # 这里用 en_full（完整数据集）而不是 en_subset
    for rank, (title, cnt) in enumerate(get_most_popular_books(en_full), start=1):
        print(f"    {rank:2d}. {title}（出现 {cnt} 次）")