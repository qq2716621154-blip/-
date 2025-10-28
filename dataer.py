import os
import time
import requests
import urllib3
urllib3.disable_warnings()
# 进度条库
from tqdm import tqdm
import os
from PIL import Image  # 需要安装 pillow 库
import imagehash       # 需要安装 imagehash 库
import hashlib         # 这个是Python标准库，不需要额外安装

cookies = {
'BDqhfp': '%E7%8B%97%E7%8B%97%26%26NaN-1undefined%26%2618880%26%2621',
'BIDUPSID': '06338E0BE23C6ADB52165ACEB972355B',
'PSTM': '1646905430',
'BAIDUID': '104BD58A7C408DABABCAC9E0A1B184B4:FG=1',
'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
'H_PS_PSSID': '35836_35105_31254_36024_36005_34584_36142_36120_36032_35993_35984_35319_26350_35723_22160_36061',
'BDSFRCVID': '8--OJexroG0xMovDbuOS5T78igKKHJQTDYLtOwXPsp3LGJLVgaSTEG0PtjcEHMA-2ZlgogKK02OTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
'H_BDCLCKID_SF': 'tJPqoKtbtDI3fP36qR3KhPt8Kpby2D62aKDs2nopBhcqEIL4QTQM5p5yQ2c7LUvtynT2KJnz3Po8MUbSj4QoDjFjXJ7RJRJbK6vwKJ5s5h5nhMJSb67JDMP0-4F8exry523ioIovQpn0MhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0D6bBjHujtT_s2TTKLPK8fCnBDP59MDTjhPrMypomWMT-0bFH_-5L-l5js56SbU5hW5LSQxQ3QhLDQNn7_JjOX-0bVIj6Wl_-etP3yarQhxQxtNRdXInjtpvhHR38MpbobUPUDa59LUvEJgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj0DKLtD8bMC-RDjt35n-Wqxobbtof-KOhLTrJaDkWsx7Oy4oTj6DD5lrG0P6RHmb8ht59JROPSU7mhqb_3MvB-fnEbf7r-2TP_R6GBPQtqMbIQft20-DIeMtjBMJaJRCqWR7jWhk2hl72ybCMQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCet5DJJn4j_Dv5b-0aKRcY-tT5M-Lf5eT22-usy6Qd2hcH0KLKDh6gb4PhQKuZ5qutLTb4QTbqWKJcKfb1MRjvMPnF-tKZDb-JXtr92nuDal5TtUthSDnTDMRhXfIL04nyKMnitnr9-pnLJpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuj6tWj6j0DNRabK6aKC5bL6rJabC3b5CzXU6q2bDeQN3OW4Rq3Irt2M8aQI0WjJ3oyU7k0q0vWtvJWbbvLT7johRTWqR4enjb3MonDh83Mxb4BUrCHRrzWn3O5hvvhKoO3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRCqVIKa3f',
'BDSFRCVID_BFESS': '8--OJexroG0xMovDbuOS5T78igKKHJQTDYLtOwXPsp3LGJLVgaSTEG0PtjcEHMA-2ZlgogKK02OTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5',
'H_BDCLCKID_SF_BFESS': 'tJPqoKtbtDI3fP36qR3KhPt8Kpby2D62aKDs2nopBhcqEIL4QTQM5p5yQ2c7LUvtynT2KJnz3Po8MUbSj4QoDjFjXJ7RJRJbK6vwKJ5s5h5nhMJSb67JDMP0-4F8exry523ioIovQpn0MhQ3DRoWXPIqbN7P-p5Z5mAqKl0MLPbtbb0xXj_0D6bBjHujtT_s2TTKLPK8fCnBDP59MDTjhPrMypomWMT-0bFH_-5L-l5js56SbU5hW5LSQxQ3QhLDQNn7_JjOX-0bVIj6Wl_-etP3yarQhxQxtNRdXInjtpvhHR38MpbobUPUDa59LUvEJgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj0DKLtD8bMC-RDjt35n-Wqxobbtof-KOhLTrJaDkWsx7Oy4oTj6DD5lrG0P6RHmb8ht59JROPSU7mhqb_3MvB-fnEbf7r-2TP_R6GBPQtqMbIQft20-DIeMtjBMJaJRCqWR7jWhk2hl72ybCMQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCet5DJJn4j_Dv5b-0aKRcY-tT5M-Lf5eT22-usy6Qd2hcH0KLKDh6gb4PhQKuZ5qutLTb4QTbqWKJcKfb1MRjvMPnF-tKZDb-JXtr92nuDal5TtUthSDnTDMRhXfIL04nyKMnitnr9-pnLJpQrh459XP68bTkA5bjZKxtq3mkjbPbDfn02eCKuj6tWj6j0DNRabK6aKC5bL6rJabC3b5CzXU6q2bDeQN3OW4Rq3Irt2M8aQI0WjJ3oyU7k0q0vWtvJWbbvLT7johRTWqR4enjb3MonDh83Mxb4BUrCHRrzWn3O5hvvhKoO3MA-yUKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQXH_E5bj2qRCqVIKa3f',
'indexPageSugList': '%5B%22%E7%8B%97%E7%8B%97%22%5D',
'cleanHistoryStatus': '0',
'BAIDUID_BFESS': '104BD58A7C408DABABCAC9E0A1B184B4:FG=1',
'BDRCVFR[dG2JNJb_ajR]': 'mk3SLVN4HKm',
'BDRCVFR[-pGxjrCMryR]': 'mk3SLVN4HKm',
'ab_sr': '1.0.1_Y2YxZDkwMWZkMmY2MzA4MGU0OTNhMzVlNTcwMmM2MWE4YWU4OTc1ZjZmZDM2N2RjYmVkMzFiY2NjNWM4Nzk4NzBlZTliYWU0ZTAyODkzNDA3YzNiMTVjMTllMzQ0MGJlZjAwYzk5MDdjNWM0MzJmMDdhOWNhYTZhMjIwODc5MDMxN2QyMmE1YTFmN2QyY2M1M2VmZDkzMjMyOThiYmNhZA==',
'delPer': '0',
'PSINO': '2',
'BA_HECTOR': '8h24a024042g05alup1h3g0aq0q',
}

