from django.template.loader import get_template
from django.template import Context, Library, RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.core.urlresolvers import reverse

from design_methods.forms import *
from design_methods.models import *

register = Library()

# Simple view extended from the generic list view. May be used in some way in the future
class UserList(ListView):
    model=User
    context_object_name='user_list'
    template_name='users/index.html'

# View to get user information using the generic detail view.
# May extend to support the extended user model
class UserDetails(DetailView):
    model=User
    context_object_name='current_user'
    template_name='users/profile.html'

# Simple view to process user registration
class Register(CreateView):
    form_class=UserCreationForm
    success_url='/'
    template_name='users/new.html'

# View for displaying a method
class MethodDetails(DetailView):
    model=Method
    context_object_name='method'
    template_name='methods/details.html'

# View to see all methods
class MethodList(ListView):
    model=Method
    context_object_name='method_list'
    template_name='methods/index.html'

@register.inclusion_tag('sessions/login.html', takes_context = True)
def login_form(context):
    request = context['request']
    next = request.get_absolute_uri
    return { 'next': next }

@register.inclusion_tag('sessions/login_form.html')
def test_tag():
    return {}

# View to process home page
# Includes logic for its context-sensitive content
def home(request):
    c = Context({
        'title': 'The Design Exchange',
        'form' : AuthenticationForm(),
        })
    if request.user.is_authenticated():
        c['user'] = request.user
    return render_to_response('home.html',  c, RequestContext(request))

# A view for the messaging feature
# Note that this is intended for one-to-one messaging for now
@login_required
def send_message(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MessageForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
        # TODO what if form is not valid?
            recipient = form.cleaned_data['recipient']
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            recipient = User.objects.get(username=recipient)
            if not recipient:
                return render(request, 'messages/new.html', { 'form': form })
                # TODO include error message
            else:
                # try to find the corresponding UUR first
                uur = UserToUserRelationship.objects.filter(
                    subject_user = request.user,
                    object_user  = recipient)
                if len(uur) == 0:   # if no UUR was found, make one
                    uur = UserToUserRelationship.objects.create(
                        subject_user = request.user,
                        object_user  = recipient)
                    uur.full_clean()
                else: # if UUR is found, move it out of the QuerySet
                    uur = uur[0]
                Message.objects.create(
                    users = uur,
                    title = title,
                    content = content,
                    sent_at = timezone.now())
                return redirect('/') # Redirect after POST
    else:
        form = MessageForm() # An unbound form

    return render(request, 'messages/new.html', { 'form': form })

# Method creation view
@login_required
def create_method(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MethodForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            title = form.cleaned_data['title']
            purpose = form.cleaned_data['purpose']
            procedure = form.cleaned_data['procedure']
            principles = form.cleaned_data['principles']

            # create the method
            method = Method.objects.create(
                title = title,
                purpose = purpose,
                procedure = procedure,
                principles = principles)

            # create a new UMR
            umr = UserToMethodRelationship.objects.create(
                user = request.user,
                method = method,
                is_author = True)
            return redirect(reverse('method_details', args=(method.id,)))
    else:
        form = MethodForm()
    return render(request, 'methods/new.html', { 'form': form })

# NOTE: the efficiency of the following views are questionable

# Retrieve all methods, or the user's created methods if the user is logged in
def list_methods(request):
    method_list = Method.objects.all()
    if request.user.is_authenticated():
        method_list = [ umr.method for umr in UserToMethodRelationship.objects.filter(
            user = request.user,
            is_author = True) ]
    return render(request, 'methods/index.html', { 'method_list': method_list })

# Retrieve received and sent messages
@login_required
def list_messages(request):
    received_messages = []
    [ received_messages.extend(mlist.iterator()) for mlist in
        [ uur.message_set for uur in UserToUserRelationship.objects.filter(
            object_user = request.user) ]]
    sent_messages = []
    [ sent_messages.extend(mlist.iterator()) for mlist in
        [ uur.message_set for uur in UserToUserRelationship.objects.filter(
            subject_user = request.user) ]]
    return render(request, 'messages/index.html',
        { 'received_messages': received_messages,
          'sent_messages'    : sent_messages })
