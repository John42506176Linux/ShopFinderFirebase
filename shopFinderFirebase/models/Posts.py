from models.Like import Like

from models.Comments import Comment


class Post(object):
	def __init__(self, image_url,username,uid, amount_of_comments=0,
	             comments=[], likes=0, likes_list=[],
	             tags=[]):
		self.image_url = image_url
		self.comments = comments
		self.amount_of_comments = amount_of_comments
		self.likes = likes
		self.likes_list = likes_list
		self.username = username
		self.tags = tags
		self.uid = uid

	@staticmethod
	def from_dict(source):
		image_url = source['image_url']
		username  = source['username']
		likes = source['likes']
		tags = source['tags']
		uid = source['uid']
		amount_of_comments = source['amount_of_comments']
		comments = [Comment.from_dict(comment) for comment in source['comments']]
		likes_list = [Like.from_dict(like) for like in source['likes_list']]
		return Post(image_url=image_url,username=username,
		            amount_of_comments=amount_of_comments,
		            comments=comments,likes=likes,likes_list=likes_list,
		            tags=tags,uid=uid)



	def to_dict(self):
		data = {
			'image_url' : self.image_url,
			'comments'  : [comment.to_dict() for comment in
			               self.comments],
			'likes'     : self.likes,
			'likes_list': [like.to_dict() for like in
			               self.likes_list],
			'username'  : self.username,
			'tags'      : self.tags,
			'uid'       : self.uid
		}
		return data;



	def __repr__(self):
		return(
            """Post(image_url={}, username={}, likes={}, tags={}, 
            comments={},likes_list={},uid={})"""
            .format(self.image_url,self.username, self.likes,
                    tuple(self.tags),
                    tuple([str(comment) for comment in self.comments])
                    ,tuple([str(like) for like in self.likes_list]),
                    self.uid ))
	def get_users_liked(self):
		users_liked =[]
		for like in self.likes_list:
			users_liked.append(like.username)
		return users_liked