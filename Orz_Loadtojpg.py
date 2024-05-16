# -*- coding: utf-8 -*-
# @Author: JogFeelingVI
# @Date:   2024-05-14 16:04:53
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-05-16 10:15:05

import pathlib, ast, re, datetime
from typing import Final, Callable
from PIL import Image, ImageDraw, ImageFont


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
    cyns_json.unlink()
    # 排序
    data.sort(key=lambda item: item[1])
    return data

def datatoPng(data:list):
    pngs = []
    with Image.open("./Fonts/bg.jpg").convert("RGBA") as base:
        # get a font
        fnt65 = ImageFont.truetype("./Fonts/Micro5-Regular.ttf", 65)
        fnt45 = ImageFont.truetype("./Fonts/Micro5-Regular.ttf", 65)
        # get a drawing context
        for i in range(0, data.__len__(), 20):
            xpoint = 30
            ypoint = 120
            count = 0
            t_number = Image.new("RGBA", base.size, (92, 92, 92, 36))
            d = ImageDraw.Draw(t_number)
            for item in data[i:i+20]:
                id, cyns, info = item
                # infos.append(f'{id:_>4}|{cyns}: {info} \n')
                cyns = f"{id:>4}|{cyns}"
                if count % 5 == 0 and count != 0:
                    # infos.append('\n')
                    d.text(
                        (xpoint, ypoint),
                        "-" * 30,
                        font=fnt45,
                        fill=(92, 92, 92, 234),
                    )
                    ypoint += 50
                # print(f"{count = }")
                d.text((xpoint, ypoint), cyns, font=fnt45, fill=(92, 92, 92, 198))
                d.text(
                    (xpoint + 160, ypoint),
                    info,
                    font=fnt65,
                    fill=(13, 13, 13, 234),
                )
                count += 1
                ypoint += 50
            now = datetime.datetime.now()
            dtime = now.strftime("%Y/%m/%d %H:%M:%S")
            d.text((xpoint + 290, ypoint), dtime, font=fnt45, fill=(92, 92, 92, 198)) 
            out = Image.alpha_composite(base, t_number)
            png = f'./jpmpng/{now.strftime("%H%M%S")}_{i:>04}.png'
            pngs.append(png)
            out.save(png)
    return pngs


def main():
    print("Hello, World!")
    # for i in range(26):
    #     if i % 5 == 0 and i != 0:
    #         print("-" * 8)
    #     print("*" * 16)
    data = loadtoData()
    pngs = datatoPng(data=data)
    for png in pngs:
        print(f'png {png=}')


if __name__ == "__main__":
    main()
