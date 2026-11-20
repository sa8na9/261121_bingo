
import os
import random

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# セッション署名用の秘密鍵
# Renderでは環境変数 SECRET_KEY を使用する
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "local-development-only-change-this"
)


@app.route('/', methods=['GET', 'POST'])
def index():

    min_val = session.get('min_val', 1)
    max_val = session.get('max_val', 75)
    drawn_num = session.get('drawn_num', [])
    current_num = session.get('current_num', None)

    # ボタンが押されたときの処理
    if request.method == 'POST':

        action = request.form.get('action')

        # 数字を出す処理
        if action == 'draw':

            all_num = list(range(min_val, max_val + 1))
            mada_num = [
                n for n in all_num
                if n not in drawn_num
            ]

            # 数字が残っている場合
            if mada_num:

                current_num = random.choice(mada_num)

                drawn_num.append(current_num)

                session['drawn_num'] = drawn_num
                session['current_num'] = current_num

            # すべて引き終わった場合
            else:

                current_num = "終了"
                session['current_num'] = current_num

        # リセット処理
        elif action == 'reset':

            session.clear()

            session['min_val'] = 1
            session['max_val'] = 75
            session['drawn_num'] = []
            session['current_num'] = None

            return redirect(url_for('index'))

    return render_template(
        'index.html',
        current_num=current_num,
        drawn_num=drawn_num,
        min_val=min_val,
        max_val=max_val
    )


if __name__ == '__main__':
    app.run(debug=False)
