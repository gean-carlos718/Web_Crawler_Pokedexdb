#BIBLIOTECA P/ REQUESTS E MANIPULAÇÃO HTML
import requests
import lxml.html as lh
#BIBLIOTECA DE ACESSO AO BANCO:
import pymongo 
from pymongo import MongoClient


class Pokemon:
    def __init__(self, num, name, type_, total_pts, hp, attack, defense, sp_attack, sp_defense, speed):
        self.num = num
        self.name = name
        self.type_ = type_
        self.total_pts = total_pts
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sp_attack = sp_attack
        self.sp_defense = sp_defense
        self.speed = speed
    #RETORNA TODOS OS DADOS DO POKEMON
    def check_entry(self, _id):
        stats_dictionary = {"_id":_id,
                            "#":self.num,
                            "Name":self.name,
                            "Type":self.type_,
                            "Total":self.total_pts,
                            "HP":self.hp,
                            "Attack":self.attack,
                            "Defense":self.defense,
                            "Sp Attack":self.sp_attack,
                            "Sp Defense":self.sp_defense,
                            "Speed":self.speed
                            }
        return stats_dictionary
    

#CONEXÃO COM MONGODB
cluster = MongoClient("mongodb+srv://gean-carlos:147147147@cluster0.cdm00.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["pokedex"]
collection = db["pokedex"]



url='http://pokemondb.net/pokedex/all'
page = requests.get(url)
doc = lh.fromstring(page.content)
#LINHAS DA TABELA NO HTML
tr_elements = doc.xpath('//tr')

#CONTADOR DE POKEMONS INSERIDOS
i = 0 
#LOOP PARA PERCORRER AS LINHAS DA TABLE
for j in range(1,len(tr_elements)):
    poke_row=tr_elements[j]
    #CHECA SE HÁ ALGUMA LINHA COM ERRO
    if (len(poke_row)!=10):
        break
    
    #LISTA PARA INSERIR OS DADOS DE UM POKEMON
    poke_stats = []    
    #LOOP PARA PERCORRER AS COLUNAS DA TABLE
    for column in poke_row.iterchildren():
        data=column.text_content()
        if(data.isnumeric()):
            try:
                data=int(data)
            except:
                pass
        poke_stats.append(data)
    #CRIAÇÃO DO POKEMON DAQUELA LINHA:
    pokemon = Pokemon(poke_stats[0],poke_stats[1],poke_stats[2],poke_stats[3],poke_stats[4],poke_stats[5],poke_stats[6],poke_stats[7],poke_stats[8],poke_stats[9])
    #INSERÇÃO NO BANCO DE DADOS:
    collection.insert_one(pokemon.check_entry(i))
    i+=1

    

    
