from app.services.geocoding_serv import geocode_address

print(geocode_address("سيتي سنتر"))  # Example test call
print(geocode_address("محطة مصر"))  # Example test call 
print(geocode_address("الورديان"))  # Example test call
print(geocode_address("جناكليس"))  # Example test call
print(geocode_address("الموقف الجديد"))  # wrong coordinates test > mawqaf el asafra
print(geocode_address("محرم بك"))  # Example test
print(geocode_address("قسم شرطة سيدي جابر"))  # wrong coordinates test > location not found
print(geocode_address("قسم شرطة محرم بك"))  # wrong coordinates test > markaz shabab el seiuof 


