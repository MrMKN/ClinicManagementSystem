from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .utils import login_required
from ..models import *
import datetime, json

login_attempt = {}


@login_required
def index(request): 
    total_income = 0
    for apmt in Appointment.objects.all():
        total_income += apmt.amount

    doctors = list(Doctor.objects.all()[::-1])
    for doctor in doctors:
        tokens = Token.objects.filter(doctor=doctor, date=datetime.date.today())
        setattr(doctor, 'tokens', len(tokens))


    context = dict(
        date = datetime.date.today(),
        general = GeneralSetting.objects.first(),
        tokens = len(Token.objects.all()),
        appoinments = len(Appointment.objects.all()),
        staffs = Staff.objects.all()[::-1],
        doctors = doctors,
        income = total_income,
        total_visitors = len(Visit.objects.all()),
    )
    
    return render(request, 'index.html', context)



def login(request):
    next_url = request.GET.get('next', '/')  # Default to home page if next parameter is not provided

    if 'user' in request.session: # checking if user is logined or not
        return redirect(next_url)

    if request.method == 'POST':
        next_url = request.POST.get('next', '/') 
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not str(email) in login_attempt.keys(): 
            login_attempt[str(email)] = 0
        user = Staff.objects.filter(email=email).exists()

        # prevent brute force attack basic
        attempt = login_attempt[str(email)]
        if int(attempt) >= 3:
            messages.warning(request, "TOO MANY ATTEMPT. TRY AGAIN LATER")    
            return redirect('login')
        
        # checking user is exist
        if not user:
            messages.warning(request, "USER DOES NOT EXIST")           
            attempt = login_attempt[str(email)]
            login_attempt[str(email)] = attempt + 1
            return redirect('login')
        
        # checking the password is correct
        elif password != (Staff.objects.get(email=email)).password:
            messages.warning(request, 'INCORRECT PASSWORD')      
            attempt = login_attempt[str(email)]
            login_attempt[str(email)] = attempt + 1
            return redirect('login')

        # after succussfully logined
        else:
            user = Staff.objects.get(email=email)
            request.session['user'] = user.email
            return redirect(next_url)

    return render(request, 'login.html', {'next': next_url})



def logout(request):
    try:
        del request.session['user']
    except: pass
    return HttpResponseRedirect('/')


@login_required
def patients(request):
    patients = Patient.objects.all()[::-1]
    if request.method == 'POST':
        name = request.POST.get("name")
        patients = Patient.objects.filter(name__startswith=name)

    context = dict(
        patients = patients,
        general = GeneralSetting.objects.first()
    )

    return render(request, 'Patients.html', context)


@login_required
def appoinment(request):
    context = dict(
        patients =  Patient.objects.all(),
        doctors = Doctor.objects.all(),
        appoinments = Appointment.objects.all()[::-1],
        shift = Shift.objects.all(),
        general = GeneralSetting.objects.first()
    )

    return render(request, 'Appointment.html', context)


@login_required
def add_appoinment(request):
    if request.method == 'POST':
        patient = Patient.objects.filter(id=int(request.POST.get('patient'))).first()
        doctor = Doctor.objects.filter(id=int(request.POST.get('doctor'))).first()
        appointed_date = request.POST.get('datetime').split('T', 1)[0]
        appointed_time = request.POST.get('datetime').split('T', 1)[1]
        shift = Shift.objects.filter(id=int(request.POST.get('shift'))).first()
        status = request.POST.get('status')
        message = request.POST.get('message')
        payment = request.POST.get('payment')
        priority = request.POST.get('priority')
        amount = request.POST.get('amount')
        token_number = request.POST.get('token')
        added_date = timezone.now()
        
        data = Appointment(patient=patient, doctor=doctor, appointed_date=appointed_date, appointed_time=appointed_time, added_date=added_date, shift=shift, status=status, message=message, payment=payment, priority=priority, amount=amount, token_number=token_number)
        if not Appointment.objects.filter(patient=patient, doctor=doctor, appointed_date=appointed_date, shift=shift, status=status, message=message, payment=payment, priority=priority).exists():     
            data.save()
            apmnt = Appointment.objects.filter(id=int(data.id)).first()
            token = Token.objects.all()  
            date = str(appointed_date)
            if not Token.objects.filter(date=date, appointment=apmnt, doctor=doctor).exists():
                token_data = Token(date=date, appointment=apmnt, doctor=doctor, token=token_number)
                token_data.save()
    return redirect('appoinment')


@login_required
def edit_appoinment(request, id):
    apmnt = Appointment.objects.filter(id=int(id)).first()
    if not apmnt:
        return redirect('appoinment')
    
    if request.method == 'POST':
        patient = Patient.objects.filter(id=int(request.POST.get('patient'))).first()
        doctor = Doctor.objects.filter(id=int(request.POST.get('doctor'))).first()
        appointed_date = request.POST.get('datetime').split('T', 1)[0]
        appointed_time = request.POST.get('datetime').split('T', 1)[1]
        shift = Shift.objects.filter(doctor=doctor).first()
        status = request.POST.get('status')
        message = request.POST.get('message')
        payment = request.POST.get('payment')
        priority = request.POST.get('priority')
        data = Appointment(
            id=int(id),
            patient=patient if patient else apmnt.patient, 
            doctor=doctor if doctor else apmnt.doctor, 
            appointed_date=appointed_date if appointed_date else apmnt.appointed_date, 
            appointed_time=appointed_time if appointed_time else apmnt.appointed_time,
            added_date=apmnt.added_date,
            shift=shift if shift else apmnt.shift, 
            status=status if status else apmnt.status, 
            message=message if message else apmnt.message, 
            payment=payment if payment else apmnt.payment, 
            priority=priority if priority else apmnt.priority,
            amount=apmnt.amount,
            token_number=apmnt.token_number,
        )  
        data.save()
    return redirect('appoinment')


