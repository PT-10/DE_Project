import pymysql

def clicked(user_id, video_id):
    db = pymysql.connect("localhost", "root", "pass", "VIDEOS")
    cursor = db.cursor()
    
    # Create the 'clicks' table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS clicks (user_id VARCHAR(255), video_id VARCHAR(255), clicks INT);")
    
    # Check if there are existing clicks for this user and video
    cursor.execute("SELECT clicks FROM clicks WHERE user_id = '{}' AND video_id = '{}';".format(user_id, video_id))
    results = cursor.fetchall()

    if len(results) == 0:
        # If no clicks exist, insert a new record
        query = "INSERT INTO clicks(user_id, video_id, clicks) VALUES ('{}', '{}', {});".format(user_id, video_id, 1)
        cursor.execute(query)
        #print("1")
    else:
        # If clicks exist, update the clicks count
        query = "UPDATE clicks SET clicks = clicks + 1 WHERE user_id = '{}' AND video_id = '{}';".format(user_id, video_id)
        cursor.execute(query)
        #print("2")

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

    # You can further process the trending_videos data and return it as needed
    return trending_videos

