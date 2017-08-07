from flask import Flask, abort, request, render_template
from auth import auth_slack
from config import *
from message import *

app = Flask(__name__)


def getNameById(_id):
    profile=vk.users.get(user_ids=_id)
    return profile[0]['first_name']+' '+profile[0]['last_name']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/callback/xE4sA', methods=['GET', 'POST'])
def callback():
    if not request.json or 'type' not in request.json:
        abort(403)

    if request.json['type'] == 'confirmation':
        print(confirmation_token_)
        return confirmation_token_

    if request.json['type'] == 'wall_post_new':
        post = request.json['object']

        text=''

        if post['post_type']=='suggest':
            text+='new suggested post from '
        else:
            text+='new wallpost from '
        attachments = Slack(post=post).create_attachments()
        Slack.send_message(auth=slack, channel=channel_, text=text+getNameById(request.json['object']['created_by'])+'\npost id: '+str(post['id']),
                           attachments=attachments)

        return 'ok', 200


slack = auth_slack()

if __name__ == '__main__':
    app.run()
