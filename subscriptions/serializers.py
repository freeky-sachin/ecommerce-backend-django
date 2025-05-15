from rest_framework import serializers
from .models import Subscription
import datetime

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user', 'start_date']

    def create(self, validated_data):
        frequency = validated_data.get("frequency")
        start_date = datetime.date.today()

        if frequency == 'Weekly':
            next_delivery = start_date + datetime.timedelta(days=7)
        else:
            next_delivery = start_date + datetime.timedelta(days=30)

        return Subscription.objects.create(
            user=self.context['request'].user,
            start_date=start_date,
            next_delivery=next_delivery,
            **validated_data
        )
