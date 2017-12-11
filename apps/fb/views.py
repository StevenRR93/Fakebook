from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from django.db.models import Q
from django.db.models import Count
from models import *
from django.contrib import messages
from django.contrib.messages import error
from django.db.models import Max
from django.db.models import F
from itertools import chain
import time
import bcrypt

def fakebook(request):
    is_logged_in = request.session.get('is_logged_in', False)
    request.session['is_logged_in'] = is_logged_in
    if (is_logged_in == True):
        return redirect('/home')
    else:
        return render(request, 'fb/fakebook.html')

def login(request):
    if (request.method == "POST"):
        try:
            user = Users.objects.get(email = request.POST['email'])
            if (bcrypt.checkpw(request.POST['password'].encode('utf8'), user.password.encode('utf8'))):
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = request.POST['email']
                request.session['id'] = user.id
                request.session['is_logged_in'] = True
                user.is_logged_in = True
                return redirect('/home')
            else: 
                messages.error(request, 'Incorrect password.')
                return redirect('/fakebook')
        except:
            messages.error(request, 'E-mail address not found, please enter a valid e-mail.')
            return redirect('/fakebook')
    else:
        return redirect('/fakebook')
def verify (request):
    if (request.method == "POST"): 
        return redirect('/fakebook')
    else:
        return redirect('/fakebook')

def register(request):
    if (request.method == "POST"):
        errors = Users.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/fakebook')
        elif (request.POST['password'] == request.POST['confirmpw']):
            errors = Users.objects.basic_validator(request.POST)
            salt = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = Users.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = salt, gender = request.POST['gender'])
            user.is_logged_in = True
            user.save()
            return redirect('/fakebook')
            # return redirect('success/'+str(user.id))
        else:
            return redirect('/fakebook')
    else:
        return redirect('/fakebook')

def success(request, idnum):
    user = Users.objects.get(id = idnum)
    return redirect('/home')

def home(request):
    is_logged_in = request.session.get('is_logged_in', False)
    request.session['is_logged_in'] = is_logged_in
    if request.session['is_logged_in'] == False:
        messages.error(request, 'You must be signed in to do that.')
        return redirect('/fakebook')
    try:
        currentuser = Users.objects.get(id = request.session['id']) 
    except:
        currentuser = None
    try:                     
        myfriends = Users.friend1.all()
        if not myfriends.exists():
            myfriends = None
    except:
        myfriends = None
    try:
        onlinefriends = myfriends.friend1.filter(is_logged_in = True)
        if not onlinefriends.exists():
            onlinefriends = None
    except:
        onlinefriends = None
    other_users = Users.objects.exclude(id = request.session['id'] )
    posts = Post.objects.all().order_by('-created_at')
    comments = Comment.objects.all()
    return render(request, 'fb/home.html', {'myfriends' : myfriends, 'other_users' : other_users, 'currentuser' : currentuser, "posts" : posts, "comments" : comments} )

def logout(request):
    if request.session['is_logged_in'] == False:
        return redirect('/main')
    #user = Users.objects.get(id = request.session['id'])
    request.session['first_name'] = None
    request.session['last_name'] = None
    request.session['email'] = None
    request.session['id'] = None
    request.session['is_logged_in'] = False
    #user.is_logged_in = False
    return redirect('/fakebook')

def sendrequest(request):
    is_logged_in = request.session.get('is_logged_in', False)
    request.session['is_logged_in'] = is_logged_in
    if request.session['is_logged_in'] == False:
        messages.error(request, 'You must be signed in to do that.')
        return redirect('/main')
    

def add(request, idnum):
    is_logged_in = request.session.get('is_logged_in', False)
    request.session['is_logged_in'] = is_logged_in
    if request.session['is_logged_in'] == False:
        messages.error(request, 'You must be signed in to do that.')
        return redirect('/main')
    errors = Friendship.objects.basic_validator(request.session["id"], idnum)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/fakebook')
    try: 
        Users.objects.get(id = idnum)

        Friendship.objects.create(friend1_id = request.session['id'], friend2_id = idnum)
        Friendship.objects.create(friend2_id = request.session['id'], friend1_id = idnum)
    except:
        messages.error(request, "Unable to add friend :(")
        return redirect('/home')
    return redirect('/home')

def remove(request, idnum):
    is_logged_in = request.session.get('is_logged_in', False)
    request.session['is_logged_in'] = is_logged_in
    if request.session['is_logged_in'] == False:
        messages.error(request, 'You must be signed in to do that.')
        return redirect('/fakebook')
    try:
        Friendship.objects.filter(friend1_id = request.session['id'], friend2_id = idnum).delete()
        Friendship.objects.filter(friend2_id = request.session['id'], friend1_id = idnum).delete()
    except:
        messages.error(request, 'Friend not found.')
    return redirect('/home')

def friendslist(request, idnum):
    is_logged_in = request.session.get('is_logged_in', False)
    request.session['is_logged_in'] = is_logged_in
    if request.session['is_logged_in'] == False:
        messages.error(request, 'You must be signed in to do that.')
        return redirect('/fakebook')
    try:
        currentuser = Users.objects.get(id = request.session['id'])
        user = Users.objects.get(id = idnum)
        friends_list = user.friend1.all()
    except:
        messages.error(request, 'Error: redirecting.')
        return redirect('/fakebook')
    return render(request, 'fb/friends.html', { 'friends_list' : friends_list, "thisuser": user, "currentuser": currentuser})

