# bo = BeatOfficerModel.objects.get(email=request.email)
# region = bo.police_station.region
# queryset = LocationCategoryModel.objects.filter(location__within=region, is_active=True)
# ser = LocationCategoryModelSerializer(queryset, many=True)
# return Response(ser.data, status=status.HTTP_200_OK)