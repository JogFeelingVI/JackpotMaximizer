# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-05-14 16:04:53
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-22 23:02:55

import pathlib, ast, re, datetime
from typing import Final, Callable
from PIL import Image, ImageDraw, ImageFont

def clear_jpmpng():
    jpmPng = pathlib.Path('./jpmpng/')
    if jpmPng.exists():
        find_png = jpmPng.glob('*.png')
        for fp in find_png:
            print(f'PNG {fp}')
            fp.unlink()
            
    else:
        print(f'The `{jpmPng.name}` directory does not exist and has been created.')
        jpmPng.mkdir()

def loadtoData():
    cyns_json = pathlib.Path("./cyns.log")
    search_id_cyn_r_b = re.compile(r"id\s+(\d+).*\{(.*)\}\s\*\s(.*)\s\+\s(.*)")
    data = []
    with cyns_json.open("r+") as f:
        for line in f:
            line = line.strip()  # 去除首尾空格
            if line:  # 检查是否为空行
                match_search = search_id_cyn_r_b.search(line)
                if match_search == None:
                    return data

                _id, cyns, _r, _b = match_search.groups()
                r = " ".join((f"{x:02}" for x in ast.literal_eval(_r)))
                b = " ".join((f"{x:02}" for x in ast.literal_eval(_b)))
                cyns = ast.literal_eval(f"{{{cyns}}}").get(4, -1)
                data.append((int(_id), cyns, f"{r} - {b}"))
    # cyns_json.unlink()
    # 排序
    data.sort(key=lambda item: item[1])
    return data


def datatoPng(data: list):
    pngs = []
    with Image.open("./Fonts/bg.jpg").convert("RGBA") as base:
        base_w, base_h = base.size
        print(f"Base SIZE {base_w} x {base_h}")
        fnt35 = ImageFont.truetype("./Fonts/Roboto-Medium.ttf", 15)
        # get a drawing context
        for i in range(0, data.__len__(), 20):
            xpoint = 25
            ypoint = 120
            count = 0
            fontsize = 65
            # get a font
            fnt65 = ImageFont.truetype("./Fonts/Roboto-Medium.ttf", fontsize)
            t_number = Image.new("RGBA", base.size, (92, 92, 92, 36))
            d = ImageDraw.Draw(t_number)
            for item in data[i : i + 20]:
                id, cyns, info = item
                test = f"{id}|{cyns} {info}"
                test_show_width = base_w - 25 * 2
                test_width = d.textlength(test, font=fnt65)
                if test_show_width < test_width:
                    fontsize -= (test_width - test_show_width) / test_width * fontsize
                else:
                    fontsize += (test_show_width - test_width) / test_width * fontsize
                fnt65 = ImageFont.truetype("./Fonts/Roboto-Medium.ttf", fontsize)

                print(f"set font size {fnt65.size}")

                # infos.append(f'{id:_>4}|{cyns}: {info} \n')
                cyns = f"{id}|{cyns}"
                if count % 5 == 0 and count != 0:
                    # infos.append('\n')
                    splen = (base_w - 25 * 2) / d.textlength("-", fnt35)
                    d.text(
                        (xpoint, ypoint),
                        "-" * int(splen),
                        font=fnt35,
                        fill=(92, 92, 92, 234),
                    )
                    ypoint += fnt35.size * 1.2
                # print(f"{count = }")
                d.text((xpoint, ypoint), cyns, font=fnt65, fill=(92, 92, 92, 198))
                cynsplis = d.textlength(f"{cyns} ", font=fnt65)
                d.text(
                    (xpoint + cynsplis, ypoint),
                    info,
                    font=fnt65,
                    fill=(13, 13, 13, 234),
                )
                count += 1
                ypoint += fnt65.size * 1.4
            now = datetime.datetime.now()
            dtime = now.strftime("%Y/%m/%d %H:%M:%S")
            dypoint = base_w - d.textlength(dtime, fnt35) - 25
            d.text((dypoint, ypoint), dtime, font=fnt35, fill=(92, 92, 92, 198))
            out = Image.alpha_composite(base, t_number)
            png = f'./jpmpng/{now.strftime("%H%M%S")}_{i:>04}.png'
            pngs.append(png)
            # out.save(png)
            out.show()
    return pngs


