from moviepy.editor import *

cliplist = []
ic = ImageClip("PLOTS/world16-35650ya.png").set_duration(3)
cliplist.append(ic)
video = concatenate(cliplist, method="compose")
video.write_videofile("PLOTS/test.mp4", fps=24)
