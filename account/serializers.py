from rest_framework import serializers
from account.models import UserInfo
from couple.models import LoveShow, RandomMath

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class UserInfoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user', 'nickname', 'gender', 'avatar', )

class LoveShowSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = LoveShow
        fields = ('lover', 'favour')
    
# class  RandomMathSerializer(DynamicFieldsModelSerializer):
#     class Meta:
#         model = RandomMath
#         files = ('vote',)
        