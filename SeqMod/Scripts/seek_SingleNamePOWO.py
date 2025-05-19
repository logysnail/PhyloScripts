import pandas
import pykew.ipni as ipni
import FileOperate
import requests
from bs4 import BeautifulSoup
import re
"""
查询一个物种名在powo中的简单信息，并访问网页获取描述"""

def search_powo(sp_name):
    """
    搜索powo的物种信息
    :param sp_name: 物种名
    :return: 搜索到的内容
    """
    result = ipni.search(sp_name)
    try:
        for record in result:
            if record['name'] == sp_name:
                first_ipni_id = record['url'].strip("/n/")
                website = f'https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:{first_ipni_id}'
                info = visit_website(website)
                return info
            else:
                continue
    except:
        return "Fail"


def search_wcvp(sp_name, df):
    """
    搜索powo的物种信息
    :param df:
    :param wcvp_name_file:
    :param sp_name: 物种名
    :return: 搜索到的内容
    """
    ndf = df[(df['taxon_name'] == sp_name) & (df['taxon_status'] != 'Accepted')]
    # 注意替换列名
    if len(ndf) > 0:
        first_ipni_id = ndf.iloc[0]['powo_id']
        website = f'https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:{first_ipni_id}'
        info = visit_website(website)
        return info
    else:
        sdf = df[df['taxon_name'] == sp_name]
        if len(sdf) > 0:
            return sdf.iloc[0]['taxon_name']
        else:
            return 'Fail'


def visit_website(url):
    """查找网页并且获取植物志信息"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    }
    try:
        information = requests.get(url, timeout=15, headers=headers)
        description_web = BeautifulSoup(information.text, 'lxml')
        accepted_sp = description_web.find(class_="name-status p-strong")
        if "accepted" in accepted_sp.text:
            detail_tag = description_web.find(class_="details p")
            detail = detail_tag.text.strip()
            detail = detail.replace(".", ",")
            detail = detail.replace("The native range of this species is ", "")
            detail = detail.replace(". It is a ", ",")
            detail = detail.replace(" and grows primarily in the ", ",")
            detail = detail.replace(". It grows primarily in the ", ",")
            detail = detail.replace(". It is used to ", ",")
            # 获得网站开头的简短描述
            distribution_tag = description_web.find(id="distribution-listing")
            Native_tag = distribution_tag.find_all("p")[0]
            native = Native_tag.text
            native = re.sub('[\s\n]\n+\s+\n+\s+', "", native).strip()
            native = native.replace(", ", "/")
            # 获得原生地数据
            return detail, native
        else:
            return accepted_sp.text.strip("\r\n").strip(" ").replace("This name is a synonym of ", "")
    except:
        return ""


def main():
    name_file = '../sp.txt'
    wcvp_name_file = "../wcvp_names.csv"
    name_list = FileOperate.get_list(name_file)
    df = pandas.read_csv(wcvp_name_file, sep="|", low_memory=False)
    df['full_name'] = df['taxon_name'] + ' ' + df['taxon_authors']
    with open("../sp_2_info.txt", "a", encoding='utf-8') as info_file:
        for name in name_list:
            info = search_wcvp(name, df)
            print(f'{name}%{info}\n')
            info_file.write(f'{name}%{info}\n')


if __name__ == '__main__':
    main()
