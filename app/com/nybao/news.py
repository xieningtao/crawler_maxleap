import json, requests
import time

def getToutiaoNews():
    url="http://c.3g.163.com/recommend/getSubDocPic?tid=T1348647909107&from=toutiao&offset=0&size=10&fn=4&prog=LMA1&passport=xt3aXUI%2F0vKeSBsgPsGx6%2F%2BVl9Iv%2BZonLeLmSMxhclRbSaGBZSsXSVQ7leyYqOgLrqJv2nCCD2QqQsfBWgSZWQ%3D%3D&devId=TN7nkeuf4NIS6%2FhflY3NEA%3D%3D&lat=d5JPmRoeCiDYCTXH9OQy4w%3D%3D&lon=lD7KfiP%2Bz5xD0wz7zZqB9A%3D%3D&version=17.1&net=wifi&ts=1478174409&sign=fUtM1OtsZKU4DT0HVA69pfdCsC2OM4ata14nFxytyb148ErR02zJ6%2FKXOnxX046I&encryption=1&canal=miliao_news&mac=Vs3jgAx3MGdwkSWIle2S%2B7XXhQnPCVyraDgInk6Dmbk%3D"
    resp = requests.get(url=url)
    #print resp.text
    data = json.loads(resp.text)
    newsReslult={}
    detailContent={}
    detailResult={}
    for key in data.keys():
        dataLenth=len(data[key])
        print "total size: "+str(dataLenth)
        for i in range(1,dataLenth):
            print "curIndex: "+str(i)
            content={}
            newsCategory = []
            #print "title: "+data[key][i]["title"]
            content["title"]=data[key][i]["title"];
            
            #print "recSource: "+data[key][i]["recSource"]
            content["label"]=data[key][i]["recSource"];
            content["imageUrl"]=data[key][i]["imgsrc"]
            content["id"]=data[key][i]["id"]
            detail=getNewsDetail(content["id"])
            #print "body: "+detail
            if(len(detail)!=0):

                newsCategory.append(content)
                detailContent["content"]=detail
                detailContent["title"]=content["title"]
                finalContent={}
                finalContent["detailConent"]=detailContent
                finalContent["newsId"]=content["id"]
                finalContentArray=[]
                finalContentArray.append(finalContent)
                detailResult["results"]=finalContentArray
                uploadNewsDetail(json.dumps(detailResult,ensure_ascii=False))
                print "detailResult: "+json.dumps(detailResult,ensure_ascii=False)
                newsReslult["results"] = newsCategory
                uploadNewsOutline(json.dumps(newsReslult, ensure_ascii=False))
                print "result: " + json.dumps(newsReslult, ensure_ascii=False)
            else:
                print "body is illegal,id: "+content["id"]

    
def getNewsDetail(newsId):
    url="http://c.m.163.com/nc/article/"+newsId+"/full.html"
    resp=doCommanHttpRequest(url);
    print "text: "+resp.text
    try:
        detailData = json.loads(resp.text)
    except ValueError, e:
        print "exception: "+str(e)
        return ""
    
    return detailData[newsId]["body"]


def uploadNewsOutline(newsOutline):
    result = doMaxleapHttpRequest("saveNewsList", json.dumps({"content": newsOutline}))
    print result

def uploadNewsDetail(newsDetail):
    result=doMaxleapHttpRequest("saveNewsDetail",json.dumps({"content": newsDetail}))
    print result

def doCommanHttpRequest(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
    resp = requests.get(url=url, headers=headers)
    return resp
def doMaxleapHttpRequest(fuctionName,myData):
    url = "https://api.maxleap.cn/2.0/functions/"+fuctionName
    headers = {
        "X-ML-AppId": "57f9edc887d4a7e337b8c231",
        "X-ML-APIKey": "MmNsUDJONjlNc2xwNzEtbVY3RE5KUQ",
        "Content-Type": "application/json"
    }
    resp = requests.post(url=url, data=myData, headers=headers)
    return resp.text

if __name__ == "__main__":
    getToutiaoNews()
    # uploadNewsDetail()
    # uploadNewsOutline()
    # getNewsDetail("BSB01PH80515955G")