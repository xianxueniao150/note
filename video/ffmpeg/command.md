## ffmpeg
```sh
# 查看视频文件的元信息
ffmpeg -hide_banner -i a.mp4 

# mp4 转 webm 的(内部的编码格式不变)
ffmpeg -i input.mp4 -c copy output.webm

# 转换编码格式
ffmpeg -i [input.file] -c:v libx265 output.mp4

# 裁剪
$ ffmpeg -ss [start] -i [input] -t [duration] -c copy [output]
$ ffmpeg -ss [start] -i [input] -to [end] -c copy [output]


$ ffmpeg \
[全局参数] \
[输入文件参数] \
-i [输入文件] \
[输出文件参数] \
[输出文件]

-c copy：直接复制，不经过重新编码（这样比较快）
-c:v：指定视频编码器
-c:a：指定音频编码器
```

### mp4 to hls
```sh
$ ffmpeg -i filename.mp4 -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls filename.m3u8

-hls_time n: 设置每片的长度，默认值为2。单位为秒 
-hls_list_size n:设置播放列表保存的最多条目，设置为0会保存有所片信息，默认值为5 
-hls_start_number n:设置播放列表中sequence number的值为number，默认值为0 
```


## ffprobe
https://ffmpeg.org/ffprobe-all.html
```sh
# 查看stream
./ffprobe -v error -show_streams -of json a.mp4 
# 输出关键帧的秒数
./ffprobe -v error -select_streams 0 -show_frames -skip_frame nokey -show_entries frame=pts_time -of csv a.mp4


过滤选项
-select_streams xxx 指定stream
-skip_frame xxx 丢弃指定帧
Possible values:
	‘nokey’: Discard all frames excepts keyframes.
	‘nointra’: Discard all frames except I frames.


输出选项
-show_frames 输出每一帧或者字幕
-show_entries section_entries 只输出指定字段
```
