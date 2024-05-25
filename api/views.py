from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import Userserializer,Taskserializer
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework import authentication,permissions
from work.models import Taskmodel
from rest_framework import status

# Create your views here.
class Userregister(APIView):
    def post(self,request,*args,**kwrgs):
        serializer=Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
            # create
      
class Todoviewsetview(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def list(self,request,*args,**kwrgs):
        qs=Taskmodel.objects.all()
        serializer=Taskserializer(qs,many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    

    def create(self,request,*args,**kwrgs):
        serializer=Taskserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
             return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)


    def retrieve(self,request,*args,**kwrgs):
        id=kwrgs.get("pk")
        try:
            qs=Taskmodel.objects.get(id=id)
            serializer=Taskserializer(qs)
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        except:
            return Response({"message":"Id doesnot exist"},status=status.HTTP_404_NOT_FOUND)
        

    def update(self,request,*args,**kwrgs):
        id =kwrgs.get("pk")
        qs=Taskmodel.objects.get(id=id)
        serializer=Taskserializer(data=request.data,instance=qs)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
        

    def destroy(self,request,*args,**kwrgs):
        id=kwrgs.get('pk')
        qs=Taskmodel.objects.get(id=id)
        if qs.user==request.user:
            qs.delete()
            return Response({"message":"Deleted sucessfully"})
        else:
            return Response({"message":"invalid User"})
            # raise serializers.ValidationError("not allowed")





class Todomodelviewset(ModelViewSet):
    queryset=Taskmodel.objects.all()
    serializer_class=Taskserializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        return Taskmodel.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        instance=Taskmodel.objects.get(id=id)
        if instance.user==self.request.user:
            return instance.delete()
        
    def perform_create(self, serializer):
    
        return serializer.save(user=self.request.user)