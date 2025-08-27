from rest_framework import serializers

class LikeActionSerializer(serializers.Serializer):
    """
    Serializer for Like/Unlike vacation actions.
    Accepts a vacation_id for the action.
    """
    vacation_id = serializers.IntegerField()
