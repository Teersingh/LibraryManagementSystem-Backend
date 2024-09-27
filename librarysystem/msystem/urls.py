from django.urls import path
from .views import Registeruser,Loginuser,BookListCreateView,BookRetriveUpdateDestroyView
from . import views
urlpatterns = [
    path('',Loginuser.as_view(),name='login'),
    path('login/',Loginuser.as_view(),name='login'),
    path('logout/',views.Logoutuser.as_view(),name='logout'),
    path('register/',Registeruser.as_view(),name='register'),
    path('books/',BookListCreateView.as_view(),name='book'),
    path('books/<int:pk>/update/',BookRetriveUpdateDestroyView.as_view(),name='bookupdate'),
    path('book/',views.Searchbook.as_view()),
    path('issuedbook/',views.IssuedbookToStudent.as_view(),name='issued-book'),
    path('student-fine/<int:pk>/',views.StudentFineView.as_view(),name='student-fine'),
    path('book-details/',views.BookdetailsView.as_view(),name='book-details')

]
