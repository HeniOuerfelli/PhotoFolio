from rest_framework import serializers
from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'email', 'first_name', 'last_name', 'cin', 'post', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Crée un admin avec un mot de passe sécurisé.
        """
        admin = Admin(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            cin=validated_data['cin'],
            post=validated_data['post']
        )
        admin.set_password(validated_data['password'])
        admin.save()
        return admin

    def validate_email(self, value):
        """
        Vérifie que l'email est unique.
        """
        if Admin.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un admin avec cet email existe déjà.")
        return value
