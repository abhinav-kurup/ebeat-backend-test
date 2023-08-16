from authentication.models import *

posts_list = ["PI", "DYSP", "SP", "IGP"]


def get_officer_region(user_obj):
    try:
        if user_obj.post not in posts_list:
            return None
        if user_obj.post == "PI":
            if PoliceStationModel.objects.filter(pi=user_obj, is_active=True).exists():
                obj = PoliceStationModel.objects.get(pi=user_obj, is_active=True)
                return obj.area
        elif user_obj.post == "DYSP":
            if SubDivisionModel.objects.filter(dysp=user_obj, is_active=True).exists():
                obj = SubDivisionModel.objects.get(dysp=user_obj, is_active=True)
                return obj.area
        elif user_obj.post == "SP":
            if DistrictModel.objects.filter(sp=user_obj, is_active=True).exists():
                obj = DistrictModel.objects.get(sp=user_obj, is_active=True)
                return obj.area
        elif user_obj.post == "IGP":
            if StateModel.objects.filter(igp=user_obj, is_active=True).exists():
                obj = StateModel.objects.get(igp=user_obj, is_active=True)
                return obj.area
    except Exception as e:
        print("error :", e)
        return None
