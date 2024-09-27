from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Student,Book,Issuedbook




class RegisterSerializer(serializers.ModelSerializer):

    class Meta:

        model= User
        fields= ('username','email','password')

        extra_fieds= {
            'password':{'write_only':True}
        }


    def create(self,validated_data):

        user=User.objects.create_user(
            username=validated_data['username'],
            email= validated_data['email'],
            password=validated_data['password']

        )

        return user
    
class LoginSerializer(serializers.Serializer):

    class Meta:

        model=User
        

    username=serializers.CharField(max_length=50)
    password= serializers.CharField(write_only=True)

    def validate(self, data):


        username=data.get('username')
        password= data.get('password')

        user=authenticate(username=username,password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid creditials')



class BookSerializer(serializers.ModelSerializer):

    class Meta:

        model =  Book
        fields =  '__all__'


class IssuedbookSerialzer(serializers.ModelSerializer):

    fine = serializers.SerializerMethodField()
    student= serializers.PrimaryKeyRelatedField(
        queryset= Student.objects.all(),
        write_only= True
    )
    student_details= serializers.SerializerMethodField(read_only=True)

    class Meta:
        
        model = Issuedbook
        fields = ['issued_book','issued_date','return_date','fine','student','student_details']

        read_only_fields = ['issued_date', 'fine','student_details']



    def get_fine(self,obj):

        return obj.calculated_fine()
    
    
    def get_student_details(self, obj):
        return {
            'id': obj.student.id,
            'username': obj.student.user.username,
            'first_name': obj.student.user.first_name,
            'last_name': obj.student.user.last_name,
        }


class StudentSerialzer(serializers.ModelSerializer):
    issued_books = IssuedbookSerialzer(many=True, read_only=True, source='issuedbook_set')
    total_fine = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['user', 'issued_books', 'total_fine']

    def get_total_fine(self, obj):
        # Calculate total fine from all issued books
        issued_books = obj.issuedbook_set.all()
        total_fine = sum(book.calculated_fine() for book in issued_books)
        return total_fine
