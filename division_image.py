# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2024-09-11 21:07:31
# @Last Modified by:   Your name
# @Last Modified time: 2024-09-11 22:59:05

from PIL import Image, ImageDraw, ImageFont


def generate_long_division_image(
    dividend, divisor, font_path="./Fonts/Roboto-Medium.ttf", font_size=30, spacing=10
):
    """生成长除法竖式图像

    Args:
        dividend: 被除数
        divisor: 除数
        font_path: 字体文件路径
        font_size: 字体大小
        spacing: 行间距

    Returns:
        PIL图像对象
    """

    quotient = dividend // divisor
    remainder = dividend % divisor

    # 将数字转换为字符串
    dividend_str = str(dividend)
    divisor_str = str(divisor)
    quotient_str = str(quotient)

    # 计算竖式各部分的长度
    dividend_len = len(dividend_str)
    divisor_len = len(divisor_str)
    quotient_len = len(quotient_str)

    # 计算图像尺寸
    width = max(dividend_len, divisor_len + quotient_len) * font_size + 40
    height = (5 + quotient_len * 2) * (font_size + spacing) + 40

    # 创建图像和绘图对象
    image = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(image)

    # 加载字体
    font = ImageFont.truetype(font_path, font_size)

    # 绘制被除数和除数
    draw.text((20 + divisor_len * font_size, 10), dividend_str, font=font, fill="black")
    draw.text((10, 10 + font_size / 2), divisor_str, font=font, fill="black")
    draw.line(
        [(20, font_size + 20), (20 + dividend_len * font_size, font_size + 20)],
        fill="black",
        width=2,
    )

    y = font_size + 30 + spacing
    remaining_dividend_str = dividend_str
    quotient_index = 0

    while remaining_dividend_str and quotient_index < len(quotient_str):
        partial_dividend_str = remaining_dividend_str[
            0 : min(divisor_len + 1, len(remaining_dividend_str))
        ]
        partial_dividend = int(partial_dividend_str)

        while partial_dividend < divisor and len(remaining_dividend_str) > len(
            partial_dividend_str
        ):
            partial_dividend_str += remaining_dividend_str[len(partial_dividend_str)]
            partial_dividend = int(partial_dividend_str)

        partial_quotient = partial_dividend // divisor
        product = partial_quotient * divisor

        draw.text(
            (20 + (len(partial_dividend_str) - 1) * font_size, y - font_size - spacing),
            str(quotient_str[quotient_index]),
            font=font,
            fill="black",
        )
        quotient_index += 1

        draw.text(
            (20, y),
            str(product).zfill(len(partial_dividend_str)),
            font=font,
            fill="black",
        )
        draw.line(
            [
                (20, y + font_size + 10),
                (20 + len(partial_dividend_str) * font_size, y + font_size + 10),
            ],
            fill="black",
            width=2,
        )

        if len(remaining_dividend_str) > len(partial_dividend_str):
            draw.text(
                (20 + len(partial_dividend_str) * font_size, y + font_size / 3),
                "↓",
                font=font,
                fill="black",
            )

        y += font_size + 2 * spacing

        remaining_dividend_str = (
            str(int(partial_dividend_str) - product)
            + remaining_dividend_str[len(partial_dividend_str) :]
        )
        if remaining_dividend_str.startswith("0") and len(remaining_dividend_str) > 1:
            remaining_dividend_str = remaining_dividend_str[1:]

        if remaining_dividend_str:
            draw.text((20, y), remaining_dividend_str, font=font, fill="black")

    return image


def main():
    # 示例用法
    dividend = 1234
    divisor = 5
    image = generate_long_division_image(dividend, divisor)
    image.save("long_division.png")


if __name__ == "__main__":
    main()
