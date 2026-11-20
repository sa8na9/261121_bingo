import random
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = 'bingo_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    min_val = session.get('min_val', 1)         # ビンゴカードの最小値
    max_val = session.get('max_val', 75)        # ビンゴカードの最大値
    drawn_num = session.get('drawn_num', [])    # 出た数値の履歴
    current_num = session.get('current_num', None)  # 今引いた数値

    # ボタンが押されたときの処理
    if request.method == 'POST':
        # どのボタンが押されたか判定
        action = request.form.get('action')

        # 数字を出す処理（重複防止）
        if action == 'draw':
            all_num = list(range(min_val, max_val + 1))
            mada_num = [n for n in all_num if n not in drawn_num]

            # 数字が残ってる限り回せる
            if mada_num:
                # まだ出てない数字から
                current_num = random.choice(mada_num)
                # 引いた数字を履歴に追加
                drawn_num.append(current_num)
                session['drawn_num'] = drawn_num
                session['current_num'] = current_num

            else:
                current_num = "終了"

        # リセットボタンが押されたときの処理
        elif action == 'reset':
            session['min_val'] = int(request.form.get('min_val', 1))
            session['max_val'] = int(request.form.get('max_val', 80))
            session['drawn_num'] = []
            session['current_num'] = None
            return redirect('/')

    return render_template('index.html', 
                                current_num=current_num,
                                drawn_num=drawn_num,
                                min_val=min_val,
                                max_val=max_val)


if __name__ == '__main__':
    app.run(debug=True)