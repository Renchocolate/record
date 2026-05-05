from flask import Flask, request, render_template_string, send_file
from datetime import datetime
import os

app = Flask(__name__)

# 智能路径：如果云端挂载了 /data 目录就用云端的，否则用本地当前目录
DATA_DIR = '/data' if os.path.exists('/data') else '.'
LOG_FILE = os.path.join(DATA_DIR, 'my_diary.txt')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>时间胶囊</title>
    <style>
        body { font-family: -apple-system, sans-serif; background: #f4f7f6; padding: 20px; color: #333; }
        .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { margin-top: 0; color: #2c3e50; font-size: 1.2rem; }
        input, textarea { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
        .export-btn { background: #6c757d; margin-top: 10px; }
        .status { color: green; font-size: 14px; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>⏳ 记录此刻</h2>
        <form method="POST" action="/add">
            <input type="text" name="activity" placeholder="在干啥/准备干啥？" required>
            <input type="text" name="mood" placeholder="心情如何？" required>
            <textarea name="feeling" placeholder="有什么感受？" rows="4"></textarea>
            <button type="submit">存档</button>
        </form>
        <form action="/download">
            <button type="submit" class="export-btn">导出 TXT</button>
        </form>
        {% if msg %}<div class="status">{{ msg }}</div>{% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/add', methods=['POST'])
def add():
    activity = request.form.get('activity')
    mood = request.form.get('mood')
    feeling = request.form.get('feeling')
    
    time_str = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    log_entry = f"【{time_str}】准备开始【{activity}】，心情是【{mood}】，感受是【{feeling}】\n"
    
    # 写入文件
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)
        
    return render_template_string(HTML_TEMPLATE, msg="✅ 存档成功！去忙吧~")

@app.route('/download')
def download():
    if os.path.exists(LOG_FILE):
        return send_file(LOG_FILE, as_attachment=True)
    return "暂无记录", 404

if __name__ == '__main__':
    # 云端托管平台通常会通过环境变量指定 PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
