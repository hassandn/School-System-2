from django.contrib.gis.db.models.functions import Distance
from school.models import School

class UserLocationManage:
    @staticmethod
    def get_nearest_schools(user, count=3):
        if not user.location:
            return []

        nearest_schools = School.objects.annotate(
            distance=Distance('location', user.location)
        ).order_by('distance')[:count]

        return nearest_schools