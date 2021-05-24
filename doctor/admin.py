from django.contrib import admin
from .models import Remark,Department,Medicine,CheckItem,DoctorBase,Check,CheckDetail,Roster
# Register your models here.

@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    """
    D2 评价信息表
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(RemarkAdmin, self).save_model(request,obj,form,change)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    D3 部门表
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(DepartmentAdmin, self).save_model(request,obj,form,change)

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    D4 药品价格信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(MedicineAdmin, self).save_model(request,obj,form,change)


@admin.register(CheckItem)
class CheckItemAdmin(admin.ModelAdmin):
    """
    D5 检查项目信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CheckItemAdmin, self).save_model(request,obj,form,change)

@admin.register(DoctorBase)
class DoctorBaseAdmin(admin.ModelAdmin):
    """
    D6 医生基本信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(DoctorBaseAdmin, self).save_model(request,obj,form,change)

@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    """
    D9 检查信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CheckAdmin, self).save_model(request,obj,form,change)

@admin.register(CheckDetail)
class CheckDetailAdmin(admin.ModelAdmin):
    """
    D12 检查相关信息
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CheckDetailAdmin, self).save_model(request,obj,form,change)

@admin.register(Roster)
class RosterAdmin(admin.ModelAdmin):
    """
    D14 排班表
    """
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(RosterAdmin, self).save_model(request,obj,form,change)