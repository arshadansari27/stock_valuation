create table IF NOT EXISTS Instrument (
	ID INT NOT NULL AUTO_INCREMENT,
	Ticker VARCHAR(10),
	Name VARCHAR(255),
	Current_Price DECIMAL,
	PRIMARY KEY (ID)
);

create table IF NOT EXISTS Transaction (
	ID INT NOT NULL AUTO_INCREMENT,
	Position_Id INT,
	User_ID INT,
	Buy_or_Sell ENUM("BUY", "SELL"),
	Quantity INT,
	Price DECIMAL,
	Date DATETIME,
	PRIMARY KEY (ID),
	FOREIGN KEY Insturment_key(Position_Id) REFERENCES Instrument(ID)
);
