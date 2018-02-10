from wxpy import *
from wxpy import get_wechat_logger

bot = Bot(cache_path = True,console_qr = True,qr_path="/home/ubuntu/wechatRobot/QR.png")
welcome = '''哈哈，我是虾米的机器人，小小虾米emmmmmmm
我有以下功能，回复序号即可查询
0.联系主人
1.查询英语外研社答案
2.让小小虾米邀请你进入外研社交流群
3.让小小虾米邀请你进入海大互帮互助群(五福群)
银联送红包，最少8.8，点http://dwz.cn/7pq003了解详情
'''
def invite(id,user):
    options = {1:"外研社",2:"互帮互助群"}
    name = options[id]
    group =  bot.groups().search(name)
    if(len(group)):
        print(len(user))
        try:
            group[0].add_members(user,use_invitation=True)
            logger = get_wechat_logger()
            logger.error(name)
        except Exception as e:
            logger = get_wechat_logger()
            logger.warning(str(e))
    else:
        user.send("哇！小小虾米没找到你想进的群")

@bot.register(msg_types = TEXT)
def reply_my_friend(msg):
    if("添加" in msg.text):#添加为好友
        return welcome
    elif("答案" in msg.text or  '1' in msg.text):
        return "答案开学更新哦"
    elif("外研社" in msg.text or "2" in msg.text):
        group = bot.groups().search("外研社")
        group[0].add_members(msg.sender, use_invitation=True)
    elif("互帮互助" in msg.text or "五福" in msg.text or "3" in msg.text):
        group = bot.groups().search("互帮互助")
        group[0].add_members(msg.sender, use_invitation=True)
    elif("主人" in msg.text or "0" in msg.text):
        return "主人现在不在，看到了就会回复你的哦！"
    else:
        return welcome

@bot.register(Group, TEXT)
def auto_reply(msg):
    # 如果是群聊，但没有被 @，则不回复
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:
        # 回复消息内容和类型
        return '收到 @{} 的消息: {} '.format(msg.member.name, msg.text)

@bot.register(msg_types = FRIENDS)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    # 接受好友 (msg.card 为该请求的用户对象)
    new_friend = bot.accept_friend(msg.card)
    # 或 new_friend = msg.card.accept()
    # 向新的好友发送消息
    new_friend.send(welcome)

bot.join()