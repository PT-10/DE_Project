import config 
from py2neo import Graph, Node, Relationship
import numpy as np

# url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
# username = os.environ.get('NEO4J_USERNAME')
# password = os.environ.get('NEO4J_PASSWORD')
# graph = Graph(url + '/db/data/', username=username, password=password)
graph = Graph("bolt://localhost:7687", auth=(config.neo4j_user, config.neo4j_pass))

class User:
    def __init__(self, username):
        self.username = username
    
    def register(self):
        if not self.find():
            user = Node('User', username=self.username)
            graph.create(user)
            return True
        else:
            return False

    def find(self):
        user = graph.find_one('User', 'username', self.username)
        return user

    def subscribe(self, channel_name):
        if not self.is_subscribed(channel_name):
            Channel(channel_name).subscribe(self.find())
            return True
        return False

    def is_subscribed(self, channel_name):
        query = """
        MATCH (n:User)-[r]-(v:Channel)
        WHERE n.username={user} and v.channelId={vid}
        RETURN COUNT(r) as count
        """
        return graph.data(query, user=self.find()['username'], vid=channel_name)[0]['count']

    def unsubscribe(self, channel_name):
        query = """
        MATCH (n:User)-[r]-(v:Channel)
        WHERE n.username={user} and v.channelId={vid}
        DELETE r
        """
        graph.run(query, user=self.find()['username'], vid=channel_name)

    def like_video(self, video_id):
        user = self.find()
        Video(video_id).like(user)

    def dislike_video(self, video_id):
        user = self.find()
        Video(video_id).dislike(user)

    def is_liked_video(self, video_id):
        query = """
        MATCH (n:User)-[r:Likes]-(v:Video)
        WHERE n.username={user} and v.videoId={vid}
        RETURN COUNT(r) as count
        """
        return graph.data(query, user=self.find()['username'], vid=video_id)[0]['count']

    def is_disliked_video(self, video_id):
        query = """
        MATCH (n:User)-[r:Dislikes]-(v:Video)
        WHERE n.username={user} and v.videoId={vid}
        RETURN COUNT(r) as count
        """
        return graph.data(query, user=self.find()['username'], vid=video_id)[0]['count']

    def clear_rel_with_video(self, video_id):
        user = self.find()
        Video(video_id).clear_user_rel(user)

    def liked_videos(self):
        query = '''
        MATCH (user:User)-[:Likes]-(video:Video)
        WHERE user.username = {user}
        RETURN DISTINCT video.mongoId
        '''
        return graph.data(query, user=self.username)

    def disliked_videos(self):
        query = '''
        MATCH (user:User)-[:Dislikes]-(video:Video)
        WHERE user.username = {user}
        RETURN DISTINCT video.mongoId
        '''
        return graph.data(query, user=self.username)


class Channel:

    def __init__(self, channel_name):
        self.name = channel_name
    
    def insert_channel(self,chanelId):
        if self.find():
            return False
        channel = Node('Channel', channelId=chanelId)
        graph.create(channel)
        return True

    def find(self):
        channel = graph.find_one('Channel', 'channelId', self.name)
        return channel

    def subscribers(self):
        query = '''
        MATCH (user:User)-[:Subscriber]-(channel:Channel)
        WHERE channel.channelId = {channel}
        RETURN DISTINCT user.username
        '''
        return graph.run(query, channel=self.name)

    def subscriber_count(self):
        query = '''
        MATCH (user:User)-[:Subscriber]-(channel:Channel)
        WHERE channel.channelId = {channel}
        RETURN COUNT(DISTINCT user)
        '''
        return graph.run(query, channel=self.name)

    def video_count(self):
        query = '''
        MATCH (video:Video)-[:HasChannel]-(channel:Channel)
        WHERE channel.channelId = {channel}
        RETURN COUNT(DISTINCT video)
        '''
        return graph.run(query, channel=self.name)

    def videos(self):
        query = '''
        MATCH (video:Video)-[:HasChannel]-(channel:Channel)
        WHERE channel.channelId = {channel}
        RETURN DISTINCT video.videoId
        '''
        return graph.run(query, channel=self.name)

    def add_video(self, video):
        graph.create(Relationship(video, "HasChannel", self.find()))
    def subscribe(self, user):
        graph.create(Relationship(user, "Subscriber", self.find()))


class Video:

    def __init__(self, id_):
        self.id = id_
    
    def insert_video(self,mongoid,title,description,channelId,channelTitle,tags):
        video = Node('Video', videoId=self.id, mongoId=mongoid, title=title, description=description, channelId=channelId, channelTitle=channelTitle,tags=tags)
        graph.create(video)
        return True


    def find(self):
        video = graph.find_one('Video', 'videoId', self.id)
        return video
    
    def get_channel(self):
        query = '''
        MATCH (video:Video)-[:HasChannel]-(channel:Channel)
        WHERE video.videoId = {video_id}
        RETURN DISTINCT channel.channelId
        '''
        return graph.data(query, video_id=self.id)[0]['channel.channelId']

    def liked_by(self):
        query = '''
        MATCH (user:User)-[:Likes]-(video:Video)
        WHERE video.videoId = {video_id}
        RETURN DISTINCT user.username
        '''
        return graph.run(query, video_id=self.id)

    def liked_by_count(self):
        query = '''
        MATCH (user:User)-[:Likes]-(video:Video)
        WHERE video.videoId = {video_id}
        RETURN COUNT(DISTINCT user.username) as count
        '''
        return graph.data(query, video_id=self.id)[0]['count']

    def disliked_by(self):
        query = '''
        MATCH (user:User)-[:Dislikes]-(video:Video)
        WHERE video.videoId = {video_id}
        RETURN DISTINCT user.username
        '''
        return graph.run(query, video_id=self.id)

    def disliked_by_count(self):
        query = '''
        MATCH (user:User)-[:Dislikes]-(video:Video)
        WHERE video.videoId = {video_id}
        RETURN COUNT(DISTINCT user.username) as count
        '''
        return graph.data(query, video_id=self.id)[0]['count']

    def like(self, user):
        self.clear_user_rel(user)
        graph.create(Relationship(user, "Likes", self.find()))

    def dislike(self, user):
        self.clear_user_rel(user)
        graph.create(Relationship(user, "Dislikes", self.find()))

    def clear_user_rel(self, user):
        query = """
        MATCH (n:User)-[r]-(v:Video)
        WHERE n.username={user} and v.videoId={vid}
        DELETE r
        """
        graph.run(query, user=user['username'], vid=self.find()['videoId'])

    def add_related_video(self, video):
        current_channel = self.get_channel()
        related_channel = video.get_channel()
        if current_channel == related_channel:
            same_channel = True
        common_tags = len(set(self.find()['tags']).intersection(set(video.find()['tags'])))
        common_description = commonDescription(self.find()['description_embedding'], video.find()['description_embedding'])
        common_title = commonTitle(self.find()['title_embedding'], video.find()['title_embedding'])
        if same_channel:
            similarity = 0.5 * common_tags + 0.25 * common_description + 0.25 * common_title
        else:
            similarity = 0.25 * common_tags + 0.375 * common_description + 0.375 * common_title
        graph.create(Relationship(self.find(), "Related", video.find(),weight=similarity))
        

def commonDescription(x, y):
    return cosine_similarity(x, y)

def commonTitle(x, y):
    return cosine_similarity(x, y)

def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    similarity = dot_product / (magnitude_a * magnitude_b)
    return similarity