#coding: utf-8 
import pycep_correios
import googlemaps
import csv
# import folium 
# from IPython.display import display

gmaps_key = googlemaps.Client(key = "AIzaSyDHvdeuprivPHC4LQygx25Y13uQaLjdIME")

def main(cep):
    
    valido = pycep_correios.validar_cep(cep)
    print(valido)
    try:
        adress = pycep_correios.get_address_from_cep(cep)
        adress = format_adress(adress)
        geocode_result  =  gmaps_key.geocode(adress)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]

        retorno = {}
       
        retorno = [cep , adress , lat , lng]
        print("Cep salvo com sucesso")
        return retorno 

    except Exception as e: 
        print(e)
        retorno  =  ["Nan","Nan","Nan","Nan"]
        print("Não é possivel pela Api dos Correios Associar um endereço a este CEP")
        return retorno 
    
def saveCsv(): 
    with open('coordenadas_cep.csv',"w") as coordenadas_cep:
        fieldnames = ["Cep" , "Endereço", "Lat" , "Lng"]
        writer = csv.DictWriter(coordenadas_cep,fieldnames = fieldnames)
        writer.writeheader()

    # Segundo o sistema de correios a faixa de ceps possiveis para campina grande, 
    # está localizada entre os numeros 58400001,5844999, porém , por experiências realizadas dentro 
    # do proprio site juntamente com a API , alguns ceps nao estão associados á endereços, ou seja
    # sao ceps vazios , podendo invalidar nossa consulta por cordenadas. Isto já foi tratado por meio
    # dos comandos try except.
        for i in range(58400001, 58401000):
            cep = str(i)
            info = main(cep)
            info_toDic = {'Cep': info[0] ,'Endereço': info[1], 'Lat': info[2], 'Lng': info[3]}
            writer.writerow(info_toDic)


    # ceps_posssiveis = range(58400001,58401000)
    # Em python o intervalo é aberto no final 
    
    

def format_adress(adress):
    return  adress["logradouro"] +  " - " + adress["bairro"] + " - " + adress["cidade"] + " - " + adress["uf"]


ceps_possiveis  = range(58400001,58401000)
#saveCsv("58400001")
saveCsv()








# print(str(lat) + str(lng)) 
# print(lat_long)
# geo_map = folium.Map(location= lat_long ,zoom_start= 600)
# folium.Marker(location= lat_long , popup= "location",tooltip="Go to Location").add_to(geo_map)
# display(geo_map)


