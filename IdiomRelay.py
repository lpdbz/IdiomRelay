#!/usr/bin/env python
# encoding:utf-8
import os
import pypinyin
from pypinyin import lazy_pinyin
import random
import pandas as pd

data = []


def get_pinyin(word):
    """
    可以将一个汉字字符串转换为音调的拼音列表
    """
    pinyin = []
    for i in word:
        pinyin.append(pypinyin.pinyin(i, style=pypinyin.TONE))  # 使用pypinyin库的pinyin函数，指定风格为带音调的风格
    return pinyin


def get_all_starts_with(letter):
    """
    根据一个汉字的拼音，从数据中找出所以以该拼音开头的成语，并返回一个列表
    """
    result = []
    target_pinyin = lazy_pinyin(letter)
    target_pinyin_first = target_pinyin[-1]  # 成功获取目标字的最后一个字的拼音
    for i in data:
        data_word = i[0]
        data_pinyin = i[1]
        data_meaning = i[2]
        data_pinyin_first = data_pinyin[0]  # 获取数据中的成语的第一个字的拼音
        if data_pinyin_first == target_pinyin_first:  # 比较拼音是否相同
            result.append([data_word, data_meaning])
    return result


def get_random_result(data):
    """
    从一个列表中随机选择一个元素，并返回它
    :param data: 表示要选择的列表
    """
    return random.choice(data)


def format_data(data):
    """
    将一个抱哈成语和解释的列表，转换为一个格式化的字符串
    """
    return "[%s] : [%s]" % (data[0], data[1])


def init():
    """
    可以从一个文件中读取成语、拼音和解释的数据，并存储到data列表中，并打印出读取的数量
    """
    # 使用with语句和open函数，以只读模式打开"data.txt"文件，并指定编码为'utf-8'，将文件对象赋值给f
    with open("data.txt", "r", encoding='utf-8') as f:
        counter = 0  # 记录读取的数量
        for line in f:
            content = line.split("\t")
            word = content[0]  # 获取content列表中的第一个元素content[0]，赋值给word，它是一个成语
            pinyin = content[1].split(
                "'")  # 获取content列表中的第二个元素content[1]，使用split方法，以单引号"'"为分隔符，将它分割为一个列表pinyin，它是一个拼音列表
            meaning = content[2].replace("\n",
                                         "")  # 获取content列表中的第三个元素content[2]，使用replace方法，将换行符"\n"替换为空字符串""，赋值给meaning，它是一个解释
            data.append([word, pinyin, meaning])
            counter += 1  # 将counter的值加1，表示读取了一个成语
        print("[+] Init finished! [%d] words." % (counter))


def is_chinese(word):
    # 判断一个字符串是否全是汉字
    for i in word:
        if not '\u4e00' <= i <= '\u9fa5':
            return False
    return True


def guess(word):
    all_data_matched = get_all_starts_with(word)
    if all_data_matched:  # 如果列表不为空
        result_data = format_data(get_random_result(all_data_matched))
        return result_data
    else:  # 如果列表为空
        return "没有找到以%s开头的成语，请换一个成语试试。" % word[-1]


def userMenu():
    print("#################欢迎来到成语接龙游戏##############")
    print("#               请输入您想要娱乐的功能             #")
    print("#               [1] 龙腾虎跃--开始游戏            #")  # 开始成语接龙游戏，每次输入一个与上一个成语接龙的四字成语
    print("#               [2] 龙马精神--查看成绩            #")  # 查看自己的成语接龙成绩
    print("#               [3] 龙争虎斗--查看获得的奖项       #")  # 参加成语接龙比赛，赢取荣誉
    print("#               [4] 龙潜凤采--查看所有成语         #")  # 学习成语的意思和出处，提高文化素养
    print("#               [5] 龙凤呈祥--祝福               #")  # 浏览龙年的吉祥语和祝福语
    print("#               [0] 龙驭上宾--退出游戏            #")  # 退出系统，感谢使用
    print("################龙行龘龘，成语接龙################\n")


def main():
    score = 0
    flag = 1
    init()
    while flag:
        userMenu()
        choice = input("请输入您的选择：")
        if choice == "1":
            word = input("请输入一个成语：")
            if word == "exit":
                print("欢迎下次再来玩成语接龙")
                break
            while word != "exit":
                word = word.strip()  # 去掉空格
                word = word.encode('utf-8').decode('utf-8')  # 转换为统一的编码
                if not is_chinese(word):  # 检查是否为汉字
                    print("请输入汉字。")
                    word = input("请输入一个成语：")
                    continue
                if word not in [i[0] for i in data]:  # 检查是否存在于数据中
                    print("没有这个成语，请重新输入。")
                    word = input("请输入一个成语：")
                    continue
                if len(word) != 4:  # 检查是否是四字成语
                    print("请输入四字成语。")
                    word = input("请输入一个成语：")
                    continue
                score += 1
                print("是一个正确的成语呢，您真棒，分数加一")
                result = guess(word)
                print(result)
                print("*****请继续操作*****")
                print("1. 继续玩")
                print("2. 不玩了")
                choice1 = input("请输入您的选择：")
                if choice1 == '1':
                    word = input("请输入一个成语：")
                else:
                    print("下次再来哦")
                    break
        elif choice == "2":
            # 查看自己的成语接龙成绩
            print("您的成语接龙成绩是：%d分。" % score)
            os.system("pause")
        elif choice == '3':
            if score < 3:
                print("恭喜获得“望子成龙”--参与奖")
            elif score < 5:
                print("恭喜获得“龙腾虎跃”--优秀奖")
            elif score < 8:
                print("恭喜获得“龙马精神”--三等奖")
            elif score < 10:
                print("恭喜获得“龙争虎斗”--二等奖")
            elif score > 10:
                print("恭喜获得“龙飞凤舞”--一等奖")
            os.system("pause")
        elif choice == '4':
            df = pd.DataFrame(data, columns=['成语', '拼音', '解释'])  # 创建一个DataFrame对象，指定列名
            # 分页显示 DataFrame
            rows_per_page = 50
            page = 1
            while True:
                # 计算要显示的行数
                start = (page - 1) * rows_per_page
                end = start + rows_per_page

                # 将 DataFrame 转换为字符串并输出
                print(df.iloc[start:end].to_string(index=False))

                # 询问用户是否继续查看下一页
                choice = input('查看下一页？(y/n) ')

                # 如果用户选择退出，则结束循环
                if choice.lower() == 'n':
                    break

                # 否则，显示下一页
                page += 1
            os.system("pause")
        elif choice == '5':
            print("祝您龙年吉祥，祥龙献瑞，瑞气盈门，门庭若市，市井传声，声名远扬，扬眉吐气，气宇轩昂，昂首阔步，步步高升，升官发财，财源广进，进退有度！")
            os.system("pause")
        elif choice == '0':
            print("欢迎下次来玩")
            flag = 0
        else:
            print("输入错啦，请重新输入")
            os.system("pause")
            continue


if __name__ == "__main__":
    main()
