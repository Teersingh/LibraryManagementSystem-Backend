from django.shortcuts import get_object_or_404

# Create your views here.
from django.contrib.auth.models import User
from .serializer import RegisterSerializer,LoginSerializer,StudentSerialzer,BookSerializer,IssuedbookSerialzer
from .models import Student,Book,Issuedbook
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login,logout
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .permissions import IsLibrarian
class Registeruser(APIView):

    def post(self,request):


        serializer=RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({'message':'Sucessfully Regsieter'},status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Loginuser(APIView):


    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request):

        serializer=LoginSerializer(data=request.data)

        if serializer.is_valid():

            user= serializer.validated_data

            login(request,user)

            return Response({'message':'Login'})
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class Logoutuser(APIView):

    def post(self,request):

        logout(request)
        
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

# librarian can create and delete

class BookListCreateView(generics.ListCreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [IsAdminUser]
    

    

class BookRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Book.objects.all()

    serializer_class = BookSerializer


class Searchbook(generics.ListAPIView):

    queryset = Book.objects.all()

    serializer_class = BookSerializer

    filter_backends = [SearchFilter]

    search_fields = ['title']

class Bookissue(generics.ListAPIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    queryset = Issuedbook.objects.all()
    serializer_class = IssuedbookSerialzer

class IssuedbookToStudent(generics.CreateAPIView):

    queryset= Issuedbook.objects.all()
    serializer_class = IssuedbookSerialzer

    permission_classes = [permissions.IsAuthenticated,IsAdminUser]

    @transaction.atomic 
    def perform_create(self, serializer):
        
        book = serializer.validated_data['issued_book']
        student= serializer.validated_data['student']

        if book.available_copies  > 0:
            book.available_copies  -=1

            book.save()
            

            # try:

            #     student= self.request.user.student

            # except Student.DoesNotExist:
            #     raise ValidationError("Authenticated user does not have student profile")
            
            serializer.save(student=student)

        else:
            raise ValidationError("No copies available")
class StudentFineView(APIView):

    def get(self,request,pk):

        student= get_object_or_404(Student,pk=pk)

        serializer = StudentSerialzer(student)

        return Response(serializer.data,status=status.HTTP_200_OK)



class BookdetailsView(generics.ListAPIView):

    queryset= Book.objects.all()
    serializer_class= BookSerializer


