import json
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from bilibili_api import video, comment, Credential, search, user
from bilibili_api.utils.danmaku import Danmaku
from bilibili_api.comment import CommentResourceType, OrderType
from bilibili_api.search import SearchObjectType, OrderVideo


CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {CONFIG_PATH}\n"
            f"请复制 config.example.json 为 config.json 并填写你的凭证"
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


config = load_config()
credential = Credential(
    sessdata=config["sessdata"],
    bili_jct=config["bili_jct"],
    buvid3=config.get("buvid3", ""),
)

mcp = FastMCP("Bilibili Tools", dependencies=["bilibili-api-python", "aiohttp"])


@mcp.tool()
async def send_danmaku(
    bvid: str,
    message: str,
    dm_time: float = 0.0,
    mode: int = 1,
    fontsize: int = 25,
    color: int = 16777215,
    page: int = 0,
) -> str:
    """
    给B站视频发送弹幕

    Args:
        bvid: 视频的BV号，例如 "BV1xx411q7Mv"
        message: 弹幕内容
        dm_time: 弹幕出现的时间（秒），默认为0.0
        mode: 弹幕模式，1=滚动，5=顶端，4=底端，默认为1
        fontsize: 字体大小，18=小，25=标准，36=大，默认为25
        color: 弹幕颜色，十进制，默认为16777215（白色）
        page: 分P编号，从0开始，默认为0

    Returns:
        发送结果信息
    """
    try:
        v = video.Video(bvid=bvid, credential=credential)
        color_hex = hex(color)[2:].zfill(6)
        danmaku = Danmaku(
            text=message,
            dm_time=dm_time,
            mode=mode,
            font_size=fontsize,
            color=color_hex,
        )
        result = await v.send_danmaku(page_index=page, danmaku=danmaku)
        return f"弹幕发送成功！\n视频: {bvid}\n内容: {message}\n时间: {dm_time}秒"
    except Exception as e:
        return f"弹幕发送失败: {str(e)}"


@mcp.tool()
async def send_comment(
    bvid: str,
    message: str,
    page: int = 0,
) -> str:
    """
    给B站视频发送评论

    Args:
        bvid: 视频的BV号，例如 "BV1xx411q7Mv"
        message: 评论内容
        page: 分P编号，从0开始，默认为0

    Returns:
        发送结果信息
    """
    try:
        v = video.Video(bvid=bvid, credential=credential)
        info = await v.get_info()
        oid = info["aid"]
        result = await comment.send_comment(
            text=message,
            oid=oid,
            type_=CommentResourceType.VIDEO,
            credential=credential
        )
        return f"评论发送成功！\n视频: {bvid}\n内容: {message}"
    except Exception as e:
        return f"评论发送失败: {str(e)}"


@mcp.tool()
async def get_video_info(bvid: str) -> str:
    """
    获取B站视频信息

    Args:
        bvid: 视频的BV号

    Returns:
        视频信息（标题、播放量、点赞数等）
    """
    try:
        v = video.Video(bvid=bvid)
        info = await v.get_info()
        stat = info["stat"]
        return (
            f"视频标题: {info['title']}\n"
            f"UP主: {info['owner']['name']}\n"
            f"播放量: {stat['view']}\n"
            f"点赞: {stat['like']}\n"
            f"投币: {stat['coin']}\n"
            f"收藏: {stat['favorite']}\n"
            f"弹幕: {stat['danmaku']}\n"
            f"评论: {stat['reply']}"
        )
    except Exception as e:
        return f"获取视频信息失败: {str(e)}"


@mcp.tool()
async def like_video(bvid: str, status: bool = True) -> str:
    """
    给视频点赞或取消点赞

    Args:
        bvid: 视频的BV号
        status: True=点赞，False=取消点赞，默认为True

    Returns:
        操作结果信息
    """
    try:
        v = video.Video(bvid=bvid, credential=credential)
        result = await v.like(status)
        return f"点赞成功！\n视频: {bvid}\n状态: {'点赞' if status else '取消点赞'}"
    except Exception as e:
        return f"点赞失败: {str(e)}"


@mcp.tool()
async def pay_coin(bvid: str, num: int = 1, like: bool = False) -> str:
    """
    给视频投币

    Args:
        bvid: 视频的BV号
        num: 投币数量，1或2个，默认为1
        like: 是否同时点赞，默认为False

    Returns:
        操作结果信息
    """
    try:
        v = video.Video(bvid=bvid, credential=credential)
        result = await v.pay_coin(num=num, like=like)
        return f"投币成功！\n视频: {bvid}\n投币数: {num}\n同时点赞: {'是' if like else '否'}"
    except Exception as e:
        return f"投币失败: {str(e)}"


@mcp.tool()
async def set_favorite(bvid: str, add_media_ids: list = None, del_media_ids: list = None) -> str:
    """
    设置视频收藏

    Args:
        bvid: 视频的BV号
        add_media_ids: 要添加到的收藏夹ID列表，默认为None
        del_media_ids: 要移出的收藏夹ID列表，默认为None

    Returns:
        操作结果信息
    """
    try:
        if add_media_ids is None:
            add_media_ids = []
        if del_media_ids is None:
            del_media_ids = []
        v = video.Video(bvid=bvid, credential=credential)
        result = await v.set_favorite(add_media_ids=add_media_ids, del_media_ids=del_media_ids)
        return f"收藏操作成功！\n视频: {bvid}\n添加到: {add_media_ids}\n移出: {del_media_ids}"
    except Exception as e:
        return f"收藏操作失败: {str(e)}"


