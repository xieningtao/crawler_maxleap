import json, requests
import news



def getVideos():
    url="http://c.m.163.com/recommend/getChanListNews?channel=T1457068979049&size=20&offset=0&fn=5&passport=&devId=TN7nkeuf4NIS6%2FhflY3NEA%3D%3D&lat=2jNdUEMwL34Odq1vtH2fCA%3D%3D&lon=uh%2B1CS5jtkS4BvTJOLRLqA%3D%3D&version=17.1&net=wifi&ts=1478414484&sign=FiipIH08lBPuFBEzWBp8o1cfMj%2Bj2wOX4oP0mVSjA6948ErR02zJ6%2FKXOnxX046I&encryption=1&canal=miliao_news&mac=Vs3jgAx3MGdwkSWIle2S%2B7XXhQnPCVyraDgInk6Dmbk%3D"
    resp = news.doCommanHttpRequest(url)
    print resp.text
    data = json.loads(resp.text)
    videos = {}
    for key in data.keys():
        dataLenth = len(data[key])
        print "total size: " + str(dataLenth)
        content={}
        for i in range(0, dataLenth):
            content["videoCover"] = data[key][i]["cover"];
            content["videoUrl"] = data[key][i]["mp4_url"];
            content["videoTitle"] = data[key][i]["title"];
            content["videoDescription"] = data[key][i]["topicDesc"];
            content["videoLabel"] = data[key][i]["videosource"];
            content["videoCount"] = data[key][i]["playCount"];
            uploadVideo(json.dumps(content,ensure_ascii=False))
            print "videoContent: "+json.dumps(content,ensure_ascii=False)


def uploadVideo(video):
    resp=news.doMaxleapHttpRequest("saveVideos",json.dumps({"content": video}))
    print resp
if __name__ == "__main__":
    getVideos()

