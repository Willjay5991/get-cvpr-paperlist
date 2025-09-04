from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm


def get_abstract(url):
    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 查找abstract部分 - CVPR论文页面通常将摘要放在特定位置
        # 方法1: 查找包含"Abstract"的div
        abstract_div = soup.find('div', string=re.compile('Abstract', re.I))
        
        # 方法2: 如果上述方法失败，尝试查找特定类名或id
        if not abstract_div:
            abstract_div = soup.find('div', {'id': 'abstract'})
        
        if not abstract_div:
            abstract_div = soup.find('div', class_=re.compile('abstract', re.I))
        
        # 提取abstract文本内容
        if abstract_div:
            # 获取abstract的下一个兄弟节点或父节点的文本
            abstract_text = abstract_div.find_next('p').text if abstract_div.find_next('p') else abstract_div.text
            return abstract_text.strip()
        else:
            return "未能找到abstract部分，可能是页面结构发生了变化。"
            
    except requests.RequestException as e:
        return f"请求错误: {str(e)}"
    except Exception as e:
        return f"处理错误: {str(e)}"
    

def extract_paper_info(url):
    """
    模拟浏览器操作，从url中提取论文的BibTeX引用和URL链接
    
    参数:
        url: 
        
    返回:
        包含论文信息的列表，论文信息为包含url的bibtex
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        
        # 使用BeautifulSoup解析HTML内容
        print('loading html file...')
        soup = BeautifulSoup(response.content, 'html.parser')

        paper_elements = soup.find_all('dt', class_='ptitle')
    
        papers = []
    
        for paper_element in tqdm(paper_elements):
            # 提取论文标题和URL
            title_link = paper_element.find('a')
            if title_link:
                title = title_link.get_text()
                url = "https://openaccess.thecvf.com" + title_link['href']
                
                # 找到紧随的两个dd元素
                next_dd_elements = paper_element.find_next_siblings('dd', limit=2)
                
                if len(next_dd_elements) >= 2:
                    # 第二个dd元素包含BibTeX信息
                    second_dd = next_dd_elements[1]
                    
                    # 查找BibTeX div
                    bibtex_div = second_dd.find('div', class_='bibref')
                    if bibtex_div:
                        bibtex = bibtex_div.get_text(strip=True)
                    else:
                        bibtex = "BibTeX not found"
                else:
                    bibtex = "BibTeX not found"
                
                # insert url to bibtex
                bibtex = bibtex.replace('\n}', ',\n   url={'+f'{url.strip()}'+'}\n}')                                
                papers.append(f"{bibtex}\n")
        print(f'have findd {len(papers)} papers')
        return papers

    except requests.RequestException as e:
        print(f"请求错误: {str(e)}")
        return -1
    except Exception as e:
        print(f"处理错误: {str(e)}")
        return -1


def wirte_to_file(papers, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        print('writing to file...')
        for paper in papers:
            f.write(f"{paper}\n")

# 示例使用
if __name__ == "__main__":
    # 假设html_content是您提供的HTML字符串
    # 这里我们直接从您提供的HTML内容中提取
    # 读取HTML文件
    url = 'https://openaccess.thecvf.com/CVPR2025?day=all'
    
    outfile_name = 'cvpr-papers'
    papers = extract_paper_info(url)
    bibtex_str = '\n'.join(papers)
    if papers != -1:
        with open(f'{outfile_name}.bib', 'w', encoding='utf-8') as f:
            print('writing to file...')
            f.write(bibtex_str)
        print("have writen {} paper infors into {}.bib".format(len(papers),outfile_name))

    
    # convert bibtex to ris
    from convert2risViare import *

    # 解析BibTeX
    entries = parse_bibtex(bibtex_str)

    # 转换并输出RIS格式
    ris_output,num = convert_to_ris(entries)
    # print(ris_output)

    # 保存到文件
    with open(f"{outfile_name}.ris", "w", encoding="utf-8") as f:
        f.write(ris_output)
    print(f"have convert {num} bib entries to {outfile_name}.ris")
    