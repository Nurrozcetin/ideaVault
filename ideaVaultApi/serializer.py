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
    title = serializers.CharField(write_only=True)
    desc = serializers.CharField(write_only=True)
    encrypted_title = serializers.SerializerMethodField(read_only=True)
    encrypted_desc = serializers.SerializerMethodField(read_only=True)
    requirements = RequirementsSerializer(many=True)
    category = CategorySerializer(many=True)
    member = MemberSerializer(many=True)

    class Meta:
        model = Idea
        fields = ['id', 'title', 'desc', 'encrypted_title', 'encrypted_desc', 'requirements', 'category', 'member']

    def create(self, validated_data):
        key = load_key('secret.key')
        validated_data['title'] = encrypt_message(validated_data['title'], key)
        validated_data['desc'] = encrypt_message(validated_data['desc'], key)

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
        if 'title' in validated_data:
            instance.title = encrypt_message(validated_data['title'], key)
        if 'desc' in validated_data:
            instance.desc = encrypt_message(validated_data['desc'], key)
        
        requirements_data = validated_data.pop('requirements', None)
        category_data = validated_data.pop('category', None)
        member_data = validated_data.pop('member', None)

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

    def get_encrypted_title(self, obj):
        key = load_key('secret.key')
        try:
            return decrypt_message(obj.title, key)
        except Exception as e:
            return str(e)

    def get_encrypted_desc(self, obj):
        key = load_key('secret.key')
        try:
            return decrypt_message(obj.desc, key)
        except Exception as e:
            return str(e)
