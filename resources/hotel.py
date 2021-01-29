from models.hotel import HotelModel
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
    def get(self):
        return [hotel.json() for hotel in HotelModel.query.all()]


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    args.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    args.add_argument('diaria', type=float, required=True, help="The field 'diaria' cannot be left blank")
    args.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be left blank")

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