@mcp.tool()
async def one_click_three_operations(bvid: str, coin_num: int = 1) -> str:
    """
    一键三连（点赞+投币+收藏）

    Args:
        bvid: 视频的BV号
        coin_num: 投币数量，1或2个，默认为1

    Returns:
        操作结果信息
    """
    try:
        results = []
        v = video.Video(bvid=bvid, credential=credential)
        
        await v.like(True)
        results.append("点赞成功")
        
        await v.pay_coin(num=coin_num, like=False)
        results.append(f"投币{coin_num}个成功")
        
        await v.set_favorite(add_media_ids=[], del_media_ids=[])
        results.append("收藏成功")
        
        return f"一键三连成功！\n视频: {bvid}\n" + "\n".join(results)
    except Exception as e:
        return f"一键三连失败: {str(e)}"


@mcp.tool()
async def get_danmaku_list(bvid: str, page: int = 0) -> str:
    """
    获取视频弹幕列表

    Args:
        bvid: 视频的BV号
        page: 分P编号，从0开始，默认为0

    Returns:
        弹幕列表（最多显示50条）
    """
    try:
        v = video.Video(bvid=bvid)
        danmakus = await v.get_danmakus(page_index=page)
        
        result = [f"视频弹幕列表（共{len(danmakus)}条，显示前50条）:"]
        for i, dm in enumerate(danmakus[:50], 1):
            result.append(f"{i}. [{dm.dm_time:.1f}秒] {dm.text}")
        
        return "\n".join(result)
    except Exception as e:
        return f"获取弹幕列表失败: {str(e)}"


@mcp.tool()
async def get_comment_list(bvid: str, page_index: int = 1) -> str:
    """
    获取视频评论列表

    Args:
        bvid: 视频的BV号
        page_index: 页码，从1开始，默认为1

    Returns:
        评论列表（每页最多20条）
    """
    try:
        v = video.Video(bvid=bvid)
        info = await v.get_info()
        oid = info["aid"]
        
        comments = await comment.get_comments(
            oid=oid,
            type_=CommentResourceType.VIDEO,
            page_index=page_index,
            order=OrderType.TIME,
            credential=credential
        )
        
        result = [f"视频评论列表（第{page_index}页）:"]
        if "replies" in comments and comments["replies"]:
            for i, rep in enumerate(comments["replies"][:20], 1):
                result.append(f"{i}. {rep['member']['uname']}: {rep['content']['message']}")
        else:
            result.append("暂无评论")
        
        return "\n".join(result)
    except Exception as e:
        return f"获取评论列表失败: {str(e)}"


@mcp.tool()
async def search_video(keyword: str, page: int = 1) -> str:
    """
    搜索视频

    Args:
        keyword: 搜索关键词
        page: 页码，从1开始，默认为1

    Returns:
        搜索结果列表（每页最多20条）
    """
    try:
        result = await search.search_by_type(
            keyword=keyword,
            search_type=SearchObjectType.VIDEO,
            order_type=OrderVideo.TOTALRANK,
            page=page
        )
        
        output = [f"视频搜索结果（关键词: {keyword}，第{page}页）:"]
        if "result" in result and result["result"]:
            for i, item in enumerate(result["result"][:20], 1):
                output.append(f"{i}. {item['title']} (BV: {item['bvid']}) - {item['author']}")
                output.append(f"   播放: {item['play']} | 弹幕: {item['video_review']}")
        else:
            output.append("未找到相关视频")
        
        return "\n".join(output)
    except Exception as e:
        return f"搜索失败: {str(e)}"


@mcp.tool()
async def get_user_videos(uid: int, page: int = 1, page_size: int = 30) -> str:
    """
    获取用户投稿视频列表

    Args:
        uid: 用户UID
        page: 页码，从1开始，默认为1
        page_size: 每页数量，默认为30

    Returns:
        用户投稿视频列表
    """
    try:
        u = user.User(uid=uid)
        videos = await u.get_videos(pn=page, ps=page_size)
        
        output = [f"用户投稿视频列表（UID: {uid}，第{page}页）:"]
        if "list" in videos and "vlist" in videos["list"]:
            for i, item in enumerate(videos["list"]["vlist"], 1):
                output.append(f"{i}. {item['title']} (BV: {item['bvid']})")
                output.append(f"   播放: {item['play']} | 时长: {item['length']}")
        else:
            output.append("该用户暂无投稿")
        
        return "\n".join(output)
    except Exception as e:
        return f"获取用户投稿失败: {str(e)}"


@mcp.tool()
async def batch_comment_user_videos(uid: int, message: str, video_indices: list = None) -> str:
    """
    批量评论用户投稿视频

    Args:
        uid: 用户UID
        message: 评论内容
        video_indices: 要评论的视频索引列表（从1开始），None表示评论所有视频

    Returns:
        评论结果信息
    """
    try:
        u = user.User(uid=uid)
        videos = await u.get_videos(pn=1, ps=100)
        
        if "list" not in videos or "vlist" not in videos["list"]:
            return "该用户暂无投稿"
        
        video_list = videos["list"]["vlist"]
        
        if video_indices is None:
            target_videos = video_list
        else:
            target_videos = [video_list[i-1] for i in video_indices if 1 <= i <= len(video_list)]
        
        results = []
        for item in target_videos:
            try:
                v = video.Video(bvid=item["bvid"], credential=credential)
                info = await v.get_info()
                oid = info["aid"]
                await comment.send_comment(
                    text=message,
                    oid=oid,
                    type_=CommentResourceType.VIDEO,
                    credential=credential
                )
                results.append(f"✅ {item['title']} - 评论成功")
            except Exception as e:
                results.append(f"❌ {item['title']} - 评论失败: {str(e)}")
        
        return f"批量评论完成！\n共 {len(target_videos)} 个视频\n\n" + "\n".join(results)
    except Exception as e:
        return f"批量评论失败: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
