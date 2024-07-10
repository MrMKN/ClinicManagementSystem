from django.urls import path
from .views import main_pages, settings
from . import fetches


# main page urls
urlpatterns = [
    # dashboard 
    path('', main_pages.index, name='index'),
    path('index/', main_pages.index, name='index'),

    # login & logout
    path('login/', main_pages.login, name='login'),
    path('logout/', main_pages.logout, name='logout'),

    # appoinment & others
    path('appoinment/', main_pages.appoinment, name='appoinment'),
    path('staff/', main_pages.staff, name='staff'),
    path('view_staff', main_pages.view_staff, name="view_staff"),
    path('front_office/', main_pages.front_office, name='front_office'),
    path('doctor-wise/', main_pages.doctor_wise_view, name='doctor_wise'),
    path('patients/', main_pages.patients, name="patients"), 
]


# main moadals urls
urlpatterns += [
    # appoinment
    path('add_appoinment/', main_pages.add_appoinment, name='add_appoinment'),
    path('edit_appoinment/<int:id>/', main_pages.edit_appoinment, name='edit_appoinment'),
    path('delete_appoinment/<int:id>/', main_pages.delete_appoinment, name='delete_appoinment'),
    path('approve_appoinment/<int:id>', main_pages.approve_appoinment, name="approve_appoinment"),

    # patient
    path('add_patient', main_pages.add_patient, name='add_patient'),

    # staff
    path('add_staff/', main_pages.add_staff, name='add_staff'),
    path('edit_staff/<int:id>/', main_pages.edit_staff, name='edit_staff'),
    path('delete_staff/<int:id>/', main_pages.delete_staff, name='delete_staff'),

    # front office
    path('add_visit/', main_pages.add_visit, name="add_visit"),  
]


# settings page urls
urlpatterns += [
    # hospital charges
    path('charge', settings.charge, name='charge'),
    path('charge_category', settings.charge_category, name='charge_category'),
    path('charge_tax', settings.charge_tax, name='charge_tax'),
    path('charge_type', settings.charge_type, name='charge_type'),
    path('charge_unit', settings.charge_unit, name='charge_unit'),
    
    # staff & role
    path('role/', settings.role, name="role"),
    path('designation/', settings.designation, name="designation"),
    path('department/', settings.department, name="department"),
    path('specialist/', settings.specialist, name="specialist"),

    #doctor
    path('shift/', settings.shift, name="shift"),
    path('doctor_shift/', settings.doctor_shift, name="doctor_shift"),
    path('change_shift_for_doctor/<int:doctor_id>/<int:shift_id>/', settings.change_shift_for_doctor, name="change_shift_for_doctor"),
]



# settings modals urls
urlpatterns += [
    # add hospital charges
    path('add_charge/', settings.add_charge, name="add_charge"),
    path('add_charge_category/', settings.add_charge_category, name="add_charge_category"),
    path('add_charge_tax/', settings.add_charge_tax, name="add_charge_tax"),
    path('add_charge_type/', settings.add_charge_type, name="add_charge_type"),
    path('add_charge_unit/', settings.add_charge_unit, name="add_charge_unit"),

    # edit & delete hospital charges
    path('edit_charge/<int:id>/', settings.edit_charge, name="edit_charge"),
    path('edit_charge_category/<int:id>/', settings.edit_charge_category, name="edit_charge_category"),
    path('edit_charge_tax/<int:id>/', settings.edit_charge_tax, name="edit_charge_tax"),
    path('edit_charge_type/<int:id>/', settings.edit_charge_type, name="edit_charge_type"),
    path('edit_charge_unit/<int:id>/', settings.edit_charge_unit, name="edit_charge_unit"),
    path('delete_charges/<int:id>/<str:data_name>/<str:path>/', settings.delete_charges, name="delete_charges"),
  
    #Staff settings
    path('add_role/', settings.add_role, name="add_role"),
    path('add_designation/', settings.add_designation, name="add_designation"),
    path('add_department/', settings.add_department, name="add_department"),
    path('add_specialist/', settings.add_specialist, name="add_specialist"),

    # edit & delete staff settings
    path('edit_role/<int:id>/', settings.edit_role, name='edit_role'),
    path('edit_staff_all/<int:id>/<str:class_name>/', settings.edit_staff_all, name="edit_staff_all"),
    path('delete_staff_all/<int:id>/<str:class_name>/', settings.delete_staff_all, name="delete_staff_all"),

    # doctor settings
    path('add_shift', settings.add_shift, name="add_shift"),

    # edit doctor settings
    path('edit_shift/<int:id>/', settings.edit_shift, name='edit_shift'),
]



# fetch python function from python file to javascript
urlpatterns += [
    path('get_token/<int:id>/<str:date>/', fetches.get_token, name="get_token"),
]