async def get_best_quality_video(files):
    qualities = [
        'mp4_2160',  # 4K
        'mp4_1440',  # 1440p
        'mp4_1080',  # 1080p
        'mp4_720',  # 720p
        'mp4_480',  # 480p
        'mp4_360',  # 360p
        'mp4_240',  # 240p
        'mp4_144',  # 144p
    ]

    for quality in qualities:
        if getattr(files, quality) is not None:
            return getattr(files, quality)

    return None
