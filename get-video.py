import urllib.request as request
import urllib.error as req_error
from urllib.parse import urlencode
import sys
import certifi
import json
import re

API_TOKEN="AIzaSyAgBwXNEAhWo403mR94B3ZK6uvfKqe0_r4"

def get_video(playlist, search_str):
    video_found = False
    PAGE_TOKEN = ''
    next_page_exist = True

    try:
        while(not video_found and next_page_exist):
            query = {
                'part': 'snippet',
                'playlistId': playlist,
                'maxResult': 50,
                'key': API_TOKEN
            }
            if PAGE_TOKEN:
                query['pageToken'] = PAGE_TOKEN

            query_string = urlencode(query)
            url = f'https://www.googleapis.com/youtube/v3/playlistItems?{query_string}'

            with request.urlopen(url, cafile=certifi.where()) as response:
                data = response.read().decode('utf-8')
                data_json = json.loads(data)
                next_page_exist = 'nextPageToken' in data_json

                metadata = find_matching_title(data_json['items'], search_str)
                if next_page_exist:
                    PAGE_TOKEN = data_json['nextPageToken']
                    print("Scanning:", PAGE_TOKEN)
                else:
                    next_page_exist = False

                if metadata is not None:
                    video_found = True
                    return metadata
    except req_error.HTTPError as e:
        print(f'HTTP error: {e.code} {e.reason}')
    except req_error.URLError as e:
        print(f'URL error: {e.reason}')

    return None


def find_matching_title(items_arr, search_str):
    for item in items_arr:
        title = item['snippet']['title']
        pattern = rf"{search_str}"
        match = re.search(pattern, title, re.IGNORECASE)

        if match:
            return item
    return None
        

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Arguments are missing. Usage: <playlist_id> <search_value>")
        sys.exit()


    playlist_id = sys.argv[1]
    search_str = "\s".join(sys.argv[2:])

    video_data = get_video(playlist_id, search_str)
    
    if video_data is None:
        print("No matching results were found in the playlist.")
        sys.exit()
    
    video_id = video_data['snippet']['resourceId']['videoId']
    formatted = f"https://youtube.com/watch?v={video_id}"
    print(formatted)
    