def datatoPngv3(data: list):
    clear_jpmpng()
    pngs = []
    print(f"{data.__len__() = }")
    # font name size
    fontname = "./Fonts/Roboto-Medium.ttf"
    fontsize = 65
    font_tips = ImageFont.truetype(fontname, 15)
    font_change = ImageFont.truetype(fontname, fontsize)
    # 起始坐标
    xpoint = 25
    ypoint = 120
    # 计数器
    count = 0
    page = 1
    with Image.open("./Fonts/bg.jpg").convert("RGBA") as base:
        base_w, base_h = base.size
        print(f"Base SIZE {base_w} x {base_h}")
        t_number = Image.new("RGBA", base.size, (92, 92, 92, 36))
        d = ImageDraw.Draw(t_number)
        for item in data:
            # print(f'{item}')
            id, cyns, info = item
            test = f"{id}|{cyns} {info}"
            test_show_width = base_w - 25 * 2
            test_width = d.textlength(test, font=font_change)
            if test_show_width < test_width:
                fontsize -= (test_width - test_show_width) / test_width * fontsize
            else:
                fontsize += (test_show_width - test_width) / test_width * fontsize
            font_change = ImageFont.truetype("./Fonts/Roboto-Medium.ttf", fontsize)
            print(f"Change font size to {fontsize}")
            # 修改条目字体以适应大小
            cyns = f"{id}|{cyns}"
            if count % 5 == 0 and count != 0:
                # infos.append('\n')
                splen = (base_w - 25 * 2) / d.textlength("-", font_tips)
                d.text(
                    (xpoint, ypoint),
                    "-" * int(splen),
                    font=font_tips,
                    fill=(164, 164, 164, 178),
                )
                ypoint += font_tips.size * 1.2
            # print(f"{count = }")
            d.text((xpoint, ypoint), cyns, font=font_change, fill=(150, 150, 150, 178))
            cynsplis = d.textlength(f"{cyns} ", font=font_change)
            #! 在这里改变行的字体颜色
            char_widths = [font_change.getlength(char) for char in info]
            xcw =0
            color = (34, 40, 58, 178)
            for i, char in enumerate(info):
                if char == '-':
                    color = (84, 102, 159, 178)
                d.text(
                    (xpoint + cynsplis + xcw, ypoint),
                    char,
                    font=font_change,
                    fill=color,
                )
                xcw += char_widths[i]
            count += 1
            ypoint += font_change.size * 1.4
            # 确认是否需要保存
            now = (
                f"{count:>04}{page:>02}"
                + " * "
                + datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            )
            # 获取索引以确定是否是最后一向
            index = data.index(item)
            abs_now = ypoint / base_h
            # if index > 15:
            #     print(f"{abs_now = } {ypoint = } {base_h}")
            if abs_now > 0.932 or index + 1 == data.__len__():

                dypoint = base_w - d.textlength(now, font_tips) - 25
                d.text((dypoint, ypoint), now, font=font_tips, fill=(92, 92, 92, 178))
                out = Image.alpha_composite(base, t_number)
                png = f'./jpmpng/{datetime.datetime.now().strftime("%H%M%S")}_{count:>02}P{page}.png'
                pngs.append(png)
                out.save(png)
                page += 1
                # out.show()
                xpoint = 25
                ypoint = 120
                count = 0
                t_number = Image.new("RGBA", base.size, (92, 92, 92, 36))
                d = ImageDraw.Draw(t_number)
    return pngs


def main():
    print("Hello, World!")
    # for i in range(26):
    #     if i % 5 == 0 and i != 0:
    #         print("-" * 8)
    #     print("*" * 16)
    data = loadtoData()
    pngs = datatoPngv3(data=data)
    for png in pngs:
        print(f"PNG {png}")


if __name__ == "__main__":
    main()
