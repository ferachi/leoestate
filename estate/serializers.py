from rest_framework import serializers
from .models import  Place, PropertyImage, RentablePlace, BuyablePlace, Address, ThreeDView, Facility, OtherField


class PropertyImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = PropertyImage
		fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = '__all__'


class ThreeDViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = ThreeDView
		fields = '__all__'


class RentablePlaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = RentablePlace
		fields = ['duration', 'is_rented', 'duration_type', 'total_duration_months']


class BuyablePlaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = BuyablePlace
		fields = ['is_sold']


class FacilitySerializer(serializers.ModelSerializer):
	class Meta:
		model = Facility
		fields = '__all__'


class OtherFieldSerializer(serializers.ModelSerializer):
	class Meta:
		model = OtherField
		fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
	other_fields = OtherFieldSerializer(many=True)
	property_type = serializers.StringRelatedField()
	facilities = FacilitySerializer(many=True)
	address = AddressSerializer()
	three_d_views = ThreeDViewSerializer
	images = PropertyImageSerializer(many=True)
	rentableplace = RentablePlaceSerializer()
	buyableplace = BuyablePlaceSerializer()
	class Meta:
		model = Place
		fields = '__all__'


