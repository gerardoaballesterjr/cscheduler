from django import urls

urlpatterns = [
    urls.path('', urls.include('core.urls')),
    urls.path('department/', urls.include('core.department.urls')),
    urls.path('user/', urls.include('core.user.urls')),
    urls.path('semester/', urls.include('core.semester.urls')),
    urls.path('course/', urls.include('core.course.urls')),
    urls.path('roomtype/', urls.include('core.roomtype.urls')),
    urls.path('room/', urls.include('core.room.urls')),
    urls.path('professor/', urls.include('core.professor.urls')),
    urls.path('curriculum/', urls.include('core.curriculum.urls')),
    urls.path('subject/', urls.include('core.subject.urls')),
    urls.path('assign/', urls.include('core.assign.urls')),
    urls.path('section/', urls.include('core.section.urls')),
]
