import pymysql
from datetime import datetime

def clicked(user_id, video_id, search_query, video_rank):
    db = pymysql.connect("localhost", "root", "pass", "VIDEOS")
    cursor = db.cursor()
    
    # Create the 'clicks' table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS clicks (user_id VARCHAR(255), video_id VARCHAR(255), search_query VARCHAR(255), video_rank INT, click_timestamp DATETIME, clicks INT);")
    
    # Check if there are existing clicks for this user, video, and search query
    cursor.execute("SELECT clicks FROM clicks WHERE user_id = '{}' AND video_id = '{}' AND search_query = '{}';".format(user_id, video_id, search_query))
    results = cursor.fetchall()

    if len(results) == 0:
        # If no clicks exist, insert a new record
        query = "INSERT INTO clicks(user_id, video_id, search_query, video_rank, click_timestamp, clicks) VALUES ('{}', '{}', '{}', {}, '{}', {});".format(user_id, video_id, search_query, video_rank, datetime.now(), 1)
        cursor.execute(query)
    else:
        # If clicks exist, update the clicks count
        query = "UPDATE clicks SET clicks = clicks + 1 WHERE user_id = '{}' AND video_id = '{}' AND search_query = '{}';".format(user_id, video_id, search_query)
        cursor.execute(query)

    db.commit()
    db.close()

def refresh_trending_videos():
    # For simplicity, let's assume trending videos are the ones with the highest click counts for now
    db = pymysql.connect("localhost", "root", "pass", "VIDEOS")
    cursor = db.cursor()

    # Query to get trending videos (assuming higher clicks mean trending)
    query = "SELECT video_id, SUM(clicks) AS total_clicks FROM clicks GROUP BY video_id ORDER BY total_clicks DESC LIMIT 10;"
    cursor.execute(query)

    trending_videos = cursor.fetchall()
    db.close()

    return trending_videos

def get_trending_videos():
    # Call the refresh_trending_videos function to ensure the trending videos are up-to-date
    trending_videos = refresh_trending_videos()

    return trending_videos
