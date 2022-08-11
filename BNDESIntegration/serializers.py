from rest_framework import serializers
from .models import Transaction, Company, BNDESTransaction, ArchiveBNDESTransaction


class BNDESTransactionSerializers(serializers.ModelSerializer):
    """CLASS to serialize 'serializers.BNDESTransaction' model data
    """

    def create(self, validated_data):
        """METHOD for saving BNDESTransaction serialized data on database

        Args:
            validated_data (dict): BNDESTransaction serialized data
        Returns:
            dict: BNDESTransaction serialized data
        """

        response_ope, obj = BNDESTransaction.objects.filter(
            logs=validated_data['logs']
        ).get_or_create(**validated_data)

        if obj == False:
            response_ope.save()

        return response_ope

    class Meta:
        model = BNDESTransaction
        fields = '__all__'


class ArchiveBNDESTransactionSerializers(serializers.Serializer):
    """METHOD for saving BNDESTransaction serialized data on database
    Args:
        validated_data (dict): BNDESTransaction serialized data
    Returns:
        dict: BNDESTransaction serialized data
    """

    def create(self, validated_data):
        """METHOD for saving ArchiveBNDESTransaction serialized data on database

        Args:
            validated_data (dict): BNDESTransaction serialized data
        Returns:
            dict: BNDESTransaction serialized data
        """
        response_ope = ArchiveBNDESTransaction.objects.create(**validated_data)
        response_ope.save()

        return response_ope

    class Meta:
        model = ArchiveBNDESTransaction
        fields = (
            'client',
            'logs',
            'delete_data',
        )