def users(request, idnum):
    # is_logged_in = request.session.get('is_logged_in', False)
    # request.session['is_logged_in'] = is_logged_in
    # if request.session['is_logged_in'] == False:
    #     messages.error(request, 'You must be signed in to do that.')
    #     return redirect('/fakebook')
    try:
        currentuser = Users.objects.get(id = request.session['id'])
    except:
        currentuser = None
    try:
        thisuser = Users.objects.get(id = idnum)
    except:
        thisuser = None
    posts = Post.objects.filter(pstsender = thisuser)
    comments = Comment.objects.all()
    try:                            
        friends = Friendship.objects.filter(friend1_id = idnum )
        if not friends.exists():
            friends = None
    except:
        friends = None
    try:
        user = Users.objects.get(id = idnum)
    except:
        users = None
    
    return render(request, 'fb/profile.html', {'friends' : friends, 'user':user, "thisuser": thisuser, "posts": posts, "currentuser" : currentuser, "comments" : comments})

def search(request):
    #print request.POST
    #print request.GET
    searchname = request.GET.get("search")
    if (searchname == None):
        searchname = ""
    #query = request.GET["searchname"].strip()
    try:
        currentuser = Users.objects.get(id = request.session['id'])
    except:
        currentuser = None
    userlist = Users.objects.filter(Q(first_name__icontains = searchname) | Q(last_name__icontains = searchname))
    return render(request, "fb/search.html", { "userlist" : userlist, "currentuser": currentuser} )


def edit(request, idnum):
    return redirect('/update')

def update(request):
    return redirect('/home')

def message(request, idnum):
    thisuser = Users.objects.get(id = idnum)
    currentuser = Users.objects.get(id = request.session['id'])
    thread = Thread.objects.filter(user1 = currentuser).order_by("-updated_at") #thread works
    #The group by command doesn't work as intended, needs work
    #user_messages = Message.objects.annotate(max_date=Max('updated_at')).filter(created_at=F('max_date'))
    user_messages = []
    for tm in thread:
        user_messages.append(tm.message.last())
    message_list = Message.objects.filter(Q(thread__user1 = currentuser) & Q(thread__user2 = thisuser))
    if not thread.exists():
        thread = None
    if not message_list.exists():
        message_list = None
    print message_list
    print thread
    print user_messages
    #print message_list
    return render(request, "fb/message.html", {  "thisuser" : thisuser, "thread" : thread, "currentuser" : currentuser, "message_list" : message_list, "user_messages": user_messages})

def messagelist(request):
    if request.session['is_logged_in'] == False:
        messages.error(request, 'You must be signed in to do that.')
        return redirect('/fakebook')
    thisuser = Users.objects.get(id = request.session['id'])
    errors = Message.objects.basic_validator(request.POST, request.session['id'])
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/fakebook')
    errors = Thread.objects.basic_validator(request.POST, request.session['id'])
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/fakebook')
    if request.method == "POST":
        msgreceiver = Users.objects.get(id = int(request.POST.get("userval", '')))
        msg = request.POST['msg']
        try:
            thread1 = Thread.objects.get(user1 = thisuser, user2 = msgreceiver)
            thread2 = Thread.objects.get(user1 = msgreceiver, user2 = thisuser)
        except:
            thread1 = Thread.objects.create(user1 = thisuser, user2 = msgreceiver)
            thread2 = Thread.objects.create(user1 = msgreceiver, user2 = thisuser)
        message1 = Message.objects.create(msgsender = thisuser, msgreceiver = msgreceiver, msg = msg, thread = thread1)
        message1.save()
        message2 = Message.objects.create(msgsender = thisuser, msgreceiver = msgreceiver, msg = msg, thread = thread2)
        message2.save()
        # print thread.id

        return redirect('/message/' + request.POST['userval'])

def reply(request):

    thismessage = Message.objects.get(id = request.POST["msgval"])
    thisuser = Users.objects.get(id = request.session['id'])
    msgreceiver = Users.objects.get(id = int(request.POST.get("userval", '')))
    msg = request.POST['reply']

    if request.method == "POST":
        message = Message.objects.create(msgsender = thisuser, msgreceiver = msgreceiver, msg = msg, thread = thread)
        message.save()

    

    return redirect('/message/'+ request.POST['msgval'])

def post(request):
    thisuser = Users.objects.get(id = request.session['id'])
    pstreceiver = Users.objects.get(id = int(request.POST["userval"]))
    pst = request.POST['pst']
    if request.method == "POST":
        post = Post.objects.create(pstsender = thisuser, pstreceiver = pstreceiver, pst = pst)
        post.save()
    return redirect('/home')

def comment(request):
    thisuser = Users.objects.get(id = request.session['id'])
    post = Post.objects.get(id =int(request.POST["postval"]))
    if request.method == "POST":
        cmnt = request.POST['cmnt']
        comment = Comment.objects.create(cmntsender = thisuser, post = post, cmnt = cmnt )
    return redirect('/home')

def delete_comment(request, idnum):
    try:
        Comment.objects.get(id= idnum).delete
    except:
        messages.error("Can't retrieve comment")
    return redirect('/home')

def delete_message(request, idnum):
    try:
        Message.objects.get(id= idnum).delete
    except:
        messages.error("Can't retrieve message")
    return redirect('/home')

def delete_post(request, idnum):
    try:
        Post.objects.get(id= idnum).delete
    except:
        messages.error("Can't retrieve post")
    return redirect('/home')


