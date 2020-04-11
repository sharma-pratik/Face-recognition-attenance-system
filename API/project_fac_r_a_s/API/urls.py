from django.urls import path
from . import views
from .Login.UserLoginView import UserLoginView
from .Admin.NewCollegeCreationView import NewCollegeCreationView
from .Admin.CollegeDeletionView import CollegeDeletionView
from .Students.StudentFacesAssignationView import StudentFacesAssignationView
from . HOD.FetchPresentStudentListView import FetchPresentStudentListView
from . HOD.MarkStudentAttendanceView import MarkStudentAttendanceView
from .HOD.StudentsCreationView import StudentsCreationView
from .Students.StudentAttendanceDetailsView import StudentAttendanceDetailsView
from .HOD.FetchSubjectsInfoView import FetchSubjectsInfoView
from .Login.UserLogoutView import UserLogoutView
from . import get_csrf_token

urlpatterns = [
    path('user/login',  UserLoginView.as_view(), name='user-login'),
    path('admin/add_college',  NewCollegeCreationView.as_view(), name='admin-add-college'),
    path('admin/delete_college',  CollegeDeletionView.as_view(), name='admin-delete-college'),
    path('student/add_faces',  StudentFacesAssignationView.as_view(), name='student-assign-images'),
    path('student/attendance_details',  StudentAttendanceDetailsView.as_view(), name='student-attendance-details'),
    path('hod/get_present_students_list',  FetchPresentStudentListView.as_view(), name='present-student-list'),
    path('hod/fetch_subjects',  FetchSubjectsInfoView.as_view(), name='fetch-subjects'),
    path('hod/mark_students_attendance',  MarkStudentAttendanceView.as_view(), name='mark-student-attendance'),
    path('hod/create_students', StudentsCreationView().as_view(), name='students-creation'),
    path('get_csrf_token', get_csrf_token.getTokenFunction , name='get-csrf-token'),
    path('user/logout', UserLogoutView.as_view() , name='user-logging-out')

]

