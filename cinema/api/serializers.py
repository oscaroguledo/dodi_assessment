from rest_framework import serializers
import re
from api.models import Movie

STATUS = (
        ("coming-up", "coming-up"),
        ("starting", "starting"),
        ("running", "running"),
        ("finished", "finished"),
    )
class DateField(serializers.CharField):
    def is_leap_year(self,year):
        if year % 4 == 0:  # Check if the year is evenly divisible by 4
            if year % 100 == 0:  # If divisible by 100, also check if divisible by 400
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
        
    def to_internal_value(self, value):
        # Check if the value matches the YYYY-MM-DD format
        if not re.match(r"\d{4}-\d{2}-\d{2}", value) or len(value) != 10:
            raise serializers.ValidationError("Date must be in YYYY-MM-DD format")
        
        # Extract month part from the date string
        year, month, day = map(int, value.split('-'))
        
        # Check if the month is within the range of 1 to 12
        if not 1 <= month <= 12:
            raise serializers.ValidationError("Month must be between 1 and 12")
        if month in [1,3,5,7,8,10,12]:
            if not 1 <= day <= 31:
                raise serializers.ValidationError("Day must be between 1 and 31")
        if month in [4,6,9,11]:
            if not 1 <= day <= 30:
                raise serializers.ValidationError("Day must be between 1 and 30")
        if month in [2]:
            if self.is_leap_year(year):
                if not 1 <= day <= 29:
                    raise serializers.ValidationError("Day must be between 1 and 29 for leap year")
            else:
                if not 1 <= day <= 28:
                    raise serializers.ValidationError("Day must be between 1 and 28")
        
        return value
    
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=False, required=False)
    name = serializers.CharField(allow_null=False, allow_blank=False)
    protagonists = serializers.ListField(required=True, allow_empty=False)
    ranking = serializers.IntegerField(allow_null=True, required=False)
    status = serializers.ChoiceField(allow_null=False, allow_blank=False, choices=STATUS)
    start_date = DateField(allow_null=False, allow_blank=False)
    poster = serializers.ImageField(allow_null=True, required=False)  # ImageField for poster
    trailer = serializers.FileField(allow_null=True, required=False)  # FileField for trailer

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)