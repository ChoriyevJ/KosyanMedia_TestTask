from bs4 import BeautifulSoup
import json
import os


class Parser:

    def __init__(self, file_name, extension, feature="xml"):
        self.__file_name = file_name
        self.__extension = extension
        self.__feature = feature

    def __get_soup(self):
        try:
            with open(f'{self.__file_name}.{self.__extension}', mode='r', encoding='utf-8') as file:
                file_content = file.read()
        except Exception as e:
            raise FileNotFoundError(e)

        soup = BeautifulSoup(file_content, self.__feature)
        return soup

    def __get_json_data(self):
        soup = self.__get_soup()
        json_data = []
        main_flights = soup.find_all("Flights")
        _t = ('OnwardPricedItinerary', 'ReturnPricedItinerary')
        for main_flight in main_flights:
            _flights = main_flight.find_all('Flights')
            flights = dict(zip(_t, _flights))
            _dict = dict()
            for key, flight in flights.items():
                carrier = flight.find("Carrier").get_text(strip=True)
                flight_number = flight.find("FlightNumber").get_text(strip=True)
                source = flight.find("Source").get_text(strip=True)
                destination = flight.find("Destination").get_text(strip=True)
                departure_time_stamp = flight.find("DepartureTimeStamp").get_text(strip=True)
                arrival_time_stamp = flight.find("ArrivalTimeStamp").get_text(strip=True)
                class_ = flight.find("Class").get_text(strip=True)
                number_of_stop = flight.find("NumberOfStops").get_text(strip=True)
                fare_basis = flight.find("FareBasis").get_text(strip=True)
                ticket_type = flight.find("TicketType").get_text(strip=True)

                _dict[key] = {
                    'carrier': carrier,
                    'flight_number': flight_number,
                    'source': source,
                    'destination': destination,
                    'departure_time_stamp': departure_time_stamp,
                    'arrival_time_stamp': arrival_time_stamp,
                    'class': class_,
                    'number_of_stop': number_of_stop,
                    'fare_basis': fare_basis,
                    'ticket_type': ticket_type
                }
                json_data.append(_dict)
            pricing = main_flight.find("Pricing")
            _pricing_dict = dict()
            if pricing:
                service_charges = pricing.find_all("ServiceCharges")
                for charge in service_charges:
                    key = charge['ChargeType']
                    value = charge.get_text()
                    _pricing_dict[f"{charge['type']}_{key}"] = value
            _dict['Pricing'] = _pricing_dict
        return json_data

    def __write_to_json(self):
        json_data = self.__get_json_data()
        os.makedirs('data', exist_ok=True)
        with open(f'data/{self.__file_name}.json', mode='w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    def run(self):
        self.__write_to_json()


Parser('RS_Via-3', extension='xml').run()
Parser('RS_ViaOW', extension='xml').run()
"""
example for github.com
"""