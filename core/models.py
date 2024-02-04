from django.db import models
from django.contrib.auth.models import AbstractUser
from django import urls
from core import utils

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('department:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('department:update', args=[self.slug])

class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='admin_department', null=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('user:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('user:update', args=[self.slug])

class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='course_department')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('course:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('course:update', args=[self.slug])

class RoomType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='room_type_department', null=True, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('room-type:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('room-type:update', args=[self.slug])

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='room_type')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('room:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('room:update', args=[self.slug])

class Professor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    minimum_units = models.IntegerField(default=24)
    maximum_units = models.IntegerField(default=24)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professor_department')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('professor:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('professor:update', args=[self.slug])
    
    def get_schedule_url(self):
        return urls.reverse_lazy('professor:schedule', args=[self.slug])

class Curriculum(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curriculum_course')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('curriculum:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('curriculum:update', args=[self.slug])

class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=(['Minor','Minor'],['Major','Major']))
    units = models.IntegerField()
    hours = models.FloatField(choices=[(1.0, 1.0), (3.0, 3.0), (4.0, 4.0), (5.0, 5.0), (6.0, 6.0), (8.0, 8.0)])
    level = models.IntegerField()
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='subject_curriculum')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subject_department')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='subject_room_type')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('subject:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('subject:update', args=[self.slug])

class Semester(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('semester:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('semester:update', args=[self.slug])
    
    def get_generate_url(self):
        return urls.reverse_lazy('semester:generate', args=[self.slug])

class Day(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)

class Assign(models.Model):
    days = models.ManyToManyField(Day, related_name='assign_days', blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assign_subject')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='assign_professor')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='assign_semester')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('assign:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('assign:update', args=[self.slug])

class Section(models.Model):
    block = models.CharField(max_length=255)
    level = models.IntegerField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='section_semester')
    subjects = models.ManyToManyField(Subject, related_name='section_subjects')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='section_course')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('section:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('section:update', args=[self.slug])
    
    def get_schedule_url(self):
        return urls.reverse_lazy('section:schedule', args=[self.slug])

class Schedule(models.Model):
    days = models.ManyToManyField(Day, related_name='schedule_days')
    stime = models.CharField(max_length=255)
    etime = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='schedule_room')
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE, related_name='schedule_assign')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='schedule_section')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = utils.slug_generator(self) if not self.slug else self.slug
        return super().save(*args, **kwargs)
    
    def get_delete_url(self):
        return urls.reverse_lazy('schedule:delete', args=[self.slug])
    
    def get_update_url(self):
        return urls.reverse_lazy('schedule:update', args=[self.slug])