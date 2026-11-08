# Лабораторная работа 2, вариант 10
import csv
import random
import re
import xml.etree.ElementTree as ET
from collections import Counter


def extract_year(raw_text):
    """从单元格文本里抽出年份。既支持 '2002'，也支持 '15.10.2021 9:22'。"""
    if raw_text is None:
        return None
    found = re.findall(r"\d{4}", str(raw_text))
    if not found:
        return None
    try:
        return int(found[-1])
    except ValueError:
        return None


def try_read_csv(csv_path, year_column, start_year):
    """
    尝试读取 CSV 文件，依次测试俄语环境常见编码。
    :param csv_path: 文件路径
    :param year_column: 存储年份的列名
    :param start_year: 筛选的最小年份
    :return: 筛选后的图书列表，成功读取所用编码
    """
    candidate_encodings = ["cp1251", "utf-8", "koi8-r", "cp866"]
    for enc in candidate_encodings:
        try:
            filtered_records = []
            with open(csv_path, "r", encoding=enc, newline="") as file_obj:
                reader = csv.DictReader(file_obj, delimiter=";")
                for row in reader:
                    year = extract_year(row.get(year_column, ""))
                    if year is not None and year >= start_year:
                        filtered_records.append(row)
            print(f"✅ 文件 {csv_path} 使用编码：{enc}")
            return filtered_records, enc
        except UnicodeDecodeError:
            continue
    raise RuntimeError("所有候选编码都无法读取该文件！")


def get_currency_dictionary(xml_file_path):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    currency_map = dict()
    for valute in root.findall("Valute"):
        name_node = valute.find("Name")
        code_node = valute.find("CharCode")
        if name_node is not None and code_node is not None:
            currency_map[name_node.text.strip()] = code_node.text.strip()
    return currency_map


def count_long_titles(book_list, title_column, minimal_length=30):
    counter = 0
    for book in book_list:
        if len(book.get(title_column, "").strip()) > minimal_length:
            counter += 1
    return counter


def search_books_by_author(book_list, author_column, search_text, max_results=None):
    found_books = []
    query_lower = search_text.lower()
    for book in book_list:
        if query_lower in book.get(author_column, "").strip().lower():
            found_books.append(book)
            if max_results is not None and len(found_books) >= max_results:
                break
    return found_books


def save_random_selection(book_list, author_col, title_col, year_col, output_path, save_encoding, sample_count=20):
    if not book_list:
        return None
    sample_size = min(sample_count, len(book_list))
    selected = random.sample(book_list, sample_size)
    with open(output_path, "w", encoding=save_encoding) as out_file:
        for index, book in enumerate(selected, start=1):
            author = (book.get(author_col) or "").strip() or "Неизвестный автор"
            title = (book.get(title_col) or "").strip() or "Без названия"
            year_val = (book.get(year_col) or "????").strip()
            # 用普通短横线，避免 cp1251 编码写入长破折号乱码
            out_file.write(f"{index}. {author}. {title} - {year_val}\n")
    return output_path


def get_unique_publishers(book_list):
    publishers = set()
    for book in book_list:
        pub = book.get("Publisher", "").strip()
        if pub:
            publishers.add(pub)
    return sorted(publishers)


def get_most_popular_books(book_list, top_limit=20):
    all_titles = [book.get("Book-Title", "").strip() for book in book_list]
    titles = [t for t in all_titles if t]
    return Counter(titles).most_common(top_limit)


if __name__ == "__main__":
    XML_PATH = "currency.xml"
    BOOKS_RU_PATH = "books.csv"
    BOOKS_EN_PATH = "books-en.csv"
    RU_YEAR_COLUMN = "Дата поступления"
    EN_YEAR_COLUMN = "Year-Of-Publication"

    ru_subset, ru_enc = try_read_csv(BOOKS_RU_PATH, RU_YEAR_COLUMN, 2018)
    en_subset, en_enc = try_read_csv(BOOKS_EN_PATH, EN_YEAR_COLUMN, 2000)

    print("=" * 60)
    print("筛选结果：")
    print(f"  俄文 books.csv：保留 2018 年后图书，共 {len(ru_subset)} 本")
    print(f"  英文 books-en.csv：保留 2000 年后图书，共 {len(en_subset)} 本\n")

    print("=" * 60)
    print("1. 货币信息（名称 → 代码）")
    print("=" * 60)
    curr_dict = get_currency_dictionary(XML_PATH)
    for name, code in list(curr_dict.items())[:8]:
        print(f"  {name:35s} → {code}")
    print(f"  一共 {len(curr_dict)} 种货币\n")

    print("=" * 60)
    print("2. 俄文图书处理结果")
    print("=" * 60)
    print(f"  • 书名长度大于 30 的图书数量：{count_long_titles(ru_subset, 'Название')}")
    found_ru = search_books_by_author(ru_subset, "Автор", "Толстой", max_results=3)
    print("  • 搜索作者 'Толстой'，找到前 3 本：")
    for b in found_ru:
        print(f"    {b.get('Автор')} — {b.get('Название')} — {b.get('Дата поступления')}")
    out_ru = save_random_selection(ru_subset, "Автор", "Название", "Дата поступления", "bibliography_ru.txt", ru_enc)
    print(f"  • 随机选取的图书已保存到：{out_ru}\n")

    print("=" * 60)
    print("3. 英文图书处理结果")
    print("=" * 60)
    print(f"  • 书名长度大于 30 的图书数量：{count_long_titles(en_subset, 'Book-Title')}")
    found_en = search_books_by_author(en_subset, "Book-Author", "Rowling", max_results=3)
    print("  • 搜索作者 'Rowling'，找到前 3 本：")
    for b in found_en:
        print(f"    {b.get('Book-Author')} — {b.get('Book-Title')} — {b.get('Year-Of-Publication')}")
    out_en = save_random_selection(en_subset, "Book-Author", "Book-Title", "Year-Of-Publication", "bibliography_en.txt", en_enc)
    print(f"  • 随机选取的图书已保存到：{out_en}\n")

    print("=" * 60)
    print("4. 英文数据集附加任务结果")
    print("=" * 60)
    publisher_list = get_unique_publishers(en_subset)
    print(f"  • 不重复出版商总数：{len(publisher_list)}，前 10 家：")
    for pub in publisher_list[:10]:
        print(f"    {pub}")
    print("  • 出现频次最高的前 20 本书：")
    for rank, (title, cnt) in enumerate(get_most_popular_books(en_subset), start=1):
        print(f"    {rank:2d}. {title}（出现 {cnt} 次）")
