import requests
import re
def GetUserNum(request):
    search_num = '''<p class="total-text">
    共找到(.*)个用户
  </p>'''
    UserNum = re.search(search_num, request).groups()[0]
    return UserNum
def IsFans(UID):
    head={
        'Referer':'https://space.bilibili.com/'+UID+'/fans/follow',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
     }
    for page in range(1,6):
        get_url = 'https://api.bilibili.com/x/relation/followings?vmid=' + UID + '&pn=' + str(page) + '&ps=20&order=desc&jsonp=jsonp&callback=__jp5'
        follow_request = requests.get(get_url, headers=head).text
        follow_search = '''"mid":17391972'''
        follow_result = re.search(follow_search, follow_request)
        if follow_result!=None:
            return "该用户已关注UP主!"
    return "该用户关注列表前5页未找到UP主!"
def UserConfirm(request,name):
    search_confirm = '''<!----><a href="//(.*)" title="(.*)" target="_blank" class="title">(.*)</a>'''
    Url= re.search(search_confirm, request).groups()[0]
    Name = re.search(search_confirm, request).groups()[1]
    if Name!=name:
        return "查无此人"
    else:
        search_space='''space.bilibili.com/(.*)\?from=search&amp;seid=(.*)'''
        UID=re.search(search_space,Url).groups()[0]
        return IsFans(UID)
def Search(name):
    url = "https://search.bilibili.com/upuser?keyword="+name
    request = requests.get(url).text
    UserNum=GetUserNum(request)
    if UserNum=='0':
        return "查无此人"
    else:
        return UserConfirm(request,name)
if __name__=="__main__":
    print("**********英俊的沈醉 粉丝查询系统**********")
    while True:
        flag_uid=1
        name = input("请输入要查询的粉丝用户名或uid:")
        name=name.strip()
        if name=='':
            print("请勿输入空白字符!")
            continue
        result = Search(name)
        if result=="查无此人":
            for i in name:
                if re.search(i,'0123456789')==None:
                    flag_uid=0
                    break
            if flag_uid==1:
                result=IsFans(name)
        print(result)