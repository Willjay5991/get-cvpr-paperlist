import bibtexparser



# 解析BibTeX字符串
# parser = BibTexParser()
# parser.customization = homogenize_latex_encoding
# bib_database = bibtexparser.loads(bibtex_str, parser=parser)

import bibtexparser

# print(len(library.entries))
# print(type(library.entries[0]))
# print(library.entries[0].fields_dict)

# dict = library.entries[0].fields_dict
# for key in dict:
#     print(key, dict[key])
# 定义BibTeX到RIS的映射
type_mapping = {
    'inproceedings': 'CONF',
    'article': 'JOUR',
    'book': 'BOOK',
    'phdthesis': 'THES',
    'mastersthesis': 'THES'
}

def convert_bibtex_to_ris(bibtex_str):
    library = bibtexparser.parse_string(bibtex_str) # 解析bibTeX字符串
    ris_entries = []
    for entry in library.entries:
        ris_lines = []
        # dict = entry.fields_dict

        # ris_lines.append('TY  - JOUR')
        # paper['title'] = dict['title'].value
        # paper['author'] = dict['author'].value
        # paper['year'] = dict['year'].value
        # paper['booktitle']=dict['booktitle'].value
        # paper['url'] = dict['url'].value
        # paper['pages']
        
        # 处理文献类型
        entry_type = entry['ENTRYTYPE'].lower()
        ris_type = type_mapping.get(entry_type, 'GEN')
        ris_lines.append(f"TY  - {ris_type}")
            
        # 处理作者
        if 'author' in entry:
            authors = entry['author'].split(' and ')
            for author in authors:
                ris_lines.append(f"AU  - {author}")
            
        # 处理标题
        if 'title' in entry:
            ris_lines.append(f"TI  - {entry['title']}")
            
        # 处理会议/期刊名称
        if 'booktitle' in entry:
            ris_lines.append(f"T2  - {entry['booktitle']}")
        elif 'journal' in entry:
            ris_lines.append(f"JO  - {entry['journal']}")
            
        # 处理年份
        if 'year' in entry:
            ris_lines.append(f"PY  - {entry['year']}")
            
        # 处理月份
        if 'month' in entry:
            month = entry['month']
            if month.lower() in ['jan', 'january']:
                month_num = '01'
            elif month.lower() in ['feb', 'february']:
                month_num = '02'
            elif month.lower() in ['mar', 'march']:
                month_num = '03'
            elif month.lower() in ['apr', 'april']:
                month_num = '04'
            elif month.lower() in ['may']:
                month_num = '05'
            elif month.lower() in ['jun', 'june']:
                month_num = '06'
            elif month.lower() in ['jul', 'july']:
                month_num = '07'
            elif month.lower() in ['aug', 'august']:
                month_num = '08'
            elif month.lower() in ['sep', 'september']:
                month_num = '09'
            elif month.lower() in ['oct', 'october']:
                month_num = '10'
            elif month.lower() in ['nov', 'november']:
                month_num = '11'
            elif month.lower() in ['dec', 'december']:
                month_num = '12'
            else:
                month_num = month
            ris_lines.append(f"DA  - {entry['year']}/{month_num}/01")
            
            # 处理页码
            if 'pages' in entry:
                pages = entry['pages'].replace('--', '-')
                ris_lines.append(f"SP  - {pages}")
            
            # 处理URL
            if 'url' in entry:
                ris_lines.append(f"UR  - {entry['url']}")
            
            # 处理DOI
            if 'doi' in entry:
                ris_lines.append(f"DO  - {entry['doi']}")
            
            # 添加结束标记
            ris_lines.append("ER  - ")
            ris_lines.append("")  # 空行分隔不同条目
            
            ris_entries.append("\n".join(ris_lines))
        
    return "\n".join(ris_entries), len(ris_entries)



if __name__ == "__main__":
    # BibTeX输入字符串
    with open('1-cvpr-papers.bib', 'r') as bibtex_file:
        bibtex_str = bibtex_file.read()
        print('have load bib file')

    # 转换为RIS格式
    ris_output, num = convert_bibtex_to_ris(bibtex_str)
    # write to file
    with open("references.ris", "w", encoding="utf-8") as f:
        f.write(ris_output)
        print(f'have written {num} records to references.ris')