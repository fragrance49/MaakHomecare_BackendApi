from rest_framework import serializers
from .models import Services, Members, Task, Booking


class taskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'description',
            'due',
        )

class membersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = '__all__'

class servicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class bookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'