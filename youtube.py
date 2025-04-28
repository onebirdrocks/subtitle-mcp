from youtube_transcript_api import YouTubeTranscriptApi

def fetch_youtube_subtitles(video_id, lang="en"):
    """
    抓取YouTube视频字幕
    :param video_id: YouTube视频ID，比如"https://www.youtube.com/watch?v=abcd1234"中的"abcd1234"
    :param lang: 优先语言，默认英文（en）
    :return: 字幕列表，每一条是 {'text': '内容', 'start': 开始秒数, 'duration': 持续秒数}
    """
    try:
        # 获取字幕列表
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # 找到目标语言的字幕
        if transcript_list.find_manually_created_transcript([lang]):
            transcript = transcript_list.find_manually_created_transcript([lang])
        else:
            transcript = transcript_list.find_generated_transcript([lang])
        
        subtitles = transcript.fetch()
        return subtitles

    except Exception as e:
        print(f"抓取字幕失败: {e}")
        return []

# 示例
if __name__ == "__main__":
    video_id = "dQw4w9WgXcQ"  # 替换成你的YouTube视频ID
    subs = fetch_youtube_subtitles(video_id)
    for sub in subs:
        print(f"{sub['start']:.2f}s: {sub['text']}")

