from django.contrib.auth.models import User,Group, Permission
admin_group=Group.objects.get(name="admin user")
#all = admin_group.permissions.all()

permission_codename_list = ['add_scheduleinfo','change_scheduleinfo','delete_scheduleinfo',\
                            'add_requesttable','change_requesttable','delete_requesttable',\
                            'add_reporttable','change_reporttable','delete_reporttable',\
                            'add_resourceusagetable','change_resourceusagetable','delete_resourceusagetable',\
                            'add_resourceusagetitletable','change_resourceusagetitletable','delete_resourceusagetitletable', \
                            'add_projectinfo','change_projectinfo','delete_projectinfo', \
                            'add_totaltable','change_totaltable','delete_totaltable',\
                            'add_maintfstatustable','change_maintfstatustable','delete_maintfstatustable',\
                            'add_scheduletable','change_scheduletable','delete_scheduletable'
                            ]
print  len(permission_codename_list)

for code_name in permission_codename_list:
    perm = Permission.objects.get(codename = code_name)
    admin_group.permissions.add(perm)

# all = admin_group.permissions.all()
# for item in all:
#     print item
