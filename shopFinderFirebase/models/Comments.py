from firebase_admin import auth

from models.Like import Like


class Comment(object):
	def __init__(self, username,uid, content, likes=0, likes_list=[]):
		self.content = content
		self.likes = likes
		self.likes_list = likes_list
		self.username = username
		self.uid = uid

	@staticmethod
	def from_dict(source):
		username  = source['username']
		likes = source['likes']
		uid = source['uid']
		likes_list = [Like.from_dict(like) for like in source['likes_list']]
		content = source['content']
		return Comment(username=username,likes=likes,likes_list=likes_list,
		               uid=uid,content=content)



	def to_dict(self):
		data = {
			'likes'     : self.likes,
			'likes_list': [like.to_dict() for like in
			               self.likes_list],
			'username'  : self.username,
			'content'   : self.content,
			'uid'       : self.uid
		}
		return data;



	def __repr__(self):
		return(
            """Comment(username={}, likes={}, 
            likes_list={},uid={},content={})"""
            .format(self.username, self.likes,
                    tuple([str(like) for like in self.likes_list]),
                    self.uid,
                    self.content))
	def get_user_record(self):
		return auth.get_user(self.uid)
