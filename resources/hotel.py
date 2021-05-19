from flask_restful import  Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

hoteis = [
                {
                    'hotel_id': 'alpha',
                    'nome': 'Alpha Hotel',
                    'estrelas': 4.3,
                    'diaria': 420.34,
                    'cidade': 'Rio de Janeiro'
                },
    {
                    'hotel_id': 'bravo',
                    'nome': 'Bravo Hotel',
                    'estrelas': 4.4,
                    'diaria': 380.90,
                    'cidade': 'Santa Catarina'
                },
    {
                    'hotel_id': 'charlie',
                    'nome': 'Charlie Hotel',
                    'estrelas': 3.9,
                    'diaria': 320.20,
                    'cidade': 'Santa Catarina'
                }
]

class Hoteis(Resource):

    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel (Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The filter 'nome' cannot be left blank.")
    argumentos.add_argument('estrelas', type=float, required=True, help ="The filter 'estrelas' cannot be left blank.")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    #def find_hotel(hotel_id):
    #    for hotel in hoteis:
    #        if hotel['hotel_id'] == hotel_id:
    #            return hotel
    #    return None
    
    def get(self, hotel_id):
        #hotel = Hotel.find_hotel(hotel_id)
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 #not found    


    @jwt_required()
    def post(self, hotel_id):
        
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' já existe.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'error ocurred trying to save hotel.'}, 500 #Internal server 500
        return hotel.json()

        #novo_hotel = hotel_objeto.json()
        #hoteis.append(novo_hotel)
        #return novo_hotel, 200

        #novo_hotel = {
        #   'hotel_id' : hotel_id,
        #    'nome' : dados['nome'],
        #    'estrelas' : dados['estrelas'],
        #   'diaria' : dados['diaria'],
        #    'cidade' : dados['cidade']
        #}

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        #novo_hotel = {'hotel_id' : hotel_id, **dados }
        #hotel_objeto = HotelModel(hotel_id, **dados)
        #novo_hotel = hotel_objeto.json()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)

        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 # OK
        
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except: 
            return {'message': 'error ocurred trying to put hotel.'}, 500 #Internal server 500
        #hoteis.append(novo_hotel)
        return hotel.json(), 201 # created criado

    @jwt_required()
    def delete(self, hotel_id):
        #global hoteis
        #hoteis = [hotel  for hotel in hoteis if hotel['hotel_id'] !=  hotel_id ]
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'error ocurred trying to delete hotel.'}, 500 #Internal server 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}
