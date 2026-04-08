import json

# 把你给的所有用户ID粘贴在这里
user_ids = """
376030853
71311020790
9959199

64671038107
964179503
95639927527
54001899661
98521751214

mong33
34343715149
nuanyangbao

B59583
ryx126

6773619
MAO313
1181542556
a6131230
964179503

qiqi215.
24350031891
Riuuk33
Songch1013
57189729901

88272320348

yujiaying2001
zhouchuxuan0606
ZOULIANGBU99
ZiQian0613520
ziwei040609
zj018168
Zhangbeibei19901
ZCL6565
YY20200202Y
yujiaying2001
ysc189918
YuanQing_1005
yuetuwudao
YeahNight0517
xzh0430
Xingxing1758
xioayi
xiaorui3698
xiaowulaoshiLWJ
Wuhuiqiong66
wyyyana
x.y.y.0116
wosuiwoxin65
wlx99777
W.KFeb7
uu1888888uu
tq1262346206
Starcandy
Sunwanwan
tang05090509
ting_bao521
tomtangxincheng
ting_bao521
tang05090509
t020923
t70houlaoayi
sweetheart_12
SUPERyang226
Sunwanwan
Starcandy
ss13146293442
SQXY151631
SonOfUA.Weiss
songyue1214
Smj030303
Simon981111
shixinxiaoke
shiloysh_
Shh2017S
sen66049
SanWa1015
S5521
Rrruui1204_
renwurenliu6
Qingtianwawa827
35497738389
"""

# 处理成列表
user_list = [uid.strip() for uid in user_ids.strip().splitlines() if uid.strip()]

# 生成目标格式
result = []
date = "20260329"

for idx, uid in enumerate(user_list, start=1):
    result.append({
        "id": f"{idx:08d}",    # 自动生成 00000001 格式
        "user_id": uid,
        "date_time": date
    })

# 输出格式化 JSON
output = json.dumps(result, ensure_ascii=False, indent=2)
print(output)

# 可选：保存到文件
with open("user_list.json", "w", encoding="utf-8") as f:
    f.write(output)

print("\n✅ 转换完成！已生成 user_list.json 文件")