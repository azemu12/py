项目结构:
builder:构建请求信息代码以及工具类
static:静态文件
data_util:下载数据相关接口
douyin_api:请求相关接口
main:主程序文件
find /sdc1/mada_16t/download_1110 -type f -iname "*.mp4" -printf "%s\n" | tee >(wc -l >&2) | awk '{sum+=$1} END {print "Total:", sum/1024/1024/1024, "GB"}':统计视频数量和视频大小
