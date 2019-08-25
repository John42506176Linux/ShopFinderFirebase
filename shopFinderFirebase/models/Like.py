from models.Posts import *
class Like(object):
	def __init__(self, username,liked_post):
		self.username = username
		self.liked_post= liked_post

	@staticmethod
	def from_dict(source):
		username  = source['username']
		liked_post_dict = source['liked_post']
		if 'image_url' in liked_post_dict: ## Checks if its a comment or a post
			liked_post = Post.from_dict(liked_post_dict)
		else:
			liked_post = Comment.from_dict(liked_post_dict)

		return Like(username=username,liked_post=liked_post)



	def to_dict(self):
		data = {
			'liked_post'     : self.liked_post.to_dict(),
			'username'       : self.username,
		}
		return data;



	def __repr__(self):
		return(
            """Like(username={}, liked_post={})"""
            .format(self.username, str(self.liked_post)))