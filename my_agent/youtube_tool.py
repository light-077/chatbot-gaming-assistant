"""
YouTube Search Tool using YouTube Data API v3.

Provides direct YouTube URLs, titles, channels, and metadata
that GoogleSearchTool's grounding does not expose locally.
"""

import os

from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def search_youtube(
    query: str,
    max_results: int = 5,
) -> list[dict]:
    """Search YouTube videos and return results with direct URLs.

    Args:
        query: Search query (e.g. "Final Fantasy XIV gameplay").
        max_results: Number of results to return (1-10). Defaults to 5.

    Returns:
        A list of video results, each containing title, channel, url,
        published_at, and description.
    """
    api_key = YOUTUBE_API_KEY or os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        return [{"error": "YOUTUBE_API_KEY not configured in environment variables."}]

    if max_results < 1:
        max_results = 1
    elif max_results > 10:
        max_results = 10

    try:
        youtube = build("youtube", "v3", developerKey=api_key)

        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=max_results,
            order="relevance",
        )
        response = request.execute()

        results = []
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            results.append(
                {
                    "title": snippet["title"],
                    "channel": snippet["channelTitle"],
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "published_at": snippet["publishedAt"],
                    "description": snippet["description"][:200],
                }
            )

        if not results:
            return [{"message": f"No videos found for: {query}"}]

        return results

    except Exception as e:
        return [{"error": f"YouTube API error: {str(e)}"}]
