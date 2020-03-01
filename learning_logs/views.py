from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm,ContentForm

# Create your views here.
def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    total_length = len(topics)
    topic_length = {}
    # ~ topic_length['lst'] = []
    # ~ for topic in topics:
        # ~ topic_length['lst'].append(21-len(topic.text))
    
    for topic in topics:
        topic_length[topic.text] = len(topic.text)
        
    context = {'topics':topics,'tl':topic_length,'ttl':total_length}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
#    topic = Topic.objects.get(id=topic_id)
    topic = get_object_or_404(Topic,id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def edit_topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
#    topic_length = len(topic.text)    

    if topic.owner != request.user:
        raise Http404    

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic,data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/edit_topic.html',context)

@login_required
def add_content(request,topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404   

    if request.method != 'POST':
        form = ContentForm()
    else:
        form = ContentForm(data=request.POST)
        if form.is_valid():
            new_content = form.save(commit=False)
            new_content.topic = topic
            new_content.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/add_content.html',context)

@login_required    
def edit_content(request,edit_id):
    content = Entry.objects.get(id=edit_id)
    topic = content.topic
    
    if topic.owner != request.user:
        raise Http404    
    
    if request.method != 'POST':
        form = ContentForm(instance=content)
    else:
        form = ContentForm(instance=content,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic.id]))
    context = {'content':content,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_content.html',context)
    
