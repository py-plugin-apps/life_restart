# coding=utf-8
from os.path import join
from .Life import Life
from .PicClass import *
import traceback
import random
from core import Handler, Request, Response

package = "life_restart"


def genp(prop):
    ps = []
    tmp = prop
    while True:
        for i in range(0, 4):
            if i == 3:
                ps.append(tmp)
            else:
                if tmp >= 10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, tmp))
                tmp -= ps[-1]
        if ps[3] < 10:
            break
        else:
            tmp = prop
            ps.clear()
    return {"CHR": ps[0], "INT": ps[1], "STR": ps[2], "MNY": ps[3]}


@Handler.FrameToStream
async def restart(request: Request):
    Life.load(join(FILE_PATH, "data"))

    while True:
        life = Life()
        life.setErrorHandler(lambda e: traceback.print_exc())
        life.setTalentHandler(lambda ts: random.choice(ts).id)
        life.setPropertyhandler(genp)
        flag = life.choose()
        if flag:
            break

    name = request.event.sender.name
    choice = 0
    person = name + "本次重生的基本信息如下：\n\n【你的天赋】\n"
    for t in life.talent.talents:
        choice = choice + 1
        person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"

    person = person + "\n【基础属性】\n"
    person = person + "   美貌值:" + str(life.property.CHR) + "  "
    person = person + "智力值:" + str(life.property.INT) + "  "
    person = person + "体质值:" + str(life.property.STR) + "  "
    person = person + "财富值:" + str(life.property.MNY) + "  "

    yield Response(
        message=f"你的命运正在重启....，这是{name}本次轮回的基础属性和天赋:",
        image=ImgText(person).draw_text(),
        messageDict={"at": request.event.sender.qq}
    )

    res = life.run()  # 命运之轮开始转动
    mes = "\n".join("\n".join(x) for x in res)

    yield Response(
        message=f"这是{name}本次轮回的生平:",
        image=ImgText(mes).draw_text(),
        messageDict={"at": request.event.sender.qq}
    )

    sums = life.property.gensummary()  # 你的命运之轮到头了

    yield Response(
        message=f"这是{name}本次轮回的评价:",
        image=ImgText(sums).draw_text(),
        messageDict={"at": request.event.sender.qq}
    )
