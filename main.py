from datetime import datetime
from typing import List

import flask

import conversion
import score

app = flask.Flask(__name__)


def calc_score(result: List[List]) -> int:
    return sum([1 for row in result if row[3]])


@app.route("/bin-dec-quiz")
def home():
    binqn = {}
    i = 1
    while len(binqn) < 5:
        if (value := conversion.randbin()) not in binqn:
            binqn[f"b{i}"] = value
            i += 1
    decqn = {}
    i = 1
    while len(decqn) < 5:
        if (value := conversion.randdec()) not in decqn:
            decqn[f"d{i}"] = value
            i += 1
    return flask.render_template("bindecquiz.html",
                                 start_time=datetime.utcnow().isoformat(),
                                 binqn=binqn,
                                 decqn=decqn)


@app.route("/bin-dec-quiz/result", methods=["POST"])
def bindec_results():
    record = dict(flask.request.form)
    name = record.pop("student_name")
    start_time = datetime.fromisoformat(record.pop("start_time"))
    duration = (datetime.utcnow() - start_time).seconds
    binresult = []
    decresult = []
    i, prefix = 1, "b"
    target = binresult
    for question, user_ans in record.items():
        if conversion.isbin(question):
            question = question[2:]  # Strip '0b' from left
            correct_ans = int(question, base=2)
            try:
                user_ans = int(user_ans)
            except ValueError:
                pass
            except:
                raise
        else:  # isdec
            correct_ans = int(question)
            try:
                user_ans = int(user_ans, base=2)
            except ValueError:
                pass
            except:
                raise
        if user_ans == correct_ans:
            correct = True
            review = "✔ Correct"
        else:
            correct = False
            review = "✘ Incorrect"
        if i > 5:
            i = 1
            prefix = "d"
            target = decresult
        if target is decresult:
            # Convert correct ans to binary
            correct_ans = bin(correct_ans)[2:]
        label = f"{prefix}{i}"
        target.append([
            label, question,
            str(user_ans), correct,
            str(correct_ans), review
        ])
        i += 1
    score.add_score(name=name,
                    bin_score=calc_score(binresult),
                    dec_score=calc_score(decresult))
    return flask.render_template("review.html",
                                 name=name,
                                 time_taken=duration,
                                 binresult=binresult,
                                 decresult=decresult)


@app.route("/")
@app.route("/conversion-quiz/")
def conversion_quiz():
    questions = conversion.generate_questions(5)
    return flask.render_template("conversion-quiz.html",
                                 start_time=datetime.utcnow().isoformat(),
                                 questions=questions)
    
@app.route("/scores")
def scores():
    scores = score.load()
    return flask.render_template("score.html", scores=scores)


if __name__ == "__main__":
    app.run('0.0.0.0')
