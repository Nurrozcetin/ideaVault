from rest_framework import serializers
from .models import Category, Member, Requirements, Idea
from .utils import encrypt_message, decrypt_message, load_key

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']  

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'name', 'job']  

class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = ['id', 'name']  

class IdeaSerializer(serializers.ModelSerializer):
    encrypted_id = serializers.SerializerMethodField()
    requirements = RequirementsSerializer(many=True)
    category = CategorySerializer(many=True)
    member = MemberSerializer(many=True)

    class Meta:
        model = Idea
        fields = ['id', 'encrypted_id', 'title', 'desc', 'requirements', 'category', 'member']

    def create(self, validated_data):
        key = load_key('secret.key')
        requirements_data = validated_data.pop('requirements')
        category_data = validated_data.pop('category')
        member_data = validated_data.pop('member')

        idea = Idea.objects.create(**validated_data)

        for req_data in requirements_data:
            req, created = Requirements.objects.get_or_create(**req_data)
            idea.requirements.add(req)
        
        for cat_data in category_data:
            cat, created = Category.objects.get_or_create(**cat_data)
            idea.category.add(cat)
        
        for mem_data in member_data:
            mem, created = Member.objects.get_or_create(**mem_data)
            idea.member.add(mem)

        return idea

    def update(self, instance, validated_data):
        key = load_key('secret.key')
        
        requirements_data = validated_data.pop('requirements', None)
        category_data = validated_data.pop('category', None)
        member_data = validated_data.pop('member', None)

        if 'title' in validated_data:
            instance.title = validated_data['title']
        if 'desc' in validated_data:
            instance.desc = validated_data['desc']

        if requirements_data:
            instance.requirements.clear()
            for req_data in requirements_data:
                req, created = Requirements.objects.get_or_create(**req_data)
                instance.requirements.add(req)

        if category_data:
            instance.category.clear()
            for cat_data in category_data:
                cat, created = Category.objects.get_or_create(**cat_data)
                instance.category.add(cat)

        if member_data:
            instance.member.clear()
            for mem_data in member_data:
                mem, created = Member.objects.get_or_create(**mem_data)
                instance.member.add(mem)

        instance.save()
        return instance

    def get_encrypted_id(self, obj):
        key = load_key('secret.key')
        try:
            return encrypt_message(str(obj.id), key)
        except Exception as e:
            return str(e)
