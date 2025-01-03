from rest_framework import serializers
from .models import Student, Instructor


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name','last_name', 'student_number', 'biography']

class TAStudentSerializer(StudentSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name','last_name', 'student_number']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'first_name','last_name', 'way_of_communication', 'research_fields', 'email']

class SimpleInstructorSerializer(InstructorSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'first_name','last_name', 'way_of_communication', 'research_fields']
        read_only_fields = ['way_of_communication', 'research_fields']