@login_required
def delete_appoinment(request, id):
    if request.method == 'POST':
        apmnt = Appointment.objects.filter(id=int(id)).first()
        if apmnt:
            apmnt.delete()
            return redirect('appoinment')
        
    return redirect('appoinment')


@login_required
def approve_appoinment(request, id):
    apmnt = Appointment.objects.filter(id=int(id)).first()
    if not apmnt:
        return redirect('appoinment')
    
    if request.method == 'POST':
        apmnt.status = "A"
        apmnt.amount = apmnt.doctor.fees.charge
        apmnt.payment = 'C'
        apmnt.save()
    return redirect('appoinment')


@login_required
def add_patient(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        guardian = request.POST.get('guardian')
        gender = request.POST.get('gender')
        age = int(request.POST.get('age'))
        bloodgroup = request.POST.get('bloodgroup')
        phone = int(request.POST.get('phone'))
        address = request.POST.get('address')

        data = Patient(name=name, guardian=guardian, gender=gender, age=age, bloodgroup=bloodgroup, phone=phone, address=address)
        if not Patient.objects.filter(name=name, guardian=guardian, gender=gender, age=age, bloodgroup=bloodgroup, phone=phone, address=address).exists():
            data.save()

    return redirect('appoinment')


@login_required
def staff(request):
    context = dict(
        staffs = Staff.objects.all()[::-1],
        role = Role.objects.all(),
        designation = Designation.objects.all(),
        department = Department.objects.all(),
        specialist = Specialist.objects.all(),
        general = GeneralSetting.objects.first()
    )
    if request.method == 'POST':
        role = Role.objects.get(id=int(request.POST.get('role')))
        staffs = Staff.objects.filter(role=role)[::-1]
        context['staffs'] = staffs
        
    return render(request, 'staff.html', context)



@login_required
def view_staff(request):
    context = dict(
        staffs = Staff.objects.all()[::-1],
        role = Role.objects.all(),
        designation = Designation.objects.all(),
        department = Department.objects.all(),
        specialist = Specialist.objects.all(),
        general = GeneralSetting.objects.first()
    )
    return render(request, 'view_staff.html', context)


@login_required
def add_staff(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if Staff.objects.filter(email=email).exists():
            messages.warning(request, f"!Email Alredy Exist")
            return HttpResponseRedirect(request.path) 


        role = Role.objects.filter(id=int(request.POST.get('role'))).first()
        designation = Designation.objects.filter(id=int(request.POST.get('designation'))).first()
        department = Department.objects.filter(id=int(request.POST.get('department'))).first()
        specialist = Specialist.objects.filter(id=int(request.POST.get('specialist'))).first()
        gender = request.POST.get('gender')

        if role == Role.objects.filter(name="doctor").first():
            doctor_data = Doctor(name=name, phone=phone, designation=designation, department=department, specialist=specialist, gender=gender)
            if not Doctor.objects.filter(name=name, phone=phone, designation=designation, department=department, specialist=specialist, gender=gender).exists():
                doctor_data.save()

        data = Staff(name=name, email=email, password=password, role=role, phone=phone, designation=designation, department=department, specialist=specialist, gender=gender)
        if not Staff.objects.filter(name=name, email=email, password=password, role=role, phone=phone, designation=designation, department=department, specialist=specialist, gender=gender).exists():
            data.save()

    return redirect('staff')


@login_required
def edit_staff(request, id):
    staf = Staff.objects.filter(id=int(id)).first()
    if not staf:
        return redirect('staff')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        role = Role.objects.filter(id=int(request.POST.get('role'))).first()
        designation = Designation.objects.filter(id=int(request.POST.get('designation'))).first()
        department = Department.objects.filter(id=int(request.POST.get('department'))).first()
        specialist = Specialist.objects.filter(id=int(request.POST.get('specialist'))).first()
        gender = request.POST.get('gender')

        data = Staff(
            id=int(id), 
            name=name, 
            email=email,
            password=password,
            role=role,
            phone=phone, 
            designation=designation, 
            department=department, 
            specialist=specialist, 
            gender=gender,
            added_date_time=staf.added_date_time
        )
        data.save()
    return redirect('staff')


@login_required
def delete_staff(request, id):
    if request.method == 'POST':
        staf = Staff.objects.filter(id=int(id)).first()
        if staf:
            staf.delete()
            return redirect('staff')
        
    return redirect('staff')


@login_required
def front_office(request):
    context = dict(
        visits = Visit.objects.all()[::-1],
        general = GeneralSetting.objects.first()
    )
    return render(request, 'front_office.html', context)


@login_required
def add_visit(request):
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        id_card = request.POST.get('id_card')
        note = request.POST.get('note')

        data = Visit(purpose=purpose, name=name, phone=phone, id_card=id_card, note=note)
        if not Visit.objects.filter(purpose=purpose, name=name, phone=phone, id_card=id_card, note=note).exists():
            data.save()

    return redirect('front_office')


@login_required
def doctor_wise_view(request):
    context = dict(
        doctors = Doctor.objects.all()
    )
    if request.method == 'POST':
        doctor = Doctor.objects.filter(id=int(request.POST.get('doctor'))).first()
        date = request.POST.get('date')

        context = dict(
            doctors = Doctor.objects.all(), 
            appoinments = Appointment.objects.filter(doctor=doctor, appointed_date=date) 
        )
    
    return render(request, 'doc_wise.html', context)




