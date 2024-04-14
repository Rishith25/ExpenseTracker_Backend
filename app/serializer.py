# serializers.py
from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'phone_number', 'first_name', 'last_name' ]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class UserSigninSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_no','balance','bank_name','is_default']

    def validated_account(self, account):
        if account<0:
            raise serializers.ValidationError("Account number must be positive")
        return account
    
    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account


class FinancialTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=FinancialTransaction
        exclude = ['user']

    def create(self, validated_data):
        transaction = FinancialTransaction.objects.create(**validated_data)
        return transaction

class AccountBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_no','balance','bank_name','is_default']

    def validate(self, data):
        return data

    