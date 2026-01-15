import pyncm
from pyncm import apis
from auth import load_session

def get_daily_recommendations():
    """获取每日推荐歌曲"""
    # 确保已登录
    if not load_session()[0]:
        return {"success": False, "error": "未登录，请先调用 login 工具"}
    
    try:
        # 定义内部函数并使用 WeapiCryptoRequest 装饰
        @apis.WeapiCryptoRequest
        def GetDailyRecommendInternal():
            return "/weapi/v1/discovery/recommend/songs", {"limit": 30, "offset": 0, "total": True}
        
        # 调用内部函数 (session 会被自动注入)
        result = GetDailyRecommendInternal()
        
        if result['code'] == 200:
            songs = []
            for song in result['recommend']:
                songs.append({
                    "id": song['id'],
                    "name": song['name'],
                    "artist": song['artists'][0]['name'] if song['artists'] else "未知",
                    "album": song['album']['name'] if song['album'] else ""
                })
            return {"success": True, "songs": songs}
        else:
            return {"success": False, "error": f"API 错误: {result.get('message', '未知错误')}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_user_playlists():
    """获取用户的歌单"""
    if not load_session()[0]:
        return {"success": False, "error": "未登录"}
    
    try:
        # 获取当前用户 ID
        user_info = apis.login.GetCurrentLoginStatus()
        uid = user_info['profile']['userId']
        
        result = apis.user.GetUserPlaylists(uid)
        if result['code'] == 200:
            playlists = []
            for pl in result['playlist']:
                playlists.append({
                    "id": pl['id'],
                    "name": pl['name'],
                    "count": pl['trackCount'],
                    "creator": pl['creator']['nickname'],
                    "is_mine": pl['creator']['userId'] == uid
                })
            return {"success": True, "playlists": playlists}
        else:
            return {"success": False, "error": "API 请求失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def search_song(keyword, limit=5):
    """搜索歌曲"""
    # 搜索不需要登录，但登录后结果更准
    load_session() 
    try:
        result = apis.cloudsearch.GetSearchResult(keyword, stype=1, limit=limit)
        if result['code'] == 200 and 'result' in result and 'songs' in result['result']:
            songs = []
            for song in result['result']['songs']:
                songs.append({
                    "id": song['id'],
                    "name": song['name'],
                    "artist": song['ar'][0]['name'] if song['ar'] else "未知"
                })
            return {"success": True, "songs": songs}
        return {"success": False, "error": "未找到结果"}
    except Exception as e:
        return {"success": False, "error": str(e)}
