from django.template import Context, loader
from polls.models import Poll,Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf

def index(request):
    if request.method=='GET' :
        latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
        return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list})
    elif request.method== 'POST' :
    	newPoll=Poll(question=request.POST["poll"])
    	newPoll.save()
    	
    for key in request.POST.keys():
      if key.startswith("choice"):
      choice=Choice(poll=newPoll, choice=request.POST[key], votes=0)
      choice.save()
      
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[Poll.objects.count()-1]
	return HttpResponseRedirect('/')
    
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
                               context_instance=RequestContext(request))

def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))
        
def new(request):
	c={}
	c.update(csrf(request))
	return render_to_response('polls/new.html', c , context_instance=RequestContext(request))
        