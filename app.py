import re
import json
import random
from flask import Flask, request, jsonify, render_template, send_from_directory

with open('./resources/responses.json', 'r', encoding='utf-8') as f:
    responses = json.load(f)

app = Flask(__name__)


def roll_dice(num, sides):
    # 创建一个列表来存储每次掷骰的点数
    rolls = []
    for i in range(int(num)):
        # 在 1 和骰子面数之间选择一个随机整数
        roll = random.randint(1, int(sides))
        # 将随机整数添加到列表中
        rolls.append(roll)

    # 计算所有点数的总和
    total = sum(rolls)

    # 根据格式返回结果字符串
    return f'掷骰{num}d{sides}={"+".join(str(x) for x in rolls)}={total}'


def process(text):
    # 如果用户输入中包含 my_dict 中的某个键，则返回对应的值
    for key, value in responses.items():
        if key in text:
            return value

    # 如果用户输入不包含任何键，则返回默认回复
    return '抱歉，我不明白您的意思'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('./static', path)


@app.route('/chat', methods=['POST'])
def reply():
    data = request.get_json()

    # 获取请求中的输入语句
    message = data['message']

    # 在 responses 变量中查找匹配该输入语句的回复
    reply = None
    for pattern, definition in responses.items():
        match = re.match(pattern, message)
        if match:
            if definition['type'] == 'text':
                reply = definition['data']
            elif definition['type'] == 'call':
                function_name = definition['call']
                # 使用命名组从 Match 对象中获取参数值，并将其传递给函数
                calling_args = match.groupdict()
                reply = globals()[function_name](**calling_args)
            break

    # 如果没有找到匹配的回复，则返回 process 函数的返回值
    if not reply:
        reply = process(message)

    # 将回复转换为 JSON 格式并返回响应
    response = {'message': reply}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=Tr)