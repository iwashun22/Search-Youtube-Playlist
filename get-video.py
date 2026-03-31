import urllib.request as request
import urllib.error as req_error
from urllib.parse import urlencode
import sys
import certifi
import json
import re
from ssl import create_default_context

API_TOKEN="YOUR_GOOGLE_API_TOKEN"

context = create_default_context(cafile=certifi.where())

def get_video(playlist, search_str):
    PAGE_TOKEN = ''
    next_page_exist = True
    videos = []

    try:
        while next_page_exist:
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

            with request.urlopen(url, context=context) as response:
                data = response.read().decode('utf-8')
                data_json = json.loads(data)
                next_page_exist = 'nextPageToken' in data_json

                found_videos = find_matching_title(data_json['items'], search_str)
                if next_page_exist:
                    PAGE_TOKEN = data_json['nextPageToken']
                    print("Scanning:", PAGE_TOKEN)
                else:
                    next_page_exist = False

                if found_videos is not None:
                    videos.extend(found_videos)

    except req_error.HTTPError as e:
        print(f'HTTP error: {e.code} {e.reason}')
    except req_error.URLError as e:
        print(f'URL error: {e.reason}')

    return videos if len(videos) > 0 else None


def find_matching_title(items_arr, search_str):
    matched = []

    for item in items_arr:
        title = item['snippet']['title']
        pattern = rf"{search_str}"
        match = re.search(pattern, title, re.IGNORECASE)

        if match:
            matched.append(item)
    return matched if len(matched) > 0 else None
        
def colored(ansi_code, val):
    return f"\033[38;5;{ansi_code}m{val}\033[0m"


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Arguments are missing. Usage: <playlist_id> <search_value>")
        sys.exit()


    playlist_id = sys.argv[1]
    search_str = "\s".join(sys.argv[2:])

    video_arr = get_video(playlist_id, search_str)
    
    if video_arr is None:
        print("No matching results were found in the playlist.")
        sys.exit()
    
    for i, video_data in enumerate(video_arr):
        video_id = video_data['snippet']['resourceId']['videoId']
        formatted_link = f"https://youtube.com/watch?v={video_id}"

        print(f"\n{colored(221, '#'*8)}  {colored(214, i+1)}  {colored(221, '#'*8)}")

        print(
            colored(99, "Title:"),
            colored(135, video_data['snippet']['title'])
        )
        print(
            colored(76, "Link:"),
            colored(114, formatted_link)
        )
    

