from django.shortcuts import render , redirect
from blog.models import Post,BlogComment
from django.contrib.auth.models import User
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.
def bloghome(request):
    allPost = Post.objects.all()
    context = {'allpost':allPost}
    return render(request,"blog/bloghome.html",context)
def blogpost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post = post , parent = None)
    replies = BlogComment.objects.filter(post = post).exclude(parent = None)
    repdict = {}
    for reply in replies:
        if reply.parent.sr_no not in repdict.keys():
            repdict[reply.parent.sr_no]=[reply]
        else:
            repdict[reply.parent.sr_no].append(reply)

    context = {'post': post,'comments':comments, "repdict": repdict}
    return render(request,"blog/blogpost.html",context)
def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postsno = request.POST.get("postsno")
        post = Post.objects.get(sr_no=postsno)
        parentSno= request.POST.get('parentsno')
        if len(comment) > 0:
            if parentSno == "":
                comment=BlogComment(comment= comment, user=user, post=post)
                comment.save()
                messages.success(request, "Your comment has been posted successfully")
            else:
                parent= BlogComment.objects.get(sr_no = parentSno)
                comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
                comment.save()
                messages.success(request, "Your reply has been posted successfully")
        else:
            messages.warning(request, "Enter some text what you want to post")
        
    return redirect(f"/blog/{post.slug}")