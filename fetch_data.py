import secrets
import requests
import time
import json

CLIENT_SECRET = secrets.SPOTIFY_API_SECRET
CLIENT_ID = secrets.SPOTIFY_API_CLIENT_ID
LASTFM_API_KEY = secrets.LASTFM_API_KEY 


##### Spotify Authentication (OAuth)
AUTH_URL = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(AUTH_URL, {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'client_credentials'
})
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']
headers = {'Authorization': 'Bearer {token}'.format(token = access_token)}


##### Setting Up Cache
CACHE_FILENAME = 'cacheArtistSearch.json'
CACHE_DICT = {}

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key

def make_request(baseurl, params):
    response = requests.get(baseurl, params=params, headers = headers)
    return response.json()

def make_request_with_cache(baseurl, params):
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("cache hit!", request_key)
        return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
        CACHE_DICT[request_key] = make_request(baseurl, params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

CACHE_DICT = open_cache()


##### Fetching Last.FM Data
lastfm_base_url = 'http://ws.audioscrobbler.com/2.0/'
top_tracks_data = []

def get_top_tracks():
    for page in range(1,21):
        params = {'method':'chart.getTopTracks', 'api_key': LASTFM_API_KEY, 'page': page,'format':'json'}
        response = make_request_with_cache(lastfm_base_url, params)
        results = response['tracks']['track']
        for track in results:
            track_dict = {}
            track_dict["Track"] = track['name']
            track_dict["Artist"] = track['artist']['name']
            track_dict.update(get_track_info(track['name'], track['artist']['name']))
            try:
                track_dict["Genre"] = get_track_top_tags(track['name'], track['artist']['name'])
            except: continue
            track_dict.update(get_track_audio_features(track['name'], track['artist']['name']))
            top_tracks_data.append(track_dict)
        time.sleep(1)
    return top_tracks_data

def get_track_top_tags(track, artist):
    params = {
                'method':'track.getTopTags',
                'api_key': LASTFM_API_KEY,
                'format':'json',
                'track': track,
                'artist': artist
            }
    response = make_request_with_cache(lastfm_base_url, params)
    top_tag = response['toptags']['tag'][0]['name']
    return top_tag  


##### Fetching Spotify Data
def spotify_search_track(track_artist):
    spotify_base_url = 'https://api.spotify.com/v1/search'
    params = {'q':track_artist, 'type':'track'}
    response = make_request_with_cache(spotify_base_url, params)
    track_id = response['tracks']['items'][0]['id']
    return track_id

def get_track_info(track, artist):
    track_artist = track + ' ' + artist
    track_id = spotify_search_track(track_artist)
    spotify_base_url = f'https://api.spotify.com/v1/tracks/{track_id}'
    params = {}
    response = make_request_with_cache(spotify_base_url, params)
    track_info_dict = {}
    track_info_dict['Album'] = response['album']['name']
    track_info_dict['Release Date'] = response['album']['release_date']
    track_info_dict['Popularity'] = response['popularity']
    return track_info_dict

def get_track_audio_features(track, artist):
    track_artist = track + ' ' + artist
    track_id = spotify_search_track(track_artist)
    spotify_base_url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    params = {}
    response = make_request_with_cache(spotify_base_url, params)
    audio_feature_dict = {}
    audio_feature_dict['acousticness'] = response['acousticness']
    audio_feature_dict['danceability'] = response['danceability']
    audio_feature_dict['energy'] = response['energy']
    audio_feature_dict['instrumentalness'] = response['instrumentalness']
    audio_feature_dict['liveness'] = response['liveness']
    audio_feature_dict['loudness'] = response['loudness']
    audio_feature_dict['speechiness'] = response['speechiness']
    audio_feature_dict['tempo'] = response['tempo']
    audio_feature_dict['valence'] = response['valence']
    audio_feature_dict['duration'] = float(response['duration_ms']) / 1000
    return audio_feature_dict


get_top_tracks()

with open("Top_Tracks_Data.json", "w") as outfile:
    json.dump(top_tracks_data, outfile)