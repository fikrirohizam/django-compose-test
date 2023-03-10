from django.conf import settings
from django.forms import model_to_dict
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django import template
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from rest_framework import viewsets, permissions
from .authentication import token_expire_handler, expires_in

from .serializers import HomeSerializer, CatSerializer, CatSerializer2, BreedSerializer, HumanSerializer2, UserSigninSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import authentication, permissions
from rest_framework import exceptions
from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework import routers
from rest_framework import renderers
from rest_framework.decorators import action


from .forms import HomeForm, HumanForm, BreedForm, CatForm, AllForms
from .models import Human,Home,Cat,Breed
from django.views import generic
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    signin_serializer = UserSigninSerializer(data = request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status = HTTP_400_BAD_REQUEST)


    user = authenticate(
            username = signin_serializer.data['username'],
            password = signin_serializer.data['password'] 
        )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)
        
    #TOKEN STUFF
    token, _ = Token.objects.get_or_create(user = user)
    username = signin_serializer.data['username']
    #token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)     # The implementation will be described further

    return Response({
        'user': username, 
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=HTTP_200_OK)

class SampleApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        data = {'sample_data': 123}
        return Response(data, status=HTTP_200_OK)

class RestView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        
        return Response(content)
    
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class HomeList2(generics.ListCreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class HomeDetail2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer

class CatList2(generics.ListAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

class CatDetail2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

class HumanList2(generics.ListAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer2

class HumanDetail2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Human.objects.all()
    serializer_class = HumanSerializer2

class BreedList2(generics.ListAPIView):
   
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class BreedDetail2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

# Get all registered models in catwiki   
catwiki_tables = [m._meta.db_table for c in apps.get_app_configs() for m in c.get_models() if "catwiki" in m._meta.db_table]
catwiki_tables_name = [name.replace('catwiki_','') for name in catwiki_tables]

def parent_index(request):
    return render(request,'parent_index.html')


def index(request):
    return render(request,'index.html', {'all_models':catwiki_tables_name})


class HomeHighlight(generics.GenericAPIView):
    queryset = Home.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    def get(self, request, *args, **kwargs):
        home = self.get_object()
        return Response(home.highlighted)

class HomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows home to be viewed or edited.
    """
    queryset = Home.objects.all().order_by('id')
    serializer_class = HomeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

class BreedViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows breed to be viewed or edited.
    """
    queryset = Breed.objects.all().order_by('id')
    serializer_class = BreedSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
   
class HumanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows human to be viewed or edited.
    """
    queryset = Human.objects.all().order_by('id')
    serializer_class = HumanSerializer2
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cat to be viewed or edited.
    """
    queryset = Cat.objects.all().order_by('id')
    serializer_class = CatSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



class HomeView(generic.ListView):
    template_name = 'home_list.html'
    context_object_name = 'home_list'
    model = Home

    def get_queryset(self):
        """Get all home"""
        return Home.objects.all().values
    
class HumanView(generic.ListView):
    template_name = 'human_list.html'
    context_object_name = 'human_list'
    model = Human

    def get_queryset(self):
        """Get all human"""
        return Human.objects.all().values

class CatView(generic.ListView):
    template_name = 'cat_list.html'
    context_object_name = 'cat_list'
    model = Cat

    def get_queryset(self):
        """Get all cat"""
        return Cat.objects.all().values

class BreedView(generic.ListView):
    template_name = 'breed_list.html'
    context_object_name = 'breed_list'
    model = Breed

    def get_queryset(self):
        """Get all breed"""
        return Breed.objects.all().values

class Home_DetailView(generic.DetailView):
    template_name = 'home_detail.html'
    model = Home

class Human_DetailView(generic.DetailView):
    template_name = 'human_detail.html'
    model = Human

class Cat_DetailView(generic.DetailView):
    template_name = 'cat_detail.html'
    model = Cat
    slug_url_kwarg = "cat_name"
    slug_field = "cat_name"
    

class Breed_DetailView(generic.DetailView):
    template_name = 'breed_detail.html'
    model = Breed

def create_home(request):
    if request.method == 'POST':
        form=HomeForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your data has been saved!")
            formReturn = form.save()
            return HttpResponseRedirect(reverse('home_detail', args=(formReturn.id,)))
        else:
            ctx = {'form':form}
            return render(request,'home_create.html',ctx)
    return  render(request, 'home_create.html', {
        'form': HomeForm(),
    })

def create_human(request):
    if request.method == 'POST':
        form=HumanForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your data has been saved!")
            formReturn = form.save()
            return HttpResponseRedirect(reverse('human_detail', args=(formReturn.id,)))
    return  render(request, 'human_create.html', {
        'form': HumanForm(),
    })

def create_cat(request):
    if request.method == 'POST':
        form=CatForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your data has been saved!")
            formReturn = form.save()
            return HttpResponseRedirect(reverse('cat_detail', args=(formReturn.id,)))
    return  render(request, 'cat_create.html', {
        'form': CatForm(),
    })

def create_breed(request):
    if request.method == 'POST':
        form=BreedForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your data has been saved!")
            formReturn = form.save()
            return HttpResponseRedirect(reverse('breed_detail', args=(formReturn.id,)))
    return  render(request, 'breed_create.html', {
        'form': BreedForm(),
    })

def edit_home(request, pk):
    instance = get_object_or_404(Home, id=pk)
    if request.method == 'POST': #It is better to explicitly check for method instead of the dictionary
        form = HomeForm(request.POST, instance=instance) #No need of the "or None" here
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home_detail', args=(pk,)))   
    else:
        form = HomeForm(instance=instance) #Here is the change

    return render(request, 'home_edit.html', {
        'form': form })

def edit_human(request, pk):
    instance = get_object_or_404(Human, id=pk)
    if request.method == 'POST': #It is better to explicitly check for method instead of the dictionary
        form = HumanForm(request.POST, instance=instance) #No need of the "or None" here
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('human_detail', args=(pk,)))   
    else:
        form = HumanForm(instance=instance) #Here is the change

    return render(request, 'human_edit.html', {
        'form': form })

def edit_cat(request, pk):
    instance = get_object_or_404(Cat, id=pk)
    if request.method == 'POST': #It is better to explicitly check for method instead of the dictionary
        form = CatForm(request.POST, instance=instance) #No need of the "or None" here
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cat_detail', args=(pk,)))   
    else:
        form = CatForm(instance=instance) #Here is the change

    return render(request, 'cat_edit.html', {
        'form': form })

def edit_breed(request, pk):
    instance = get_object_or_404(Breed, id=pk)
    if request.method == 'POST': #It is better to explicitly check for method instead of the dictionary
        form = BreedForm(request.POST, instance=instance) #No need of the "or None" here
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('breed_detail', args=(pk,)))   
    else:
        form = BreedForm(instance=instance) #Here is the change

    return render(request, 'home_edit.html', {
        'form': form })

class Home_DeleteView(generic.DeleteView):
    model = Home
    success_url = reverse_lazy('home_list')

class Human_DeleteView(generic.DeleteView):
    model = Human
    success_url = reverse_lazy('human_list')

class Breed_DeleteView(generic.DeleteView):
    model = Breed
    success_url = reverse_lazy('breed_list')

class Cat_DeleteView(generic.DeleteView):
    model = Cat
    success_url = reverse_lazy('cat_list')     
