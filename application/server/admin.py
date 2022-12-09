from django.contrib import admin

from server.models import (AssignmentsInitiators, AssignmentsSources,
                           CuratorsKid, DeputyGovernor, ExcludedOrganizations,
                           Minister, Person, ReportKid)


class AssignmentsSourcesAdmin(admin.ModelAdmin):
    list_display = ('assignment_source', 'coefficient')


class CuratorsKidAdmin(admin.ModelAdmin):

    def get_dependants(self, obj):
        return obj.get_dependants()

    get_dependants.short_description = 'Список подчиненных'
    list_display = ('curator', 'get_dependants')


admin.site.register(Person)
admin.site.register(ReportKid)
admin.site.register(AssignmentsSources, AssignmentsSourcesAdmin)
admin.site.register(ExcludedOrganizations)
admin.site.register(AssignmentsInitiators)
admin.site.register(CuratorsKid, CuratorsKidAdmin)
admin.site.register(DeputyGovernor)
admin.site.register(Minister)
