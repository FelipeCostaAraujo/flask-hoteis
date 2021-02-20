from models.hotel import HotelModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.site import SiteModel
from resources.filters import *
import sqlite3

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        data = path_params.parse_args()
        valid_data = {key: data[key] for key in data if data[key] is not None}
        params = normalize_path_params(**valid_data)

        if not params.get('cidade'):
            tupla = tuple([params[key] for key in params])
            result = cursor.execute(query_without_city, tupla)
        else:
            tupla = tuple([params[key] for key in params])
            result = cursor.execute(query_with_city, tupla)

        hoteis = []

        for index in result:
            hoteis.append({
                'hotel_id': index[0],
                'nome': index[1],
                'estrelas': index[2],
                'diaria': index[3],
                'cidade': index[4],
                'site_id': index[5]
            })
        return hoteis


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    args.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    args.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank")
    args.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank")
    args.add_argument('site_id', type=int, required=True, help="Every hotel need to be linked with a site")

    def get(self, hotel_id):
        hotel = HotelModel.findHotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.findHotel(hotel_id):
            return {"message": "Hotel id '{}' already exist.".format(hotel_id)}, 400

        dados = Hotel.args.parse_args()
        hotelModel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {"message": "The hotel must be associated to a valid site id".format(hotel_id)}, 400

        try:
            hotelModel.save_hotel()
            return hotelModel.json(), 201
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.args.parse_args()
        hotel = HotelModel.findHotel(hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return hotel.json(), 200
        hotelModel = HotelModel(hotel_id, **dados)
        try:
            hotelModel.save_hotel()
            return hotelModel.json(), 201
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'}, 500

    @jwt_required
    def delete(self, hotel_id):
        hotelModel = HotelModel.findHotel(hotel_id)
        if hotelModel:
            try:
                hotelModel.delete_hotel()
            except:
                return {'message': 'An error ocurred trying to delete hotel.'}, 500
            return {'message': 'hotel deleted'}, 200
        return {'message': 'hotel not found'}, 404
