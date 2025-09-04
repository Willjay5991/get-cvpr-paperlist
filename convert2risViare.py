import re



# 解析BibTeX字符串的简单函数
def parse_bibtex(bibtex_str):
    entries = []
    # 使用正则表达式分割不同的BibTeX条目
    pattern = r'@(\w+)\{([^,]+),\s*([^@]*)\}'
    matches = re.findall(pattern, bibtex_str, re.DOTALL)
    
    for match in matches:
        entry_type, cite_key, fields_str = match
        fields = {}
        
        # 解析字段
        field_pattern = r'(\w+)\s*=\s*\{([^}]*)\}'
        field_matches = re.findall(field_pattern, fields_str)
        
        for field_name, field_value in field_matches:
            fields[field_name.lower()] = field_value
        
        entries.append({
            'type': entry_type.lower(),
            'cite_key': cite_key,
            'fields': fields
        })
    
    return entries



# 定义BibTeX到RIS的映射
type_mapping = {
    'inproceedings': 'CONF',
    'article': 'JOUR',
    'book': 'BOOK',
    'phdthesis': 'THES',
    'mastersthesis': 'THES'
}

# 月份映射
month_mapping = {
    'jan': '01', 'january': '01',
    'feb': '02', 'february': '02',
    'mar': '03', 'march': '03',
    'apr': '04', 'april': '04',
    'may': '05',
    'jun': '06', 'june': '06',
    'jul': '07', 'july': '07',
    'aug': '08', 'august': '08',
    'sep': '09', 'september': '09',
    'oct': '10', 'october': '10',
    'nov': '11', 'november': '11',
    'dec': '12', 'december': '12'
}

# 转换函数
def convert_to_ris(entries):
    ris_entries = []
    
    for entry in entries:
        ris_lines = []
        fields = entry['fields']
        
        # 处理文献类型
        entry_type = entry['type']
        ris_type = type_mapping.get(entry_type, 'GEN')
        ris_lines.append(f"TY  - {ris_type}")
        
        # 处理作者
        if 'author' in fields:
            authors = fields['author'].split(' and ')
            for author in authors:
                ris_lines.append(f"AU  - {author}")
        
        # 处理标题
        if 'title' in fields:
            ris_lines.append(f"TI  - {fields['title']}")
        
        # 处理会议/期刊名称
        if 'booktitle' in fields:
            ris_lines.append(f"T2  - {fields['booktitle']}")
        elif 'journal' in fields:
            ris_lines.append(f"JO  - {fields['journal']}")
        
        # 处理年份
        if 'year' in fields:
            ris_lines.append(f"PY  - {fields['year']}")
        
        # 处理月份
        if 'month' in fields:
            month = fields['month'].lower()
            month_num = month_mapping.get(month, month)
            if 'year' in fields:
                ris_lines.append(f"DA  - {fields['year']}/{month_num}/01")
        
        # 处理页码
        if 'pages' in fields:
            pages = fields['pages'].replace('--', '-')
            ris_lines.append(f"SP  - {pages}")
        
        # 处理URL
        if 'url' in fields:
            ris_lines.append(f"UR  - {fields['url']}")
        
        # 处理DOI
        if 'doi' in fields:
            ris_lines.append(f"DO  - {fields['doi']}")
        
        # 添加结束标记
        ris_lines.append("ER  - ")
        ris_lines.append("")  # 空行分隔不同条目
        
        ris_entries.append("\n".join(ris_lines))
    
    return "\n".join(ris_entries), len(ris_entries)


if __name__ == "__main__":
    with open('1-cvpr-papers.bib', 'r', encoding='utf-8') as f:
        bibtex_str = f.read()
        print('have load bib file')
    # 解析BibTeX
    entries = parse_bibtex(bibtex_str)

    # 转换并输出RIS格式
    ris_output,num = convert_to_ris(entries)
    # print(ris_output)

    # 保存到文件
    with open("references.ris", "w", encoding="utf-8") as f:
        f.write(ris_output)
    print(f"have convert {num} bib entries to references.ris")
   