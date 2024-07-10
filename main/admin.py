from django.contrib import admin
from .models import *

# registering models to database
admin.site.register(Theme)
admin.site.register(GeneralSetting)
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(Specialist)
admin.site.register(Shift)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Days)
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Visit)
admin.site.register(Token)

#charges
admin.site.register(UnitType)
admin.site.register(TaxCategory)
admin.site.register(ChargeType)
admin.site.register(ChargeCategory)
admin.site.register(Charge)