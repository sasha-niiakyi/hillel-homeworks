CREATE TABLE IF NOT EXISTS warehouses (
	wh_id int PRIMARY KEY NOT NULL,
	wh_name varchar(100) NOT NULL,
	wh_type varchar(50),
	wh_location varchar(50)
);
	
CREATE TABLE IF NOT EXISTS goods (
	gd_id int PRIMARY KEY NOT NULL,
	gd_name varchar(50) NOT NULL,
	gd_price real NOT NULL,
	gd_count int NOT NULL,
	gd_wh_id int references warehouses(wh_id)
);

INSERT INTO warehouses VALUES(1, 'Випівничий', 'Роздрібний', 'Київ'),
							 (2, 'Електросейв', 'Оптовий', 'Львів'),
							 (3, 'Ескімос', 'Холодильний', 'Одеса');

INSERT INTO goods VALUES(1, 'Пепсі', 50, 200, 1),
						(2, 'Кондиціонер', 9000, 100, 2),
						(3, 'Повербанк', 1000, 300, 2),
						(4, 'Морозиво Каштан', 25, 300, 3),
						(5, 'Пиво', 100, 300, 1),
						(6, 'Яловичина', 300, 300, 3),
						(7, 'Айфон14', 40000, 400, 2),
						(8, 'Лосось', 1000, 100, 3),
						(9, 'Йогурт', 20, 300, 3),
						(10, 'Лимонад', 30, 400, 1);

UPDATE goods SET gd_price = gd_price + 10 WHERE gd_price < 300;

DELETE FROM goods WHERE gd_wh_id = 1;

CREATE INDEX gd_name_idx ON goods(gd_name);

explain analyse SELECT * FROM goods WHERE gd_name = 'Пепсі';