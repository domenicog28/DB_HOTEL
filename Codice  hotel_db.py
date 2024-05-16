#pacchetto python/mysql installato pip install mysql-connector-python
#connessione
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)

#creazione database

cursore = db.cursor()
cursore.execute("create database hotel_db")

cursore.execute("use hotel_db;")

#creazione tabelle

cursore.execute("create table clienti (id_cliente int primary key auto_increment, nome varchar(16) not null, cognome varchar(16) not null, n_tel char(10) not null, email text(155) not null)engine=innodb;")

cursore.execute("create table camere(n_camera int primary key,piano int not null, tipologia text not null)engine=innodb;")

cursore.execute("create table prenotazioni (id_prenotazioni int primary key auto_increment, cliente int not null references clienti(id_cliente),n_ospiti int not null, ch_in date not null, ch_out date not null, stanza int not null references camere(n_camera))engine=innodb")

cursore.execute("create table soggiorno (prenotazione int not null references prenotazioni(id_prenotazioni),cliente int not null references clienti(id_cliente),documento varchar(16) not null,primary key(prenotazione))engine=innodb")

cursore.execute("create table dipendenti (matricola char(4) primary key, nome varchar(16) not null, cognome varchar(16) not null, tel char(10) not null, ruolo varchar(24))engine=innodb;")

cursore.execute("create table turni (id int primary key auto_increment, data date not null, turno enum('m','p','s') not null, matricola char(4) not null references dipendenti(matricola))engine=innodb;")

cursore.execute("create table fornitori(p_iva char(11) primary key,azienda varchar(24) not null, tel char(10) not null, email varchar(155) not null)engine=innodb;")

cursore.execute("create table indirizzo_f(p_iva char(11) primary key references fornitori(p_iva),tipo_via varchar(24),nome_via varchar(255), civico int,c_post char(5),città varchar(255))engine=innodb;")

cursore.execute("create table prodotti (cod_prodotto int(8) primary key, nome varchar(255) not null, fornitore char(11) not null references fornitori(p_iva))engine=innodb;")

cursore.execute("create table ordini (id_ordine int primary key auto_increment, stato enum('a','i','r','p') not null)engine=innodb;")

cursore.execute("create table lista_ordine(id int primary key auto_increment, ordine int not null references ordini(id_ordine), prodotto int(8) not null references prodotti(cod_prodotto), quantità int not null)engine=innodb;")

cursore.execute("create table effettuati (ordine int references ordini(id_ordine), dipendente char(4) not null references dipendenti(matricola), data date not null, primary key(ordine))engine=innodb;")

cursore.execute("create table ricevuti (ordine int references ordini(id_ordine),formitore char(11) not null references fornitori(p_iva), data_ricezione date not null, stato_pagamento enum('effettuato','non effettuato') not null, primary key(ordine))engine=innodb;")

cursore.execute("create table pagamenti(id_pagamento int primary key auto_increment, ordine int not null references ordini(id_ordine), n_fattura int not null, metodo_pagamento enum('contanti','assegno','bonifico') not null, importo decimal(6,2) not null, n_ass_bon varchar(16) default NULL, data_pagamento date not null)engine=innodb;")

cursore.execute("create table scorte (prodotto int(8) references prodotti(cod_prodotto),quantità int not null,primary key(prodotto))engine=innodb;")

#inserimento dei dati in ogni tabella

in_clienti="insert into clienti (nome,cognome,n_tel,email) values (%s,%s,%s,%s);"
clienti=[
    ("gianni","paglierino","3408989769","gianni.paglierino@gmail.com"),
    ("angela","milazzo","3458876969","angela.milazzo@gmail.com"),
    ("giorgia","cavalieri","3298841128","giorgia.cavalieri@libero.it"),
    ("pietro","romano","3516969348","pietro.romano@libero.it"), 
    ("fabiana","roma","3335659678","fabiana.roma@libero.it"),   
    ("antonio","lombardi","3356474644","antonio.lombardi@libero.it"),
    ("melissa","antonioli","3469984549","melissa.antonioli@libero.it"),
    ("martina","galeazzo","3281010114","martina.galeazzo@gmail.com"),
    ("lucia","paoli","3298989652","lucia.paoli@gmail.com"),
    ("jaqueline","smith","3775652312","jaqueline.smith@gmail.com"),
]
cursore.executemany(in_clienti,clienti)
db.commit()

