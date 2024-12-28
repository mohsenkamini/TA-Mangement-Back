from rest_framework import serializers
from .models import Request
from faculty.models import Student
from course.models import Course  # Ensure to import your Course model
from course.serializers import SimpleCourseSerializer
from rest_framework.exceptions import PermissionDenied

class StudentRequestSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    course = SimpleCourseSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'course_id', 'course', 'score', 'status', 'date']
        read_only_fields = ['status']

    def validate(self, data):
        user = self.context['request'].user
        student, created = Student.objects.get_or_create(user=user)

        # Check if a request with the same course and student already exists
        if Request.objects.filter(course=data['course'], student=student).exists():
            raise PermissionDenied("You have already made a request for this course.")

        course = data['course']
        if course.condition is not None and data['score'] < course.condition:
            raise PermissionDenied("Your score is lower than required condition for this course.")

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        student, created = Student.objects.get_or_create(user=user)
        validated_data['student'] = student
        return super().create(validated_data)

    def get_course(self, obj):
        return str(obj.course)

class InstructorRequestSerializer(serializers.ModelSerializer):
    # student = SimpleStudentSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)
    class Meta:
        model = Request
        fields = ['id','student', 'course', 'score', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'date', 'score']

    def get_course(self, obj):
        return str(obj.course)

class AdminRequestSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer(read_only=True)
    class Meta:
        model = Request
        fields = ['id','student', 'course', 'status', 'date']

    def get_course(self, obj):
        return str(obj.course)
