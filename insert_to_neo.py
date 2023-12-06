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
        if 'tags' not in video_info['snippet']:
            continue
        tags=video_info['snippet']['tags']
        tittle_embedding=video['title_embedding_hf']
        video = Video(video_id)
        video.insert_video(video_id,title,description,channel_id,channel_title,tags,tittle_embedding)
        channel=Channel(channel_id)
        channel.insert_channel(channel_id)
        channel.add_video(video.find())
        
        print(f'Inserted video {video_id} into Neo4j')

def add_video_relations():
    mongo = MongoDB()
    videos = mongo.db.test.find()
    for video in videos:
        for video2 in videos:
            if video != video2:
                video1_id = video['videoInfo']['id']
                video2_id = video2['videoInfo']['id']
                video1 = Video(video1_id)
                video2 = Video(video2_id)
                video1.add_related_video(video2)
                print(f'related video {video1_id} and {video2_id} into Neo4j')

if __name__ == '__main__':
    #insert_to_neo()
    add_video_relations()


