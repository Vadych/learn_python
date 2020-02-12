import csv
import os



class BaseCar:
    def __init__(self, type, brand, photo, carrying):
        self.car_type = type
        self.brand = brand
        self.photo_file_name = photo
        self.carrying = carrying
    def __repr__(self):
        return self.car_type+'-'+self.brand
    def __str__(self):
        return self.car_type+'-'+self.brand
    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[-1]


class Car(BaseCar):
    def __init__(self, brand, passeger_seats_count, photo, carrying):
        super().__init__("car", brand, photo, carrying)
        self.passenger_seats_count=passeger_seats_count

class Truck(BaseCar):
    def __init__(self, brand, photo,bl,bh,bw, carrying):
        super().__init__("truck",brand,photo,carrying)
        self.body_width=bw
        self.body_height=bh
        self.body_length=bl

    def get_body_volume(self):
        return self.body_height*self.body_length*self.body_width

class SpecMachine(BaseCar):
    def __init__(self, brand, photo, carrying, extra):
        super().__init__("spec_machine", brand, photo, carrying)
        self.extra = extra


def main():
    result=get_car_list('cars.csv')
    print ('РЕЗУЛЬТАТ')
    for r in result:
        print (r, r.get_photo_file_ext(),r.get_body_volume()if type(r)==Truck else '')


def get_car_list(file_name):
    f = open(file_name, 'r')
    reader = csv.reader(f, delimiter=';')
    car_list=[]
    for row in reader:
        if len(row) != 7:
            continue
        if not row[3]:
            continue
        try:
            carrying = float(row[5])
            if row[0] == 'car':
                pass_count = int(row[2])
                cars=Car(row[1],pass_count, row[3], carrying)
            elif row[0] == 'truck':
                if not row[4]:
                    bw = bh = bl = 0
                else:
                    lwh = row[4].split('x')
                    bl = float(lwh[0])
                    bw = float(lwh[1])
                    bh = float(lwh[2])
                cars=Truck(row[1], row[3], bl, bh, bw, carrying)
            elif row[0] == 'spec_machine':
                cars= SpecMachine(row[1], row[3], carrying, row[6])
            else:
                continue
        except ValueError:
            continue
        car_list.append(cars)
    f.close()
    return car_list


if __name__ == '__main__':
    main()
