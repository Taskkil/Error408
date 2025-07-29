import pyglet
import os
import sys

def play_video_fullscreen(video_path):
    # 创建窗口并设置为全屏
    window = pyglet.window.Window(fullscreen=True)
    window.set_caption("Fullscreen Video Player")
    
    # 加载视频文件
    player = pyglet.media.Player()
    source = pyglet.media.load(video_path)
    player.queue(source)
    player.play()
    
    # 设置视频位置为窗口中心
    video_width = source.video_format.width
    video_height = source.video_format.height
    player.position = (window.width - video_width) // 2, (window.height - video_height) // 2, 0
    
    # 按ESC退出的事件处理
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            window.close()
    
    # 绘制视频帧（自动更新）
    @window.event
    def on_draw():
        window.clear()
        player.texture.blit(player.position[0], player.position[1])
    
    # 视频结束自动关闭
    @player.event
    def on_eos():
        window.close()
    
    # 开始运行
    pyglet.app.run()

if __name__ == "__main__":
    
    video_path = r"T:\python\Error408\resource1.mp4"
    
    if not os.path.exists(video_path):
        print(f"错误: 文件 '{video_path}' 不存在")
        sys.exit(1)
    
    play_video_fullscreen(video_path)