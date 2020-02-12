from bs4 import BeautifulSoup
import re
import os

def search_for_scan(page, patch,files):
    pages=set()
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    with open("{}{}".format(patch, page),"r",encoding='utf-8') as data:
        str=data.read()
    links=link_re.findall(str)
    for link in links:
        if link in files:
            pages.add(link)

    return pages

# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    scan_page=set() # страницы для сканирования
    scan_page.add(start)
    used_page=set() # отсканированные страницы
    next_page=set() # страницы для следующего сканирования
    not_find=True
    while not_find:
        for page in scan_page:
            find_page=search_for_scan(page, path,files)
            if end in find_page:
                files[end]=page
                not_find=False
                break
            next_page.update(find_page)
            used_page.add(page)
            for p in find_page:
                if not files[p]:
                    files[p]=page
        scan_page=next_page.difference(used_page)

    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    files = build_tree(start, end, path)
    bridge = []
    current=end
    while current!=start:
        bridge.append(current)
        current=files[current]
    bridge.append(start)
    return bridge


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  #
    # bridge=[]
    bridge.append(start)
    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open("{}{}".format(path, file),encoding='utf-8') as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        imgs = len(body.find_all('img',width=re.compile(r'[2-9]\d\d')))

        headers = 0
        head_sym=re.compile(r'[ETC]')
        for h in body.find_all(name=re.compile(r'h[1-6]')):
            if head_sym.search(h.text):
                headers +=1
        linkslen = 0  # Длина максимальной последовательности ссылок, между которыми нет других тегов

        for link in body.find_all("a"):
            max_link=1
            next_tag=link.nextSibling
            while not next_tag is None:
                if next_tag.name=='a':
                    next_tag=next_tag.nextSibling
                    max_link +=1
                elif next_tag.name is None:
                    next_tag=next_tag.nextSibling
                    continue
                else:
                    break
            if max_link>linkslen:
                linkslen=max_link

        lists = 0  # Количество списков, не вложенных в другие списки

        for list in body.find_all(["ul","ol"]):
            no_parents=False
            for parent in list.parents:
                no_parents = no_parents or parent.name=='ol' or parent.name =="ul"
            if not no_parents:
                lists +=1
            pass
        out[file] = [imgs, headers, linkslen, lists]

    return out
