from rest_framework import serializers
from .models import Operacoes, Empresa, BNDESOperacoes, ArchiveBNDESOperacoes


class BNDESOperacoesSerializers(serializers.ModelSerializer):
    """CLASS to serialize 'serializers.BNDESOperacoes' model data
    """

    def create(self, validated_data):
        """METHOD for saving BNDESOperacoes serialized data on database

        Args:
            validated_data (dict): BNDESOperacoes serialized data
        Returns:
            dict: BNDESOperacoes serialized data
        """

        response_ope, obj = BNDESOperacoes.objects.filter(
            logs=validated_data['logs']
        ).get_or_create(**validated_data)

        if response_ope == False:
            response_ope.save()

        return response_ope

    class Meta:
        model = BNDESOperacoes
        fields = '__all__'


class ArchiveBNDESOperacoesSerializers(serializers.Serializer):
    """METHOD for saving BNDESOperacoes serialized data on database
    Args:
        validated_data (dict): BNDESOperacoes serialized data
    Returns:
        dict: BNDESOperacoes serialized data
    """

    def create(self, validated_data):
        """METHOD for saving ArchiveBNDESOperacoes serialized data on database

        Args:
            validated_data (dict): BNDESOperacoes serialized data
        Returns:
            dict: BNDESOperacoes serialized data
        """
        response_ope = ArchiveBNDESOperacoes.objects.create(**validated_data)
        response_ope.save()

        return response_ope

    class Meta:
        model = ArchiveBNDESOperacoes
        fields = (
            'client',
            'logs',
            'delete_data',
        )
