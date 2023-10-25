import requests
from bs4 import BeautifulSoup
import re

# 存放重庆的市区拼写的列表
regions = ['jiangbei', 'yubei', 'nanan', 'banan', 'shapingba', 'jiulongpo', 'yuzhong', 'dadukou','jiangjing', 'changshou1', 'beibei']

# 自定义一个爬虫函数
def findInfo(url):
    with open(r'HouseData.csv', 'a', encoding='utf-8') as f:  # 打开一个csv文件将爬取的数据存放到文件中
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                     '(KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'
        headers = {'User-Agent': user_agent}
        resp = requests.get(url, headers=headers)

        html = resp.text
        # print(resp.text)  # 打印网页代码内容

        # 对网页进行解析
        soup = BeautifulSoup(html, 'html.parser')
        #  print(soup)

        # 将找到的li标签（一套房子的信息）内容存放到列表中
        infos = soup.find('ul', {'class': "sellListContent"}).find_all('li')
        # print(infos)

        for info in infos:
            # 一层一层的找到每条信息对应的标签
            title = info.find('div', {'class': "title"}).find('a').get_text()
            # print(title)

            # 房屋的总价
            price = info.find('div', {'class': "priceInfo"}).find('div', {'class': "totalPrice"}).find(
                'span').get_text()
            # print(price)

            # 爬取房屋地段信息，并去除房屋地段信息中的空格符
            address = info.find('div', {'class': 'positionInfo'}).get_text().replace(' ', '')
            # print(address)

            # 其他房屋基本信息
            otherInfo = info.find('div', {'class': 'address'}).find('div', {'class': 'houseInfo'}).get_text()
            # print(otherInfo)

            # 使用正则表达式把爬到的一整串信息分割成多条
            List = re.split(r' | ', otherInfo)
            houseType = List[0]  # 户型
            # print(houseType)
            houseArea = List[2]  # 面积
            # print(houseArea)
            houseOrientation = List[4]  # 房屋朝向
            # print(houseOrientation)
            Renovation = List[6]  # 房屋装修
            houseFloor = List[8]  # 房屋楼层
            BuildingYear = List[10]  # 建房年份
            ArchitecturalType = List[12]  # 建筑类型

            # 爬取房屋的单价信息
            danjia = info.find('div', {'class': 'unitPrice'}).find('span').get_text()  # 单价信息

            danjia = danjia[2:]  # 去除爬到的数据中前面的”单价“两个字
            # print(danjia)

            # 把爬到的信息依次写入文件中
            f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(title, price, address, danjia, houseType, houseArea,houseOrientation  Renovation, houseFloor, BuildingYear,ArchitecturalTyp))

if __name__ == '__main__':
    print("现在开始爬取重庆市二手房信息，请耐心等候！")
    for region in regions:
        for i in range(1, 100):  # 每个区爬取100页信息
            url = 'https://cq.lianjia.com/ershoufang/' + region + '/pg' +str(i) + '/'  # 拼接URL地址
            findInfo(url)
            # 每爬取一个区一个网页的信息就输出一句提示
            print('{} has been writen.'.format(region))
    print("爬取结束！")