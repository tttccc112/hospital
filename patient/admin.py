from django.contrib import admin
from .models import Register,Fee,Diagnose,Prescribe,PatientBase,PatientHealth
from import_export.admin import ImportExportModelAdmin


# Register your models here.
@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    """
    D1 挂号信息
    """
    list_display = ('register_id','pid_id','doc_id',
                    'dept_id','register_date','status')  # 采用的是原本的名字
    fields =('register_id','pid',('doc_id',
            'dept_id'),'register_date','status')
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(RegisterAdmin, self).save_model(request,obj,form,change)

@admin.register(Fee)
class FeeAdmin(ImportExportModelAdmin):
    """
    D7 收费流水
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(FeeAdmin, self).save_model(request, obj, form, change)

@admin.register(Diagnose)
class DiagnoseAdmin(admin.ModelAdmin):
    """
    D8 诊断信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(DiagnoseAdmin, self).save_model(request,obj,form,change)


@admin.register(Prescribe)
class PrescribeAdmin(admin.ModelAdmin):
    """
    D10 开药记录
    """

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PrescribeAdmin, self).save_model(request,obj,form,change)

@admin.register(PatientBase)
class PatientBaseAdmin(admin.ModelAdmin):
    """
    D11 患者基本信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PatientBaseAdmin, self).save_model(request,obj,form,change)

@admin.register(PatientHealth)
class PatientHealthAdmin(admin.ModelAdmin):
    """
    患者身体信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PatientHealthAdmin, self).save_model(request,obj,form,change)
    