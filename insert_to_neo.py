from mongodb import MongoDB
from neo import Video, User, Channel

def insert_to_neo():
    mongo = MongoDB()
    videos = mongo.db.test.find()
    for video in videos:
        video_info=video['videoInfo']
        video_id = video_info['id']
        title = video_info['snippet']['title']
        description = video_info['snippet']['description']
        channel_id = video_info['snippet']['channelId']
        channel_title = video_info['snippet']['channelTitle']
        tags=video_info['snippet']['tags']
        video = Video(video_id)
        video.insert_video(video_id,title,description,channel_id,channel_title,tags)
        channel=Channel(channel_id)
        channel.insert_channel(channel_id,channel_title)
        channel.add_video(video)
        
        print(f'Inserted video {video_id} into Neo4j')

def add_video_relations():
    mongo = MongoDB()
    videos = mongo.db.test.find()
    length = len(videos)
    for i in range(length):
        for j in range(i+1,length):
            video1_id = videos[i]['videoInfo']['id']
            video2_id = videos[j]['videoInfo']['id']
            video1 = Video(video1_id)
            video2 = Video(video2_id)
            video1.add_related_video(video2)
            video2.add_related_video(video1)
            print(f'related video {video1_id} and {video2_id} into Neo4j')

if __name__ == '__main__':
    insert_to_neo()
    add_video_relations()


