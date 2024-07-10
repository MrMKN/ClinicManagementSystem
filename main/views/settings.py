from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .utils import login_required
from ..models import *
import datetime, json, logging

logger = logging.getLogger(__name__)

# ================================================================ (HOSPITAL CHARGE SETTINGS) ======================================================= #


# hospital charges
@login_required
def charge(request):  
    context = dict(
        charges = Charge.objects.all()[::-1],
        type = ChargeType.objects.all(),
        category = ChargeCategory.objects.all(),
        unit = UnitType.objects.all(),
        tax = TaxCategory.objects.all(),
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/charges/charge.html', context)


@login_required
def charge_category(request): 
    context = dict(
        charges = ChargeCategory.objects.all()[::-1],
        type = ChargeType.objects.all(),
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/charges/category.html', context)


@login_required
def charge_tax(request):  
    context = dict(
        charges = TaxCategory.objects.all()[::-1],
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/charges/tax.html', context)

@login_required
def charge_type(request):   
    context = dict(
        charges = ChargeType.objects.all()[::-1],
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/charges/type.html', context)


@login_required
def charge_unit(request):
    context = dict(
        charges = UnitType.objects.all()[::-1],
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/charges/unit.html', context)



# add hospital charges
@login_required
def add_charge(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        type = ChargeType.objects.filter(id=int(request.POST.get('type'))).first()
        category = ChargeCategory.objects.filter(id=int(request.POST.get('category'))).first()
        unit = UnitType.objects.filter(id=int(request.POST.get('unit'))).first()
        tax = TaxCategory.objects.filter(id=int(request.POST.get('tax'))).first()
        
        data = Charge(name=name, ChargeType=type, ChargeCategory=category, TaxCategory=tax, UnitType=unit, charge=amount, description=description)
        if not Charge.objects.filter(name=name, ChargeType=type, ChargeCategory=category, TaxCategory=tax, UnitType=unit, charge=amount, description=description).exists():
            data.save()

    return redirect("charge")


@login_required
def add_charge_category(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        type = ChargeType.objects.filter(id=int(request.POST.get('type'))).first()
        
        data = ChargeCategory(name=name, ChargeType=type, description=description)
        if not ChargeCategory.objects.filter(name=name, ChargeType=type, description=description).exists():
            data.save()

    return redirect("charge_category")


@login_required
def add_charge_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Appointment = True if request.POST.get('Appointment') == "on" else False
        OPD = True if request.POST.get('OPD') == "on" else False

        data = ChargeType(name=name, Appointment=Appointment, OPD=OPD)
        if not ChargeType.objects.filter(name=name, Appointment=Appointment, OPD=OPD).exists():
            data.save()

    return redirect("charge_type")


@login_required
def add_charge_tax(request):  
    if request.method == 'POST':
        name = request.POST.get('name')
        percentage = request.POST.get('percentage')

        data = TaxCategory(name=name, percentage=percentage)
        if not TaxCategory.objects.filter(name=name, percentage=percentage).exists():
            data.save()

    return redirect("charge_tax")


@login_required
def add_charge_unit(request): 
    if request.method == 'POST':
        name = request.POST.get('name')
       
        data = UnitType(name=name)
        if not UnitType.objects.filter(name=name).exists():
            data.save()

    return redirect("charge_unit")



# edit hospital charges
@login_required
def edit_charge(request, id):   
    dta = Charge.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('charge')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        type = ChargeType.objects.filter(id=int(request.POST.get('type'))).first()
        category = ChargeCategory.objects.filter(id=int(request.POST.get('category'))).first()
        unit = UnitType.objects.filter(id=int(request.POST.get('unit'))).first()
        tax = TaxCategory.objects.filter(id=int(request.POST.get('tax'))).first()
        
        data = Charge(id=int(id), name=name, ChargeType=type, ChargeCategory=category, TaxCategory=tax, UnitType=unit, charge=amount, description=description, added_date_time=dta.added_date_time)
        data.save()

    return redirect("charge")


@login_required
def edit_charge_category(request, id):  
    dta = ChargeCategory.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('charge_category')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        type = ChargeType.objects.filter(id=int(request.POST.get('type'))).first()
        
        data = ChargeCategory(id=int(id), name=name, ChargeType=type, description=description, added_date_time=dta.added_date_time)
        data.save()

    return redirect("charge_category")


@login_required
def edit_charge_tax(request, id):  
    dta = TaxCategory.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('charge_tax')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        percentage = request.POST.get('percentage')

        data = TaxCategory(id=int(id), name=name, percentage=percentage, added_date_time=dta.added_date_time)
        data.save()

    return redirect("charge_tax")


@login_required
def edit_charge_type(request, id):  
    dta = ChargeType.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('charge_type')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        Appointment = True if request.POST.get('Appointment') == "on" else False
        OPD = True if request.POST.get('OPD') == "on" else False

        data = ChargeType(id=int(id), name=name, Appointment=Appointment, OPD=OPD, added_date_time=dta.added_date_time)
        data.save()

    return redirect("charge_type")


@login_required
def edit_charge_unit(request, id):  
    dta = UnitType.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('charge_unit')
    
    if request.method == 'POST':
        name = request.POST.get('name')
       
        data = UnitType(id=int(id), name=name, added_date_time=dta.added_date_time)
        data.save()

    return redirect("charge_unit")


# delete hospital charges
@login_required
def delete_charges(request, id, data_name, path):   
    if request.method == 'POST':
        data = eval(data_name).objects.filter(id=int(id)).first()
        if data:
            data.delete()
        
    return redirect(path)



# ================================================================ (STAFF SETTINGS) ======================================================= #


# staff settings
@login_required
def role(request):   
    context = dict(
        roles = Role.objects.all()[::-1],
        class_name = Role.__name__,
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/staff/role.html', context)


@login_required
def designation(request):
    context = dict(
        designation = Designation.objects.all()[::-1],
        class_name = Designation.__name__,
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/staff/designation.html', context)


@login_required
def department(request):  
    context = dict(
        department = Department.objects.all()[::-1],
        class_name = Department.__name__,
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/staff/department.html', context)


@login_required
def specialist(request):  
    context = dict(
        specialist = Specialist.objects.all()[::-1],
        class_name = Specialist.__name__,
        general = GeneralSetting.objects.first()
    )
    return render(request, 'settings/staff/specialist.html', context)


# add staff settings modal
@login_required
def add_role(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dashboard = True if request.POST.get('dashboard') == "on" else False
        appointment = True if request.POST.get('appointment') == "on" else False
        front_office = True if request.POST.get('front_office') == "on" else False
        staffs = True if request.POST.get('staffs') == "on" else False
        settings = True if request.POST.get('settings') == "on" else False

        data = Role(name=name, dashboard=dashboard, appointment=appointment, front_office=front_office, staffs=staffs, settings=settings)
        if not Role.objects.filter(name=name, dashboard=dashboard, appointment=appointment, front_office=front_office, staffs=staffs, settings=settings).exists():
            data.save()
    return redirect("role")


@login_required
def add_designation(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
       
        data = Designation(name=name)
        if not Designation.objects.filter(name=name).exists():
            data.save()

    return redirect("designation")


@login_required
def add_department(request):   
    if request.method == 'POST':
        name = request.POST.get('name')
       
        data = Department(name=name)
        if not Department.objects.filter(name=name).exists():
            data.save()

    return redirect("department")


@login_required
def add_specialist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
       
        data = Specialist(name=name)
        if not Specialist.objects.filter(name=name).exists():
            data.save()

    return redirect("specialist")


# edit & staff settings modal
@login_required
def edit_role(request, id): 
    dta = Role.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('role')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        dashboard = True if request.POST.get('dashboard') == "on" else False
        appointment = True if request.POST.get('appointment') == "on" else False
        front_office = True if request.POST.get('front_office') == "on" else False
        staffs = True if request.POST.get('staffs') == "on" else False
        settings = True if request.POST.get('settings') == "on" else False

        data = Role(id=int(id), name=name, dashboard=dashboard, appointment=appointment, front_office=front_office, staffs=staffs, settings=settings, added_date_time=dta.added_date_time)
        data.save()

    return redirect("role")


@login_required
def edit_staff_all(request, id, class_name): 
    dta = eval(class_name).objects.filter(id=int(id)).first()
    if not dta:
        return redirect(f'{class_name.lower()}')
    
    if request.method == 'POST':
        name = request.POST.get('name')

        data = eval(class_name)(id=int(id), name=name, added_date_time=dta.added_date_time)
        data.save()

    return redirect(f'{class_name.lower()}')


@login_required
def delete_staff_all(request, id, class_name):  
    if request.method == 'POST':
        data = eval(class_name).objects.filter(id=int(id)).first()
        if data:
            data.delete()

    return redirect(f'{class_name.lower()}')



# ===================================================== (APPOINTMENT SETTINGS) =========================================================== #

@login_required
def shift(request):
    context = dict(
        shifts = Shift.objects.all()[::-1],
        class_name = Shift.__name__,
        general = GeneralSetting.objects.first()      
    )
    return render(request, 'settings/doctor/shift.html', context)


@login_required
def add_shift(request):    
    if request.method == 'POST':
        name = request.POST.get('name')
        start = request.POST.get('start')
        end = request.POST.get('end')

        data = Shift(name=name, time_start=start, time_end=end)
        if not Shift.objects.filter(name=name, time_start=start, time_end=end).exists():
            data.save()

    return redirect("shift")


@login_required
def edit_shift(request, id):  
    dta = Shift.objects.filter(id=int(id)).first()
    if not dta:
        return redirect('shift')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        start = request.POST.get('start')
        end = request.POST.get('end')

        data = Shift(id=int(id), name=name, time_start=start, time_end=end, added_date_time=dta.added_date_time)
        data.save()

    return redirect("shift")




#add shift for doctor
@login_required
def doctor_shift(request):  
    context = dict(
        shifts = Shift.objects.all()[::-1],
        doctors = Doctor.objects.all(),
        general = GeneralSetting.objects.first()      
    )
    return render(request, 'settings/doctor/doctor_shift.html', context)


@login_required
def change_shift_for_doctor(request, doctor_id, shift_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        doctor = Doctor.objects.filter(id=doctor_id).first()      
        shift = Shift.objects.filter(id=int(shift_id)).first()

        if request.POST.get('add') == 'on':
            doctor.shift.add(shift)
            action = 'added'
        else:
            doctor.shift.remove(shift)
            action = 'removed'
            
        return JsonResponse({'status': 'success', 'action': action, 'shift_id': shift_id})
    return JsonResponse({'status': 'error'}, status=400)







