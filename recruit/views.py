from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Recruit,Picture,Comment
from django.http import JsonResponse
from django.conf import settings
import simplejson
from django.core.cache import cache
#注意导入这个应用的时候
from user.models import imageprofile,user_profile_graduate,user_profile_stu,user_profile_company

#上传帖子基本信息
@csrf_exempt
def uploadpost(request):
    response={}
    if(request.method=="POST"):
        req=simplejson.loads(request.body)
        sessionid=req["sessionid"]
        dic = cache.get(sessionid)
        if dic is None:
            return JsonResponse({"msg":"expire"})
        username=dic["username"]
        title=req["title"]
        content=req["content"]
        imgurls=req["imgurls"]
        companylink=req["companylink"]
        try:
            user=User.objects.get(username=username)
            post=Recruit(user=user,title=title,content=content,like_count=0,companylink=companylink)
            post.save()
            for i in range(len(imgurls)):
                img=Picture(imgurl=imgurls[i],post=post)
                img.save()
            response["msg"]="true"
            response["post_id"]=post.id
            response["post_time"]=post.created_time
        except Exception as e:
            response["msg"]=e
            print(e)
            return JsonResponse(response)
        return JsonResponse(response)

#发布评论
@csrf_exempt
def uploadcomment(request):
    if(request.method=="POST"):
        response = {"msg":"true"}
        req=simplejson.loads(request.body)
        to_which_post=Recruit.objects.get(id=req["postid"])
        to_which_user=None
        try:
            touserid=req.get("touserid",None)
            if touserid is not None:
                # 回复评论的id
                to_which_user = User.objects.get(id=req["receiverid"])
            user=User.objects.get(id=req["senderid"])
            content=req["content"]
            comment=Comment(user=user,content=content,to_which_user=to_which_user,to_which_post=to_which_post)
            comment.save()
        except Exception as e:
            response["msg"]="false"
        return JsonResponse(response)

@csrf_exempt
#获取所有帖子的信息
def getpost(request):
    if(request.method=="POST"):
        response={}
        posts=list(Recruit.objects.all().order_by("-created_time"))
        i=1
        response["post"]=[]
        for post in posts:
           postname="post"+str(i)
           j = 1
           i=i+1
           postins={}
           postins["content"]=post.content
           postins["postid"] = post.id
           postins["userid_p"] =post.user.id
           postins["like_count"] = post.like_count
           postins["created_time"]=post.created_time
           postins["title"]=post.title
           postins["companylink"]=post.companylink
           #获取发布者的昵称

           user=User.objects.get(id=post.user.id)
           stu_profile = list(user_profile_stu.objects.filter(user=user))
           c_profile = list(user_profile_company.objects.filter(user=user))
           g_profile = list(user_profile_graduate.objects.filter(user=user))
           if len(stu_profile) > 0:
               postins["postername"] = stu_profile[0].name
           if len(c_profile) > 0:
               postins["postername"] = c_profile[0].name
           if len(g_profile) > 0:
               postins["postername"] = g_profile[0].name
           #获取发布者的头像
           try:
               user = User.objects.get(id=post.user.id)
           except Exception as e:
               print(e)
           img=list(imageprofile.objects.filter(user=user))
           if len(img)>0:
               postins["userimg"] = img[0].imgurl
           imgs=Picture.objects.filter(post=post)
           arr_img=[]
           for k in range(len(imgs)):
               arr_img.append(imgs[k].imgurl)
           postins["imgurls"]=arr_img
           response["post"].append(postins)
        return JsonResponse(response)

#获取帖子的评论
@csrf_exempt
def getpostcomment(request):
    response={}
    response["msg"]="true"
    if request.method=="POST":
        req=simplejson.loads(request.body)
        postid=req["postid"]
        post=Recruit.objects.get(id=postid)
        comments=list(Comment.objects.filter(to_which_post=post).order_by("created_time"))
        response["comments"]=[]
        for comment in comments:
            com={}
            com["content"]=comment.content
            com["sendername"]=""
            com["senderimg"] = ""
            com["receivername"] = ""
            com["receiverimg"] = ""
            #拿到发送者的姓名和头像
            user = User.objects.get(id=comment.user.id)
            stu_profile = list(user_profile_stu.objects.filter(user=user))
            c_profile = list(user_profile_company.objects.filter(user=user))
            g_profile = list(user_profile_graduate.objects.filter(user=user))
            if len(stu_profile)>0:
                com["sendername"] = stu_profile[0].name
            if len(c_profile) > 0:
                com["sendername"] = c_profile[0].name
            if len(g_profile) > 0:
                com["sendername"] = g_profile[0].name
            img=list(imageprofile.objects.filter(user=user))
            if len(img)>0:
                com["senderimg"]=img[0].imgurl

            #拿到接受者的姓名和头像
            user = User.objects.get(id=comment.user.id)
            stu_profile = list(user_profile_stu.objects.filter(user=user))
            c_profile = list(user_profile_company.objects.filter(user=user))
            g_profile = list(user_profile_graduate.objects.filter(user=user))
            if len(stu_profile) > 0:
                com["receivername"] = stu_profile[0].name
            if len(c_profile) > 0:
                com["receivername"] = c_profile[0].name
            if len(g_profile) > 0:
                com["receivername"] = g_profile[0].name
            com["commentid"]=comment.id
            com["senderid"]=comment.user.id
            com["created_time"]=comment.created_time
            response["comments"].append(com)

        return JsonResponse(response)

#点赞
@csrf_exempt
def add_likecount(request):
    if(request.method=="POST"):
        response={}
        req=simplejson.loads(request.body)
        postid=req["post_id"]
        post_lostf=Recruit.objects.get(id=postid)
        post_lostf.like_count+=1
        post_lostf.save()
        response["msg"] = "true"
        return JsonResponse(response)









