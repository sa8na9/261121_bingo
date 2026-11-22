import os
import random

from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "local-development-only-change-this"
)


@app.route("/", methods=["GET", "POST"])
def index():
    min_val = session.get("min_val", 1)
    max_val = session.get("max_val", 75)
    drawn_num = session.get("drawn_num", [])
    current_num = session.get("current_num", None)

    animate = False

    if request.method == "POST":
        action = request.form.get("action")

        if action == "draw":

            # 前回の数字を履歴に確定
            pending_num = session.get("pending_num")

            if pending_num is not None:
                if pending_num not in drawn_num:
                    drawn_num.append(pending_num)

                session["drawn_num"] = drawn_num
                session.pop("pending_num", None)

            # 未抽選の数字を取得
            all_num = list(range(min_val, max_val + 1))

            remaining_num = [
                n for n in all_num
                if n not in drawn_num
            ]

            if remaining_num:
                current_num = random.choice(remaining_num)

                # 今回の数字は次の抽選まで履歴に追加しない
                session["pending_num"] = current_num
                session["current_num"] = current_num

                animate = True

            else:
                current_num = "終了"
                session["current_num"] = current_num

        elif action == "reset":
            session.clear()

            session["min_val"] = 1
            session["max_val"] = 75
            session["drawn_num"] = []
            session["current_num"] = None

            return redirect(url_for("index"))

    return render_template(
        "index.html",
        current_num=current_num,
        drawn_num=drawn_num,
        min_val=min_val,
        max_val=max_val,
        animate=animate
    )


if __name__ == "__main__":
    app.run(debug=False)