headers = {
'Connection': 'keep-alive',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
'Accept': 'text/plain, */*; q=0.01',
'X-Requested-With': 'XMLHttpRequest',
'sec-ch-ua-mobile': '?0',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
'sec-ch-ua-platform': '"macOS"',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Dest': 'empty',
'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1647837998851_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDIsNiwxLDUsNCw4LDcsOQ%3D%3D&ie=utf-8&sid=&word=%E7%8B%97%E7%8B%97',
'Accept-Language': 'zh-CN,zh;q=0.9',
}

def craw_single_class(keyword, DOWNLOAD_NUM=200):
    if os.path.exists('dataset/' + keyword):
        print('文件夹 dataset/{} 已存在，之后直接将爬取到的图片保存至该文件夹中'.format(keyword))
    else:
        os.makedirs('dataset/{}'.format(keyword))
        print('新建文件夹：dataset/{}'.format(keyword))
    count = 1

    with tqdm(total=DOWNLOAD_NUM, position=0, leave=True) as pbar:

        # 爬取第几张
        num = 0

        # 是否继续爬取
        FLAG = True

        while FLAG:

            page = 30 * count

            params = (
                ('tn', 'resultjson_com'),
                ('logid', '12508239107856075440'),
                ('ipn', 'rj'),
                ('ct', '201326592'),
                ('is', ''),
                ('fp', 'result'),
                ('fr', ''),
                ('word', f'{keyword}'),
                ('queryWord', f'{keyword}'),
                ('cl', '2'),
                ('lm', '-1'),
                ('ie', 'utf-8'),
                ('oe', 'utf-8'),
                ('adpicid', ''),
                ('st', '-1'),
                ('z', ''),
                ('ic', ''),
                ('hd', ''),
                ('latest', ''),
                ('copyright', ''),
                ('s', ''),
                ('se', ''),
                ('tab', ''),
                ('width', ''),
                ('height', ''),
                ('face', '0'),
                ('istype', '2'),
                ('qc', ''),
                ('nc', '1'),
                ('expermode', ''),
                ('nojc', ''),
                ('isAsync', ''),
                ('pn', f'{page}'),
                ('rn', '30'),
                ('gsm', '1e'),
                ('1647838001666', ''),
            )

            response = requests.get('https://image.baidu.com/search/acjson', headers=headers, params=params,
                                    cookies=cookies)
            if response.status_code == 200:
                try:
                    json_data = response.json().get("data")

                    if json_data:
                        for x in json_data:
                            type = x.get("type")
                            if type not in ["gif"]:
                                img = x.get("thumbURL")
                                fromPageTitleEnc = x.get("fromPageTitleEnc")
                                try:
                                    resp = requests.get(url=img, verify=False)
                                    time.sleep(1)

                                    # 保存文件名
                                    file_save_path = f'dataset/{keyword}/{num}.{type}'
                                    with open(file_save_path, 'wb') as f:
                                        f.write(resp.content)
                                        f.flush()
                                        # print('第 {} 张图像 {} 爬取完成'.format(num, fromPageTitleEnc))
                                        num += 1
                                        pbar.update(1)  # 进度条更新

                                    # 爬取数量达到要求
                                    if num > DOWNLOAD_NUM:
                                        FLAG = False
                                        print('{} 张图像爬取完毕'.format(num))
                                        break

                                except Exception:
                                    pass
                except:
                    pass
            else:
                break

            count += 1

