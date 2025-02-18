from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

import request.models
from policy.models import Policy
from .models import Request
from faculty.models import Student
from faculty.serializers import StudentSerializer
from course.models import Course  # Ensure to import your Course model
from course.serializers import SimpleCourseSerializer


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
        course = data['course']
        # Check if a request with the same course and student already exists
        if Request.objects.filter(course=course, student=student).exists():
            raise PermissionDenied("You have already made a request for this course.")
        if course.max_TA_number is not None and \
                Request.objects.filter(course_id=course.id, status=Request.REQUSET_STATUS_ACCEPTED).count() >= course.max_TA_number:
            raise PermissionDenied("The capacity of teaching assistants is the completion period")
        maximum_number_of_course_for_ta = Policy.objects.filter(key="MaximumNumberOfCourseForTA").first()
        if maximum_number_of_course_for_ta is not None and maximum_number_of_course_for_ta.value <= \
                Request.objects.filter(student_id=student.id, status=Request.REQUSET_STATUS_ACCEPTED, course__semester__exact=course.semester).count():
            raise PermissionDenied("student already reach to the maximum number of course for TA")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        student, created = Student.objects.get_or_create(user=user)
        validated_data['student'] = student

        course = validated_data['course']
        if course.condition is not None and validated_data['score'] < course.condition:
            # Create the request with declined status
            validated_data['status'] = 'declined'
            request = super().create(validated_data)

            # Raise a PermissionDenied error with a custom message
            raise PermissionDenied(
                f"Your request is declined because your score "
                f"({validated_data['score']}) is lower than the required score for this course."
            )

        # Create the request with default 'pending' status
        validated_data['status'] = 'pending'
        return super().create(validated_data)

    def get_course(self, obj):
        return str(obj.course)


class InstructorRequestSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = SimpleCourseSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'student', 'course', 'score', 'status', 'date']
        read_only_fields = ['id', 'student', 'course', 'date', 'score']

    def get_course(self, obj):
        return str(obj.course)


class AdminRequestSerializer(serializers.ModelSerializer):
    course = SimpleCourseSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'student', 'course', 'status', 'date']

    def get_course(self, obj):
        return str(obj.course)