in_camere="insert into camere (n_camera,piano,tipologia) values (%s,%s,%s);"
camere=[
    ("101","1","matrimoniale"),
    ("102","1","matrimoniale"),
    ("103","1","matrimoniale"),
    ("104","1","doppia"),
    ("105","1","singola"),
    ("201","2","matrimoniale"),
    ("202","2","matrimoniale"),
    ("203","2","matrimoniale"),
    ("204","2","doppia"),
    ("205","2","singola"),
    ("301","3","matrimoniale"),
    ("302","3","matrimoniale"),
    ("303","3","matrimoniale"),
    ("304","3","doppia"),
    ("305","3","singola")
]

cursore.executemany(in_camere,camere)
db.commit()

in_prenot="insert into prenotazioni (cliente,n_ospiti,ch_in,ch_out,stanza) values (%s,%s,%s,%s,%s);"
prenot=[
    ("1","2","2024-05-20","2024-05-25","101"),
    ("2","1","2024-05-20","2024-05-25","205"),
    ("3","2","2024-05-20","2024-05-25","301"),
    ("4","2","2024-05-24","2024-05-27","103"),
    ("5","2","2024-05-25","2024-05-28","101"),
    ("6","2","2024-06-02","2024-06-05","101"),
    ("7","2","2024-06-02","2024-06-05","301"),
    ("8","2","2024-06-02","2024-06-05","302"),
    ("9","2","2024-05-16","2024-05-20","104"),
    ("10","2","2024-05-16","2024-05-20","204")
]

cursore.executemany(in_prenot,prenot)
db.commit()

in_dipend="insert into dipendenti (matricola,nome,cognome,tel,ruolo) values (%s,%s,%s,%s,%s);"
dipend=[
    ("0001","Gianna","Casino","3245565789","receptionist"),
    ("0002","claudia","fiorentino","3201215169","receptionist"),
    ("0003","federica","longo","3567474574","receptionist"),
    ("0004","federica","galiberti","3285859624","addetta"),
    ("0005","sara","bicio","3541231455","addetta")
]

cursore.executemany(in_dipend,dipend)
db.commit()

in_forn="insert into fornitori(p_iva,azienda,tel,email) values(%s,%s,%s,%s);"
forn=[
    ("00374514522","sassari","0456954786","sassari@aruba.it"),
    ("00385641243","f&b","0039856478","f&b@aruba.it"),
    ("00398547511","brigantini","0036858566","brigantinisrl@aruba.it"),
    ("01546320259","sigma","0759865214","sigmasrl@aruba.it"),
    ("03210569854","martucci","0759445632","martuccisrl@aruba.it")
]

cursore.executemany(in_forn,forn)
db.commit()

in_tur="insert into turni(data,turno,matricola) values (%s,%s,%s);"
tur=[
    ("2024-05-16","m","0001"),
    ("2024-05-16","m","0004"),
    ("2024-05-16","p","0005"),
    ("2024-05-16","p","0002"),
    ("2024-05-16","s","0003"),
    ("2024-05-17","m","0002"),
    ("2024-05-17","m","0005"),
    ("2024-05-17","p","0003"),
    ("2024-05-17","p","0004"),
    ("2024-05-17","s","0001"),
    ("2024-05-18","m","0003"),
    ("2024-05-18","m","0005"),
    ("2024-05-18","p","0001"),
    ("2024-05-18","p","0004"),
    ("2024-05-18","s","0002"),
    ("2024-05-19","m","0001"),
    ("2024-05-19","m","0005"),
    ("2024-05-19","p","0003"),
    ("2024-05-19","p","0004"),
    ("2024-05-19","s","0002"),
    ("2024-05-20","m","0001"),
    ("2024-05-20","m","0005"),
    ("2024-05-20","p","0003"),
    ("2024-05-20","p","0004"),
    ("2024-05-20","s","0002")
]

