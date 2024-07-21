from rest_framework import serializers




class PredictionSerializer(serializers.Serializer):
    CHOICES = [
        ('yes', 'yes'),
        ('no', 'no')
    ]
    hours_studied = serializers.IntegerField(min_value=0)
    previous_scores = serializers.FloatField(min_value=0, max_value=100)
    extracurricular_activities = serializers.ChoiceField(choices=CHOICES)
    sleep_hours = serializers.IntegerField(min_value=0)
    sample_question_papers_practiced = serializers.IntegerField(min_value=0)