class_list = [
    "白黄侧耳",
    "裂皮侧耳",
    "玫耳",
    "硫磺菌",
    "鸡冠菌",
    "牛舌菌",
    "卷缘齿菌",
    "狮黄齿菌",
    "珊瑚菌",
    "杯冠珊瑚菌",
    "紫丁香蘑",
    "肉色香蘑",
    "灰紫香蘑",
    "白桩菇",
    "疝疼乳菇",
    "松乳菇",
    "红汁乳菇",
    "多汁乳菇",
    "辣乳菇",
    "绒白乳菇",
    "环纹苦乳菇",
    "黑乳菇",
    "绒盖乳菇",
    "皱盖罗鳞伞",
    "黄伞",
    "毛头鬼伞",
    "家园鬼伞",
    "瓦鳞鬼伞",
    "粪鬼伞",
    "晶粒鬼伞",
    "疣孢黄枝瑚菌",
    "红顶枝瑚菌",
    "葡萄色顶枝瑚菌",
    "秃马勃",
    "网纹马勃",
    "梨形马勃",
    "中国静灰球",
    "白秃马勃",
    "大秃马勃",
    "紫色秃马勃",
    "豆包菌",
    "黄裙竹荪",
    "红托竹荪",
    "短裙竹荪",
    "长裙竹荪",
    "棘托竹荪",
    "橘色网孢盘菌",
    "鹿花菌",
    "赭鹿花菌",
    "钟菌",
    "波缘盘菌"
]


def check_image_integrity(image_path):
    """检查图像完整性"""
    try:
        with Image.open(image_path) as img:
            img.verify()  # 验证图像完整性
        return True
    except Exception as e:
        print(f"图像损坏: {image_path}, 错误: {e}")
        return False


def calculate_image_hash(image_path):
    """计算图像哈希值用于去重"""
    try:
        with Image.open(image_path) as img:
            # 使用感知哈希，对缩放和格式变化不敏感
            return imagehash.phash(img)
    except Exception as e:
        print(f"计算哈希失败: {image_path}, 错误: {e}")
        return None


def remove_duplicate_images(folder_path):
    """去除重复图像"""
    hash_dict = {}
    duplicates = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(folder_path, filename)
            img_hash = calculate_image_hash(file_path)

            if img_hash is not None:
                # 查找相似图像（允许一定误差）
                is_duplicate = False
                for existing_hash in hash_dict:
                    if img_hash - existing_hash <= 5:  # 相似度阈值
                        duplicates.append(file_path)
                        is_duplicate = True
                        break

                if not is_duplicate:
                    hash_dict[img_hash] = file_path

    # 删除重复文件
    for duplicate in duplicates:
        os.remove(duplicate)
        print(f"删除重复图像: {duplicate}")

    return len(duplicates)


def filter_small_images(folder_path, min_size=(100, 100)):
    """过滤尺寸过小的图像"""
    removed_count = 0
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width < min_size[0] or height < min_size[1]:
                        os.remove(file_path)
                        removed_count += 1
                        print(f"删除小尺寸图像: {filename} ({width}x{height})")
            except Exception as e:
                print(f"检查图像尺寸失败: {filename}, 错误: {e}")

    return removed_count


def data_cleaning(keyword):
    """数据清洗主函数"""
    folder_path = f'dataset/{keyword}'

    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在")
        return

    print(f"\n开始清洗 {keyword} 类别的图像数据...")

    # 1. 检查图像完整性
    print("1. 检查图像完整性...")
    valid_count = 0
    total_count = 0

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            total_count += 1
            file_path = os.path.join(folder_path, filename)
            if check_image_integrity(file_path):
                valid_count += 1
            else:
                os.remove(file_path)

    print(f"完整性检查完成: {valid_count}/{total_count} 张图像有效")

    # 2. 去除重复数据
    print("2. 去除重复图像...")
    duplicate_count = remove_duplicate_images(folder_path)
    print(f"去重完成: 删除了 {duplicate_count} 张重复图像")

    # 3. 数据筛选（过滤小尺寸图像）
    print("3. 过滤小尺寸图像...")
    small_count = filter_small_images(folder_path, min_size=(100, 100))
    print(f"尺寸过滤完成: 删除了 {small_count} 张小尺寸图像")

    # 最终统计
    final_count = len([f for f in os.listdir(folder_path)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))])
    print(f"数据清洗完成: {keyword} 类别最终剩余 {final_count} 张图像")



def clean_all_datasets():
    """清洗所有类别的数据"""
    for each in class_list:
        data_cleaning(each)
for each in class_list:
    craw_single_class(each, DOWNLOAD_NUM = 200)
clean_all_datasets()