cursore.executemany(in_tur,tur)
db.commit()

in_indir="insert into indirizzo_f(p_iva,tipo_via,nome_via,civico,c_post,città) values (%s,%s,%s,%s,%s,%s);"
indir=[
    ("00374514522","via","dei briganti",123,"12569","roma"),
    ("00385641243","piazzale","belvedere",67,"87069","catanzaro"),
    ("00398547511","via","longobucco",556,"89025","salerno"),
    ("01546320259","piazza","dei mercanti",18,"12059","palermo"),
    ("03210569854","via","firenze",45,"10259","catania")
]

cursore.executemany(in_indir,indir)
db.commit()

in_prod="insert into prodotti (cod_prodotto,nome,fornitore) values(%s,%s,%s);"
prod=[
    ("00000001","spazz&denti monouso","00374514522"),
    ("00000002","shampoo monouso","00374514522"),
    ("00000003","bagnoschiuma monouso","00374514522"),
    ("00000004","crema monouso","00374514522"),
    ("00000005","acqua 0,5l","00385641243"),
    ("00000006","cocacola 0.5l","00385641243"),
    ("00000007","birra 0,33l","00385641243"),
    ("00000008","lenzuola sing","00398547511"),
    ("00000009","lenzuola matrim","00398547511"),
    ("00000010","vetril","01546320259"),
    ("00000011","asciugacapelli","03210569854")

]

cursore.executemany(in_prod,prod)
db.commit()

in_scort="insert into scorte (prodotto,quantità) values (%s,%s);"
scort=[
    ("00000001",1000),
    ("00000002",200),
    ("00000003",200),
    ("00000004",120),
    ("00000005",100),
    ("00000006",100),
    ("00000007",100),
    ("00000008",100),
    ("00000009",100),
    ("00000010",10),
    ("00000011",6)
]

cursore.executemany(in_scort,scort)
db.commit()

in_ord="insert into ordini (id_ordine, stato) values (%s,%s);"
ord=[
    (1,"p"),
    (2,"r"),
    (3,"i"),
    (4,"a")
]

cursore.executemany(in_ord,ord)
db.commit()

in_lista="insert into lista_ordine(ordine,prodotto,quantità) values (%s,%s,%s);"
lista=[
    (1,"00000001",120),
    (1,"00000002",70),
    (1,"00000003",80),
    (1,"00000004",50),
    (2,"00000011",6),
    (3,"00000010",8),
    (4,"00000005",200),
    (4,"00000006",200),
    (4,"00000007",200)
]

cursore.executemany(in_lista,lista)
db.commit()

in_eff="insert into effettuati (ordine,dipendente,data) values(%s,%s,%s);"
eff=[
    (1,"0004","2024-05-11"),
    (2,"0005","2024-05-12"),
    (3,"0001","2024-05-16")
]

cursore.executemany(in_eff,eff)
db.commit()

in_ric="insert into ricevuti(ordine,fornitore,data_ricezione,stato_pagamento) values(%s,%s,%s,%s);"
ric=[
   (1,"00374514522","2024-05-13","effettuato"),
    (2,"03210569854","2024-05-16","non effettuato") 
]

in_pag="insert into pagamenti(ordine,n_fattura,metodo_pagamento,importo,n_ass_bon,data_pagamento) values (%s,%s,%s,%s,%s,%s)"
pag= (1,125620,"contanti",1256.00,"","2024-05-15")

cursore.execute(in_pag,pag)
db.commit()

in_soggi="insert into soggiorno (prenotazione,cliente,documento) values (%s,%s,%s);"
soggi= [
    (9, 9, "CI:CG78906CF"),
    (10,10,"CI:AS99087TY")
]

cursore.executemany(in_soggi,soggi)
db.commit()
