import json

from auth import auth_vk

vk = auth_vk()

#show all information within message header only
MESSAGE_HEADER_ID = 0


class User(object):
    def __init__(self, id):
        self.id = id
        self.user = vk.users.get(user_ids=self.id, fields='photo_50')[0]

    def footer(self):
        footer = self.user['first_name'] + ' ' + self.user['last_name']
        footer_icon = self.user['photo_50']
        return footer, footer_icon


class Group(object):
    def __init__(self, id):
        self.id = id
        self.group = vk.groups.getById(group_id=self.id)[0]

    def footer(self):
        footer = self.group['name']
        footer_icon = self.group['photo']

        return footer, footer_icon


class Slack(object):
    def __init__(self, post):
        try:
            if post['copy_history']:
                self.repost = Repost(post['copy_history'][0])
                self.post = Post(post)
                try:
                    self.repost.howManyAttachments = len(post['copy_history'][0]['attachments'])
                except Exception:
                    self.repost.howManyAttachments = 0
                try:
                    self.post.howManyAttachments=len(post['attachments'])
                except Exception:
                    self.post.howManyAttachments=0
        except KeyError:
            self.post = Post(post)
            try:
                self.post.howManyAttachments = len(post['attachments'])
            except Exception:
                self.post.howManyAttachments = 0

    def create_attachments(self):
        data_to_send = self.post.json_prepare()
        try:
            if self.repost:
                data_repost_to_send = self.repost.json_prepare()
                for i in data_repost_to_send:
                    data_to_send.append(i)
                return json.dumps([data_to_send][0])
        except AttributeError:
            for i in range(self.post.howManyAttachments):
                data_to_send[i]['mrkdwn_in'] = ['text']
        return json.dumps([data_to_send][0])

    @staticmethod
    def send_message(auth, channel, text, attachments=None, as_user=True):
        auth.chat.post_message(channel=channel,
                               text=text,
                               attachments=attachments,
                               as_user=as_user)


class Post(object):
    def __init__(self, post):
        self.text = post['text']
        self.ts = post['date']
        self.color = '#0093DA'
        self.footer, self.footer_icon = self.get_footer(post)
        self.image_url=[]
        self.thumb_url=[]
        self.howManyAttachments=0
        try:
            for i in post['attachments']:
                try:
                        new_image_url, new_thumb_url = self.get_image(
                            i)
                        self.image_url.append(new_image_url)
                        self.thumb_url.append(new_thumb_url)
                except KeyError:
                    self.image_url, self.thumb_url = [''], ['']
        except KeyError:
            self.image_url, self.thumb_url = [''], ['']

    @staticmethod
    def get_image(attachment):
            if attachment['type'] == 'photo':
                image = attachment['photo']
                try:
                    image_url = image['photo_1280']
                except KeyError:
                    try:
                        image_url = image['photo_807']
                    except KeyError:
                        image_url = image['photo_604']
                thumb_url = image['photo_75']
                return image_url, thumb_url
            else:
                return None, None

    @staticmethod
    def get_footer(post):
        if post['owner_id'] < 0:
            author = Group(id=str(post['owner_id'])[1:])
            footer, footer_icon = author.footer()
            return footer, footer_icon
        else:
            author = User(id=post['owner_id'])
            footer, footer_icon = author.footer()
            return footer, footer_icon
    #FIXME Разделить кол-во аттачментов к посту и к репосту
    def json_prepare(self):
        items=[]
        if self.howManyAttachments==0: #if only text in message
            self.howManyAttachments=1  #handle it
        for i in range(self.howManyAttachments):
            items.append(
                {
                    'fallback':    '',
                    'color':       self.color,
                    'text':        (lambda x: self.text if i==MESSAGE_HEADER_ID else '')(i),
                    'ts':          (lambda x: self.ts if i==MESSAGE_HEADER_ID else 0)(i),
                    'footer':      (lambda x: self.footer if i==MESSAGE_HEADER_ID else '')(i),
                    'footer_icon': (lambda x: self.footer_icon if i==MESSAGE_HEADER_ID else '')(i),
                    'image_url':   self.image_url[i],
                    'thumb_url':   self.thumb_url[i]
                }
            )
        return items


class Repost(Post):
    def __init__(self, repost):
        Post.__init__(self, post=repost)
        self.text = repost['text']
        self.ts = repost['date']
        self.color = '#1C6047'
        self.footer, self.footer_icon = self.get_footer(repost)
        self.image_url=[]
        self.thumb_url=[]
        self.howManyAttachments=0
        try:
            for i in repost['attachments']:
                try:
                        new_image_url, new_thumb_url = self.get_image(
                            i)
                        self.image_url.append(new_image_url)
                        self.thumb_url.append(new_thumb_url)
                except KeyError:
                    self.image_url, self.thumb_url = [''], ['']
        except KeyError:
            self.image_url, self.thumb_url = [''], ['']
