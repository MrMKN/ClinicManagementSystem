from django.db import models
from solo.models import SingletonModel


class Theme(models.Model):
    name = models.CharField(max_length=30)
    nav_color = models.CharField(max_length=30, null=True, blank=True)
    nav_text_color = models.CharField(max_length=30, null=True, blank=True)
    btn_color = models.CharField(max_length=30, null=True, blank=True)
    btn_text_color = models.CharField(max_length=30, null=True, blank=True)
    body_color = models.CharField(max_length=30, null=True, blank=True)
    body_text_color = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name

class GeneralSetting(SingletonModel):
    hospital_name = models.CharField(max_length=200, null=True, blank=True)
    hospital_code = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone_number =  models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    hospital_logo = models.ImageField(upload_to='media/')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

    def __str__(self):
        return self.hospital_name



# Hospital charges
class UnitType(models.Model):
    name = models.CharField(max_length=20)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaxCategory(models.Model):
    name = models.CharField(max_length=200)
    percentage = models.IntegerField()
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChargeType(models.Model):
    name = models.CharField(max_length=200)
    Appointment = models.BooleanField(default=False)
    OPD = models.BooleanField(default=False)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChargeCategory(models.Model):
    name = models.CharField(max_length=200)
    ChargeType = models.ForeignKey(ChargeType, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Charge(models.Model):
    name = models.CharField(max_length=200)
    ChargeType = models.ForeignKey(ChargeType, on_delete=models.CASCADE)
    ChargeCategory = models.ForeignKey(ChargeCategory, on_delete=models.CASCADE)
    TaxCategory = models.ForeignKey(TaxCategory, on_delete=models.CASCADE)
    UnitType = models.ForeignKey(UnitType, on_delete=models.CASCADE)
    charge = models.IntegerField()
    description = models.CharField(max_length=200)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    added_date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Role(models.Model):
    name = models.CharField(max_length=200)
    dashboard = models.BooleanField(default=True)
    appointment = models.BooleanField(default=False)
    front_office = models.BooleanField(default=False)
    staffs = models.BooleanField(default=False) 
    settings = models.BooleanField(default=False) 
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name = models.CharField(max_length=200)
    guardian = models.CharField(max_length=200, null=True, blank=True)
    gender = models.TextField(choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bloodgroup = models.TextField(choices=[('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+')], null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=200)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Specialist(models.Model):
    name = models.CharField(max_length=200)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Shift(models.Model):
    name = models.CharField(max_length=200)
    time_start = models.TimeField()
    time_end = models.TimeField()
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Staff(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.TextField(choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    name = models.CharField(max_length=200)
    fees = models.ForeignKey(Charge, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    gender = models.TextField(choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    phone = models.IntegerField(default=0)
    shift = models.ManyToManyField(Shift, null=True, blank=True)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointed_date = models.DateField()
    appointed_time = models.TimeField()
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    status = models.TextField(choices=[('P', 'Pending'), ('A', 'Approved'), ('C', 'Cancelled')], default='P')
    message = models.TextField(blank=True, null=True)
    payment = models.TextField(choices=[('C', 'Cash'), ('U', 'UPI'), ('O', 'Other'), ('Not Paid', 'N')], default='C')
    priority = models.TextField(choices=[('N', 'Normal'), ('U', 'Urgent')], default='N')
    amount = models.IntegerField(default=0, null=True, blank=True)
    token_number = models.IntegerField()

    def __str__(self):
        return f"{self.id}, {self.patient.name} | {self.doctor.name} | {self.status}"

class Days(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    added_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doctor.name


class Visit(models.Model):
    purpose = models.CharField(max_length=500)
    name = models.CharField(max_length=200)
    related_to = models.CharField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(default=0)
    id_card = models.CharField(max_length=200, null=True, blank=True)
    added_date_time = models.DateTimeField(auto_now_add=True)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    number_of_person = models.IntegerField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name


class Token(models.Model):
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    token = models.IntegerField()

    def __str__(self):
        return f"{self.date} | {self.appointment.patient.name} | dr. {self.appointment.doctor.name}"
    
