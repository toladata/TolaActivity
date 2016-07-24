from rest_framework import serializers
from activitydb.models import ProjectComplete, ProjectAgreement, Program, LoggedUser

class ProgramSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Program
		fields = ('name', 'gaitid')

class ProjectAgreementSerializer(serializers.ModelSerializer):
	program = ProgramSerializer()

	class Meta:
		model = ProjectComplete 
		fields = ('project_name','program','approval','create_date')

class LoggedUserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = LoggedUser
		fields = ('username', 'country', 'email')