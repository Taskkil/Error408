import vlc
import time



def play_video(video_path, t):
    """全屏播放视频，播放完成后退出程序"""
    player = vlc.MediaPlayer(video_path)
    player.set_fullscreen(True)
    player.play()
    
    # 等待播放完成
    while player.is_playing():
        pass
    time.sleep(t)
    player.stop()
    player.release()


if __name__ == "__main__":
    play_video("resource1.mp4", 21)