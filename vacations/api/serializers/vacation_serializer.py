from rest_framework import serializers
from datetime import date
from vacations.models import Vacation, Country


class VacationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Vacation model.
    Converts Vacation model instances to and from JSON format.
    """

    class Meta:
        model = Vacation
        fields = [
            'id',
            'country',
            'description',
            'start_date',
            'end_date',
            'price',
            'image_filename',
        ]
class AddVacationSerializer(serializers.ModelSerializer):
    """
    Serializer for adding a new vacation.
    Validates business rules.
    """

    class Meta:
        model = Vacation
        fields = [
            'country',
            'description',
            'start_date',
            'end_date',
            'price',
            'image_filename',
        ]

    def validate_price(self, value: float) -> float:
        if value < 0 or value > 10000:
            raise serializers.ValidationError("Price must be between 0 and 10,000.")
        return value

    def validate(self, data: dict) -> dict:
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be before start date.")
        if data['start_date'] < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return data
    
class EditVacationSerializer(serializers.ModelSerializer):
    """
    Serializer for editing an existing vacation.
    Allows skipping the image update.
    """

    class Meta:
        model = Vacation
        fields = [
            'description',
            'start_date',
            'end_date',
            'price',
            'image_filename',
        ]

    def validate_price(self, value: float) -> float:
        if value < 0 or value > 10000:
            raise serializers.ValidationError("Price must be between 0 and 10,000.")
        return value

    def validate(self, data: dict) -> dict:
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date cannot be before start date.")

        return data
