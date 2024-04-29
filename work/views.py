from django.shortcuts import render,redirect
from django.views.generic import View
from work.form import Register ,Loginform,TaskForm
from work.models import User,Taskmodel
from django. contrib.auth import authenticate,login,logout
from django.contrib import messages
from django .utils.decorators import method_decorator



# decorator
def signin_required(fn):
    def wrapper(request,**kwargs):
        if  not request.user.is_authenticated:
            return redirect("sign_in")
        else:
            return fn(request,**kwargs)
    return wrapper


def mylogin(fn):
    def wrapper(request,**kwrgs):
        id=kwrgs.get("pk")
        obj=Taskmodel.objects.get(id=id)
        if obj.user!=request.user:
            return redirect("sign_in")
        else:
            return fn(request,**kwrgs)
    return wrapper



class Registration(View):
    def get(self, request, **kwargs):
        form = Register()
        return render(request, "Register.html", {"form": form})
    
    def post(self, request, **kwargs):
        form = Register(request.POST)
        if form.is_valid():

            # Create a new user based on form data
            User.objects.create_user(**form.cleaned_data)

            # Redirect to the login page after successful registration
            return redirect("sign_in")  
        else:
            # If form is not valid, re-render the registration form with errors
            return render(request, "Register.html", {"form": form})





# Create your views here.
class Registration(View):
    def get(self,request,**kwrgs):
        form=Register()
        return render(request,"Register.html",{"form":form})
    

    def post(self,request,**kwrgs):
        form=Register(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            form=Register()
            return render(request,"Register.html",{"form":form})
        
class Signin(View):
    def get(self,request,**kwrgs):
        form=Loginform()
        return render(request,"login.html",{"form":form})

    def post(self,request,**kwrgs):

        form=Loginform(request.POST)

        if form.is_valid():
            print(form.cleaned_data)

            # getting username and password
            u_name=form.cleaned_data.get("username")

            pwd=form.cleaned_data.get("password")
   
# checking if the username and password are valid in the table auth_user

            user_obj=authenticate(username=u_name,password=pwd)

            if user_obj:
                print("Valid credentials")
                login(request,user_obj)
                return redirect("index")
            else:
                print("Invalid credentials")
                return render(request,"login.html")
            
# for adding task
@method_decorator(signin_required,name="dispatch")
class Add_task(View):

    def get(self,request,**kwrgs):
        form=TaskForm()
        data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})
    

    def post(self,request,**kwrgs):
        form=TaskForm(request.POST)
        if form.is_valid():
            # To get the login details of user
            form.instance.user=request.user

            form.save()
            # Taskmodel.objects.create(**form.cleaned_data)
            messages.success(request,"Task added successfully")
            print(messages)
            form=TaskForm()
            data=Taskmodel.objects.filter(user=request.user).order_by('completed')
        return render(request,"index.html",{"form":form,"data":data})


          # To view added task
# class All_task(View):
#     def get(self,request,**kwrgs):
#         data=Taskmodel.objects.all() 
#         return render(request,"index.html" ,{"data":data})

@method_decorator(mylogin,name="dispatch")
@method_decorator(signin_required,name="dispatch")
class Delete_task(View):
    def get(self,request,**kwrgs):
        task_id=kwrgs.get("pk")
        Taskmodel.objects.get(id=task_id).delete()
        print("deleted sucessfully")
        return redirect("index")
    


    # to update

class Task_edit(View):
    def get(self,request,**kwrgs):
        id=kwrgs.get("pk")
        obj=Taskmodel.objects.get(id=id)
        print(obj.completed)
        if obj.completed == False:
            obj.completed = True
            print(obj.completed)
            obj.save()
        return redirect("index")
    

    # sign out
class Sign_out(View):
    def get(self,request):
        logout(request)
        return redirect("sign_in")
    

class User_del(View):
    def get(self,request,**kwrgs):
        id=kwrgs.get("pk")
        User.objects.get(id=id).delete()
        return redirect("sign_in")



# To update user details
class Update_user(View):
    def get(self,request,**kwrgs):
        id=kwrgs.get("pk")
        data=User.objects.get(id=id)
        form=Register(instance=data)
        return render(request,"Register.html",{"form":form})
    
    def post(self,request,**kwrgs):
          id=kwrgs.get("pk")
          data=User.objects.get(id=id)
          form=Register(request.POST,instance=data)
          if form.is_valid:
              form.save()
          return render(request,"Register.html",{"form":form})
