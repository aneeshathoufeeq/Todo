from work.models import Taskmodel,User
from rest_framework import serializers


class Userserializer(serializers.ModelSerializer):
    # User=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=User
        fields=['id','username','first_name','last_name','email','password']
        read_only_fields=['id']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class Taskserializer(serializers.ModelSerializer):
    class Meta:
        model=Taskmodel
        fields='__all__'
        read_only_fields=['id','created_date','user','completed']

