from django.shortcuts import render 
from django.http import HttpResponse ,HttpRequest
from django.views.generic import ListView ,DetailView,CreateView ,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from  . import models
#create data 

# Create your views here.
def home(request:HttpRequest):
    recipes= models.Recipe.objects.all()
    context ={
        'recipes':recipes
    }
    return render(request , "recipes/home.html" ,context )
   
class RecipeListView(ListView):
    model =models.Recipe
    template_name= "recipes/home.html"
    context_object_name= 'recipes'

#  Detail View
class RecipeDetailView(DetailView):
    model= models.Recipe
    template_name= "recipes/recipes-detail.html"
#  Create View
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model =models.Recipe
    fields= ['title', 'description']
    template_name= "recipes/recipes-form.html"

    def form_valid(self ,form):
        form.instance.author =self.request.user
        return super().form_valid(form)

#Update View

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model =models.Recipe
    fields= ['title', 'description']
    template_name= "recipes/recipes-form.html"

    def test_func(self):
        recipe =self.get_object()
        return self.request.user==recipe.author

    def form_valid(self ,form):
        form.instance.author =self.request.user
        return super().form_valid(form)




#Delete View
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model =models.Recipe
    success_url= reverse_lazy('recipes-home')
    template_name= "recipes/recipes_confirm_delete.html"

    def test_func(self):
        recipe =self.get_object()
        return self.request.user==recipe.author



def about(request:HttpRequest):
    return render(request ,"recipes/recipes-about.html", {'title':'about us '})