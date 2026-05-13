"""
Generador del catálogo Mundial 2026 - Panini.
Fuente: cartophilic-info-exch.blogspot.com (checklist comunitario, abierto, no comercial).
Output: catalog.json con estructura compatible con el data model v0.1.

Decisiones de limpieza:
- Typos del fuente corregidos silenciosamente (POR-11 duplicado → POR-14, KAS-12 → KSA-12,
  "Morrocco" → "Morocco", etc.).
- "Printed in album" (NNIO/NNO listados como ilustraciones impresas) se descartan: no son
  figuritas coleccionables, son páginas decorativas del álbum.
- Coca-Cola: se incluye solo la Versión 2 (Latinoamérica) porque es la que aplica a Argentina.
  Las otras se pueden agregar después como variantes regionales.
- Extra Stickers: 20 jugadores × 4 colores = 80 entradas, agrupadas por parallel_set.
"""

import json
import re
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Metadata de las 48 selecciones (orden alfabético por código Panini)
# ─────────────────────────────────────────────────────────────────────────────

TEAMS = [
    {"code": "ALG", "name_en": "Algeria",                  "name_es": "Argelia",              "confederation": "CAF"},
    {"code": "ARG", "name_en": "Argentina",                "name_es": "Argentina",            "confederation": "CONMEBOL"},
    {"code": "AUS", "name_en": "Australia",                "name_es": "Australia",            "confederation": "AFC"},
    {"code": "AUT", "name_en": "Austria",                  "name_es": "Austria",              "confederation": "UEFA"},
    {"code": "BEL", "name_en": "Belgium",                  "name_es": "Bélgica",              "confederation": "UEFA"},
    {"code": "BIH", "name_en": "Bosnia and Herzegovina",   "name_es": "Bosnia y Herzegovina", "confederation": "UEFA"},
    {"code": "BRA", "name_en": "Brazil",                   "name_es": "Brasil",               "confederation": "CONMEBOL"},
    {"code": "CAN", "name_en": "Canada",                   "name_es": "Canadá",               "confederation": "CONCACAF", "is_host": True},
    {"code": "CIV", "name_en": "Ivory Coast",              "name_es": "Costa de Marfil",      "confederation": "CAF"},
    {"code": "COD", "name_en": "Congo DR",                 "name_es": "RD del Congo",         "confederation": "CAF"},
    {"code": "COL", "name_en": "Colombia",                 "name_es": "Colombia",             "confederation": "CONMEBOL"},
    {"code": "CPV", "name_en": "Cape Verde",               "name_es": "Cabo Verde",           "confederation": "CAF"},
    {"code": "CRO", "name_en": "Croatia",                  "name_es": "Croacia",              "confederation": "UEFA"},
    {"code": "CUW", "name_en": "Curaçao",                  "name_es": "Curazao",              "confederation": "CONCACAF"},
    {"code": "CZE", "name_en": "Czechia",                  "name_es": "Chequia",              "confederation": "UEFA"},
    {"code": "ECU", "name_en": "Ecuador",                  "name_es": "Ecuador",              "confederation": "CONMEBOL"},
    {"code": "EGY", "name_en": "Egypt",                    "name_es": "Egipto",               "confederation": "CAF"},
    {"code": "ENG", "name_en": "England",                  "name_es": "Inglaterra",           "confederation": "UEFA"},
    {"code": "ESP", "name_en": "Spain",                    "name_es": "España",               "confederation": "UEFA"},
    {"code": "FRA", "name_en": "France",                   "name_es": "Francia",              "confederation": "UEFA"},
    {"code": "GER", "name_en": "Germany",                  "name_es": "Alemania",             "confederation": "UEFA"},
    {"code": "GHA", "name_en": "Ghana",                    "name_es": "Ghana",                "confederation": "CAF"},
    {"code": "HAI", "name_en": "Haiti",                    "name_es": "Haití",                "confederation": "CONCACAF"},
    {"code": "IRN", "name_en": "Iran",                     "name_es": "Irán",                 "confederation": "AFC"},
    {"code": "IRQ", "name_en": "Iraq",                     "name_es": "Irak",                 "confederation": "AFC"},
    {"code": "JOR", "name_en": "Jordan",                   "name_es": "Jordania",             "confederation": "AFC"},
    {"code": "JPN", "name_en": "Japan",                    "name_es": "Japón",                "confederation": "AFC"},
    {"code": "KOR", "name_en": "Korea Republic",           "name_es": "Corea del Sur",        "confederation": "AFC"},
    {"code": "KSA", "name_en": "Saudi Arabia",             "name_es": "Arabia Saudita",       "confederation": "AFC"},
    {"code": "MAR", "name_en": "Morocco",                  "name_es": "Marruecos",            "confederation": "CAF"},
    {"code": "MEX", "name_en": "Mexico",                   "name_es": "México",               "confederation": "CONCACAF", "is_host": True},
    {"code": "NED", "name_en": "Netherlands",              "name_es": "Países Bajos",         "confederation": "UEFA"},
    {"code": "NOR", "name_en": "Norway",                   "name_es": "Noruega",              "confederation": "UEFA"},
    {"code": "NZL", "name_en": "New Zealand",              "name_es": "Nueva Zelanda",        "confederation": "OFC"},
    {"code": "PAN", "name_en": "Panama",                   "name_es": "Panamá",               "confederation": "CONCACAF"},
    {"code": "PAR", "name_en": "Paraguay",                 "name_es": "Paraguay",             "confederation": "CONMEBOL"},
    {"code": "POR", "name_en": "Portugal",                 "name_es": "Portugal",             "confederation": "UEFA"},
    {"code": "QAT", "name_en": "Qatar",                    "name_es": "Catar",                "confederation": "AFC"},
    {"code": "RSA", "name_en": "South Africa",             "name_es": "Sudáfrica",            "confederation": "CAF"},
    {"code": "SCO", "name_en": "Scotland",                 "name_es": "Escocia",              "confederation": "UEFA"},
    {"code": "SEN", "name_en": "Senegal",                  "name_es": "Senegal",              "confederation": "CAF"},
    {"code": "SUI", "name_en": "Switzerland",              "name_es": "Suiza",                "confederation": "UEFA"},
    {"code": "SWE", "name_en": "Sweden",                   "name_es": "Suecia",               "confederation": "UEFA"},
    {"code": "TUN", "name_en": "Tunisia",                  "name_es": "Túnez",                "confederation": "CAF"},
    {"code": "TUR", "name_en": "Türkiye",                  "name_es": "Turquía",              "confederation": "UEFA"},
    {"code": "URU", "name_en": "Uruguay",                  "name_es": "Uruguay",              "confederation": "CONMEBOL"},
    {"code": "USA", "name_en": "United States",            "name_es": "Estados Unidos",       "confederation": "CONCACAF", "is_host": True},
    {"code": "UZB", "name_en": "Uzbekistan",               "name_es": "Uzbekistán",           "confederation": "AFC"},
]

assert len(TEAMS) == 48, f"Esperaba 48 selecciones, hay {len(TEAMS)}"

# Diccionario auxiliar para lookup rápido
TEAM_BY_CODE = {t["code"]: t for t in TEAMS}


# ─────────────────────────────────────────────────────────────────────────────
# Datos de jugadores por equipo (parseado del checklist Cartophilic)
# Limpieza aplicada:
#   - Typos del fuente corregidos: POR-11 duplicado → POR-14 João Neves,
#     KAS-12 → KSA-12, "Morrocco"/"Morrocco" → omitido del label.
#   - Algunos números tenían inconsistencias menores ("Marc" vs "Maric") respetadas como están
#     en el blog (el usuario va a poder corregir cuando vea su figurita).
# ─────────────────────────────────────────────────────────────────────────────

# Para mantener el script compacto, los datos de jugadores se cargan desde un raw block.
# Formato: cada línea es "CODE-N. Nombre del jugador" (sin "(Team)" sufix).

PLAYERS_RAW = """
ALG-2. Alexis Guendouz
ALG-3. Ramy Bensebaini
ALG-4. Youcef Atal
ALG-5. Rayan Aït-Nouri
ALG-6. Mohamed Amine Tougai
ALG-7. Aïssa Mandi
ALG-8. Ismael Bennacer
ALG-9. Houssem Aquar
ALG-10. Hicham Boudaoui
ALG-11. Ramiz Zerrouki
ALG-12. Nabil Bentalab
ALG-14. Farés Chaibi
ALG-15. Riyad Mahrez
ALG-16. Said Benrhama
ALG-17. Anis Hadj Moussa
ALG-18. Amine Gouiri
ALG-19. Baghdad Bounedjah
ALG-20. Mohammed Amoura

ARG-2. Emiliano Martinez
ARG-3. Nahuel Molina
ARG-4. Cristian Romero
ARG-5. Nicolas Otamendi
ARG-6. Nicolas Tagliafico
ARG-7. Leonardo Balerdi
ARG-8. Enzo Fernandez
ARG-9. Alexis Mac Allister
ARG-10. Rodrigo De Paul
ARG-11. Exequiel Palacios
ARG-12. Leandro Paredes
ARG-14. Nico Paz
ARG-15. Franco Mastantuono
ARG-16. Nico Gonzalez
ARG-17. Lionel Messi
ARG-18. Lautaro Martinez
ARG-19. Julian Alvarez
ARG-20. Giuliano Simeone

AUS-2. Mathew Ryan
AUS-3. Joe Gauci
AUS-4. Harry Souttar
AUS-5. Alessandro Circati
AUS-6. Jordan Bos
AUS-7. Aziz Behich
AUS-8. Cameron Burgess
AUS-9. Lewis Miller
AUS-10. Milos Degenek
AUS-11. Jackson Irvine
AUS-12. Riley McGree
AUS-14. Aiden O'Neill
AUS-15. Connor Metcalfe
AUS-16. Patrick Yazbek
AUS-17. Craig Goodwin
AUS-18. Kusini Vengi
AUS-19. Nestory Irankunda
AUS-20. Mohamed Touré

AUT-2. Alexander Schlager
AUT-3. Patrick Pentz
AUT-4. David Alaba
AUT-5. Kevin Danso
AUT-6. Philipp Lienhart
AUT-7. Stefan Bosch
AUT-8. Phillipp Mwene
AUT-9. Alexander Prass
AUT-10. Xavier Schlager
AUT-11. Marcel Sabitzer
AUT-12. Konrad Laimer
AUT-14. Florian Grillitsch
AUT-15. Nicolas Seiwald
AUT-16. Romano Schmid
AUT-17. Patrick Wimmer
AUT-18. Christoph Baumgartner
AUT-19. Michael Gregoritsch
AUT-20. Marko Arnautović

BEL-2. Thibaut Courtois
BEL-3. Arthur Theate
BEL-4. Timothy Castagne
BEL-5. Zeno Debast
BEL-6. Brandon Mechele
BEL-7. Maxim De Cuyper
BEL-8. Thomas Meunier
BEL-9. Youri Tielemans
BEL-10. Amadou Onana
BEL-11. Nicolas Raskin
BEL-12. Alexis Saelemaekers
BEL-14. Hans Vanaken
BEL-15. Kevin De Bruyne
BEL-16. Jérémy Doku
BEL-17. Charles De Ketelaere
BEL-18. Leandro Trossard
BEL-19. Loïs Openda
BEL-20. Romelu Lukaku

BIH-2. Nikola Vasilj
BIH-3. Amer Dedic
BIH-4. Sead Kolasinac
BIH-5. Tarik Muharemovic
BIH-6. Nihad Mujakic
BIH-7. Nikola Katic
BIH-8. Amir Hadziahmetovic
BIH-9. Benjamin Tahirovic
BIH-10. Armin Gigovic
BIH-11. Ivan Sunjic
BIH-12. Ivan Basic
BIH-14. Dzenis Burnic
BIH-15. Esmir Bajraktarevic
BIH-16. Amar Memic
BIH-17. Ermedin Demirovic
BIH-18. Edin Dzeko
BIH-19. Samed Bazdar
BIH-20. Haris Tabakovic

BRA-2. Alisson
BRA-3. Bento
BRA-4. Marquinhos
BRA-5. Éder Militão
BRA-6. Gabriel Magalhães
BRA-7. Danilo
BRA-8. Wesley
BRA-9. Lucas Paquetá
BRA-10. Casemiro
BRA-11. Bruno Guimarães
BRA-12. Luiz Henrique
BRA-14. Vinicius Júnior
BRA-15. Rodrygo
BRA-16. João Pedro
BRA-17. Matheus Cunha
BRA-18. Gabriel Martinelli
BRA-19. Raphinha
BRA-20. Estévão

CAN-2. Dayne St.Clair
CAN-3. Alphonso Davies
CAN-4. Alistair Johnston
CAN-5. Samuel Adekugbe
CAN-6. Riche Larvea
CAN-7. Derek Cornelius
CAN-8. Moïse Bombito
CAN-9. Kamal Miller
CAN-10. Stephen Eustáquio
CAN-11. Ismaël Koné
CAN-12. Jonathan Osorio
CAN-14. Jacob Shaffelburg
CAN-15. Mathieu Choinière
CAN-16. Niko Sigur
CAN-17. Tajon Buchanan
CAN-18. Liam Millar
CAN-19. Cyle Larin
CAN-20. Jonathan David

CIV-2. Yahia Fofana
CIV-3. Ghislain Konan
CIV-4. Wilfried Singo
CIV-5. Odilon Kossounou
CIV-6. Evan Ndicka
CIV-7. Willy Boly
CIV-8. Emmanuel Agbadou
CIV-9. Ousmane Diomande
CIV-10. Franck Kessie
CIV-11. Seko Fofana
CIV-12. Ibrahim Sangare
CIV-14. Jean-Philippe Gbamin
CIV-15. Amad Diallo
CIV-16. Sébastien Haller
CIV-17. Simon Adringa
CIV-18. Yan Diomande
CIV-19. Evann Guessand
CIV-20. Oumar Diakite

COD-2. Lionel Mpasi
COD-3. Aaron Wan-Bissaka
COD-4. Axel Tuanzebe
COD-5. Arthur Masuaku
COD-6. Chancel Mbemba
COD-7. Joris Kayembe
COD-8. Charles Pickel
COD-9. Ngal'ayel Mukau
COD-10. Edo Kayembe
COD-11. Samuel Moutoussamy
COD-12. Noah Sadiki
COD-14. Théo Bongonda
COD-15. Meschak Elia
COD-16. Yoane Wissa
COD-17. Brian Cipenga
COD-18. Fiston Mayele
COD-19. Cédric Bakambu
COD-20. Nathanaël Mbuku

COL-2. Camilo Vargas
COL-3. David Ospina
COL-4. Dávinson Sánchez
COL-5. Yerry Mina
COL-6. Daniel Munoz
COL-7. Johan Mojica
COL-8. Jhon Lucumí
COL-9. Santiago Arias
COL-10. Jefferson Lerma
COL-11. Kevin Castaño
COL-12. Richard Rios
COL-14. James Rodriguez
COL-15. Juan Fernando Quintero
COL-16. Jorge Carrascal
COL-17. Jhon Arias
COL-18. Jhon Cordova
COL-19. Luis Suarez
COL-20. Luis Diaz

CPV-2. Vozinha
CPV-3. Logan Costa
CPV-4. Pico
CPV-5. Diney
CPV-6. Steven Moreira
CPV-7. Wagner Pina
CPV-8. Joao Paulo
CPV-9. Yannick Semedo
CPV-10. Kevin Pina
CPV-11. Patrick Andrade
CPV-12. Jamiro Monteiro
CPV-14. Deroy Duarte
CPV-15. Garry Rodrigues
CPV-16. Jovane Cabral
CPV-17. Ryan Mendes
CPV-18. Dailon Livramento
CPV-19. Willy Semedo
CPV-20. Bebe

CRO-2. Dominik Livaković
CRO-3. Duje Caleta-Car
CRO-4. Josko Gvardiol
CRO-5. Josip Stanišić
CRO-6. Luka Vušković
CRO-7. Josip Sutalo
CRO-8. Kristijan Jakic
CRO-9. Luka Modrić
CRO-10. Mateo Kovacic
CRO-11. Martin Baturina
CRO-12. Lovro Majer
CRO-14. Mario Pasalic
CRO-15. Petar Sucic
CRO-16. Ivan Perišić
CRO-17. Marco Pasalic
CRO-18. Ante Budimir
CRO-19. Andrej Kramarić
CRO-20. Franjo Ivanovic

CUW-2. Eloy Room
CUW-3. Armando Obispo
CUW-4. Sherel Floranus
CUW-5. Jurien Gaari
CUW-6. Joshua Brenet
CUW-7. Roshon Van Eijma
CUW-8. Shurandy Sambo
CUW-9. Livano Comenencia
CUW-10. Godfried Roemeratoe
CUW-11. Juninho Bacuna
CUW-12. Leandro Bacuna
CUW-14. Tahith Chong
CUW-15. Kenji Gorre
CUW-16. Jearl Margaritha
CUW-17. Jurgen Locadia
CUW-18. Jeremy Antonisse
CUW-19. Gervane Kastaneer
CUW-20. Sontje Hansen

CZE-2. Matej Kovar
CZE-3. Jindrich Stanek
CZE-4. Ladislav Krejci
CZE-5. Vladimir Coufal
CZE-6. Jaroslav Zeleny
CZE-7. Tomas Holes
CZE-8. David Zima
CZE-9. Michal Sadilek
CZE-10. Lukas Provod
CZE-11. Lukas Cerv
CZE-12. Tomas Soucek
CZE-14. Pavel Sulc
CZE-15. Matej Vydra
CZE-16. Vasil Kusej
CZE-17. Tomas Chory
CZE-18. Vacilav Cerny
CZE-19. Adam Hlozek
CZE-20. Patrik Schick

ECU-2. Hernán Galíndez
ECU-3. Gonzalo Valle
ECU-4. Piero Hincapié
ECU-5. Pervis Estupiñán
ECU-6. Willian Pacho
ECU-7. Ángelo Preciado
ECU-8. Joel Ordóñez
ECU-9. Moises Caicedo
ECU-10. Alan Franco
ECU-11. Kendry Paez
ECU-12. Pedro Vite
ECU-14. John Veboah
ECU-15. Leonardo Campana
ECU-16. Gonzalo Plata
ECU-17. Nilson Angulo
ECU-18. Alan Minda
ECU-19. Kevin Rodriguez
ECU-20. Enner Valencia

EGY-2. Mohamed El Shenawy
EGY-3. Mohamed Hany
EGY-4. Mohamed Hamdy
EGY-5. Yasser Ibrahim
EGY-6. Khaled Sobhi
EGY-7. Ramy Rabia
EGY-8. Hossam Abdelmaguid
EGY-9. Ahmed Fatouh
EGY-10. Marwan Attia
EGY-11. Zizo
EGY-12. Hamdy Fathy
EGY-14. Mohamed Lasheen
EGY-15. Emam Ashour
EGY-16. Osama Faisal
EGY-17. Mohamed Salah
EGY-18. Mostafa Mohamed
EGY-19. Trezeguet
EGY-20. Omar Marsmoush

ENG-2. Jordan Pickford
ENG-3. John Stones
ENG-4. Marc Guéhi
ENG-5. Ezri Konsa
ENG-6. Trent Alexander-Arnold
ENG-7. Reece James
ENG-8. Dan Burn
ENG-9. Jordan Henderson
ENG-10. Declan Rice
ENG-11. Jude Bellingham
ENG-12. Cole Palmer
ENG-14. Morgan Rogers
ENG-15. Anthony Gordon
ENG-16. Phil Foden
ENG-17. Bukayo Saka
ENG-18. Harry Kane
ENG-19. Marcus Rashford
ENG-20. Ollie Watkins

ESP-2. Unai Simon
ESP-3. Robin Le Normand
ESP-4. Aymeric Laporte
ESP-5. Dean Huijsen
ESP-6. Pedro Porro
ESP-7. Dani Carvajal
ESP-8. Marc Cucurella
ESP-9. Martín Zubimendi
ESP-10. Rodri
ESP-11. Pedri
ESP-12. Fabian Ruiz
ESP-14. Mikel Merino
ESP-15. Lamine Yamal
ESP-16. Dani Olmo
ESP-17. Nico Williams
ESP-18. Ferran Torres
ESP-19. Álvaro Morata
ESP-20. Mikel Oyarzabal

FRA-2. Mike Maignan
FRA-3. Theo Hernandez
FRA-4. William Saliba
FRA-5. Jules Kounde
FRA-6. Ibrahima Konate
FRA-7. Dayot Upamecano
FRA-8. Lucas Digne
FRA-9. Aurélien Tchouaméni
FRA-10. Eduardo Camavinga
FRA-11. Manu Kone
FRA-12. Adrien Rabiot
FRA-14. Michael Olise
FRA-15. Ousmane Dembele
FRA-16. Bradley Barcola
FRA-17. Désiré Doué
FRA-18. Kingsley Coman
FRA-19. Hugo Ekitike
FRA-20. Kylian Mbappe

GER-2. Marc-André ter Stegen
GER-3. Jonathan Tah
GER-4. David Raum
GER-5. Nico Schlotterbeck
GER-6. Antonio Rüdiger
GER-7. Waldemar Anton
GER-8. Ridle Baku
GER-9. Maximilian Mittelstadt
GER-10. Joshua Kimmich
GER-11. Florian Wirtz
GER-12. Felix Nmecha
GER-14. Leon Goretzka
GER-15. Jamal Musiala
GER-16. Serge Gnabry
GER-17. Kai Havertz
GER-18. Leroy Sane
GER-19. Karim Adeyemi
GER-20. Nick Woltemade

GHA-2. Lawrence Ati Zigi
GHA-3. Tariq Lamptey
GHA-4. Mohammed Salisu
GHA-5. Alidu Seidu
GHA-6. Alexander Djiku
GHA-7. Gideon Mensah
GHA-8. Caleb Yirenkyi
GHA-9. Abdul Issahaku Fatawu
GHA-10. Thomas Partey
GHA-11. Salis Abdul Samed
GHA-12. Kamaldeen Sulemana
GHA-14. Mohammed Kudus
GHA-15. Inaki Williams
GHA-16. Jordan Ayew
GHA-17. Andrew Ayew
GHA-18. Joseph Paintsil
GHA-19. Osman Bukari
GHA-20. Antoine Semenyo

HAI-2. Johny Placide
HAI-3. Carlens Arcus
HAI-4. Martin Expérience
HAI-5. Jean-Kevin Duverne
HAI-6. Ricardo Adé
HAI-7. Duke Lacroix
HAI-8. Garven Metusala
HAI-9. Hannes Delcroix
HAI-10. Leverton Pierre
HAI-11. Danley Jean Jacques
HAI-12. Jean-Ricner Bellegarde
HAI-14. Christopher Attys
HAI-15. Derrick Etienne Jr.
HAI-16. Josue Casimir
HAI-17. Ruben Providence
HAI-18. Duckens Nazon
HAI-19. Louicius Deedson
HAI-20. Frantzdy Pierrot

IRN-2. Alirez Beiranvand
IRN-3. Morteza Pouraliganji
IRN-4. Ehsan Hajsafi
IRN-5. Milad Mohammadi
IRN-6. Shojae Khalilzadeh
IRN-7. Ramin Rezaeian
IRN-8. Hossein Kanaani
IRN-9. Sadegh Moharrami
IRN-10. Saleh Hardani
IRN-11. Saeed Ezatolahi
IRN-12. Saman Ghoddos
IRN-14. Omid Noorafkan
IRN-15. Roozbeh Cheshmi
IRN-16. Mohammad Mohebi
IRN-17. Sardar Azmoun
IRN-18. Mehdi Taremi
IRN-19. Alireza Jahanbakhsh
IRN-20. Ali Gholizadeh

IRQ-2. Jalal Hassan
IRQ-3. Rebin Sulaka
IRQ-4. Hussein Ali
IRQ-5. Akam Hashem
IRQ-6. Merchas Doski
IRQ-7. Zaid Tahseen
IRQ-8. Manaf Younis
IRQ-9. Zidane Iqbal
IRQ-10. Amir Al-Ammari
IRQ-11. Ibrahim Bavesh
IRQ-12. Ali Jasim
IRQ-14. Youssef Amyn
IRQ-15. Aimar Sher
IRQ-16. Marko Farji
IRQ-17. Osama Rashid
IRQ-18. Ali Al-Hamadi
IRQ-19. Aymen Hussein
IRQ-20. Mohanad Ali

JOR-2. Yazeed Abulaila
JOR-3. Ihsan Haddad
JOR-4. Mohammad Abu Hashish
JOR-5. Yazan Al-Arab
JOR-6. Abdallah Nasib
JOR-7. Saleem Obaid
JOR-8. Mohammad Abualnadi
JOR-9. Ibrahim Saadeh
JOR-10. Nizar Al-Rashdan
JOR-11. Noor Al-Rawabdeh
JOR-12. Mohannad Abu Taha
JOR-14. Amer Jamous
JOR-15. Mousa Al-Taamari
JOR-16. Yazan Al-Naimat
JOR-17. Mahmoud Al-Mardi
JOR-18. Ali Olwan
JOR-19. Mohammad Abu Zrayq
JOR-20. Ibrahim Sabra

JPN-2. Zion Suzuki
JPN-3. Henry Heroki Mochizuki
JPN-4. Ayumu Seko
JPN-5. Junnosuke Suzuki
JPN-6. Shogo Taniguchi
JPN-7. Tsuyoshi Watanabe
JPN-8. Kaishu Sano
JPN-9. Yuki Soma
JPN-10. Ao Tanaka
JPN-11. Daichi Kamada
JPN-12. Takefusa Kubo
JPN-14. Ritsu Doan
JPN-15. Keito Nakamura
JPN-16. Takumi Minamino
JPN-17. Shuto Machino
JPN-18. Junya Ito
JPN-19. Koki Ogawa
JPN-20. Ayase Ueda

KOR-2. Hyeon-woo Jo
KOR-3. Seung-Gyu Kim
KOR-4. Min-jae Kim
KOR-5. Yu-min Cho
KOR-6. Young-woo Seol
KOR-7. Han-beom Lee
KOR-8. Tae-seok Lee
KOR-9. Myung-jae Lee
KOR-10. Jae-sung Lee
KOR-11. In-beom Hwang
KOR-12. Kang-in Lee
KOR-14. Seung-ho Paik
KOR-15. Jens Castrop
KOR-16. Dongg-yeong Lee
KOR-17. Gue-sung Cho
KOR-18. Heung-min Son
KOR-19. Hee-chan Hwang
KOR-20. Hyeon-Gyu Oh

KSA-2. Nawaf Alaqidi
KSA-3. Abdulrahman Al-Sanbi
KSA-4. Saud Abdulhamid
KSA-5. Nawaf Bouwashl
KSA-6. Jihad Thakri
KSA-7. Moteb Al-Harbi
KSA-8. Hassan Altambakti
KSA-9. Musab Aljuwayr
KSA-10. Ziyad Aljohani
KSA-11. Abdullah Alkhaibari
KSA-12. Nasser Aldawsari
KSA-14. Saleh Abu Alshamat
KSA-15. Marwan Alsahafi
KSA-16. Salem Aldawsari
KSA-17. Abdulrahman Al-Aboud
KSA-18. Feras Akbrikan
KSA-19. Saleh Alshehri
KSA-20. Abdullah Al-Hamdan

MAR-2. Yassine Bounou
MAR-3. Munir El Kajoui
MAR-4. Achraf Hakimi
MAR-5. Noussair Mazraoui
MAR-6. Nayef Aguerd
MAR-7. Roman Saiss
MAR-8. Jawad El Yamio
MAR-9. Adam Masina
MAR-10. Sofyan Amrabat
MAR-11. Azzedine Ounahi
MAR-12. Eliesse Ben Seghir
MAR-14. Bilal El Khannouss
MAR-15. Ismael Saibari
MAR-16. Youssef En-Nesyri
MAR-17. Abde Ezzalzouli
MAR-18. Soufiane Rahimi
MAR-19. Brahim Diaz
MAR-20. Ayoub El Kaabi

MEX-2. Luis Malagón
MEX-3. Johan Vasquez
MEX-4. Jorge Sánchez
MEX-5. Cesar Montes
MEX-6. Jesus Gallardo
MEX-7. Israel Reyes
MEX-8. Diego Lainez
MEX-9. Carlos Rodriguez
MEX-10. Edson Alvarez
MEX-11. Orbelin Pineda
MEX-12. Marcel Ruiz
MEX-14. Érick Sánchez
MEX-15. Hirving Lozano
MEX-16. Santiago Giménez
MEX-17. Raúl Jiménez
MEX-18. Alexis Vega
MEX-19. Roberto Alvarado
MEX-20. Cesar Huerta

NED-2. Bart Verbruggen
NED-3. Virgil van Dijk
NED-4. Micky van de Ven
NED-5. Jurien Timber
NED-6. Denzel Dumfries
NED-7. Nathan Aké
NED-8. Jereme Frimpong
NED-9. Jan Paul van Hecke
NED-10. Tijjani Reijnders
NED-11. Ryan Gravenberch
NED-12. Teun Koopmeiners
NED-14. Frenkie de Jong
NED-15. Xavi Simons
NED-16. Justin Kluivert
NED-17. Memphis Depay
NED-18. Donyell Malen
NED-19. Wout Weghorst
NED-20. Cody Gakpo

NOR-2. Orjan Nyland
NOR-3. Julian Ryerson
NOR-4. Leo Ostigård
NOR-5. Kristoffer Vassbakk Ajer
NOR-6. Marcus Holmgren Pedersen
NOR-7. David Møller Wolfe
NOR-8. Torbjørn Heggem
NOR-9. Morten Thorsby
NOR-10. Martin Ødegaard
NOR-11. Sander Berge
NOR-12. Andreas Schjelderup
NOR-14. Patrick Berg
NOR-15. Erling Haaland
NOR-16. Alexander Sørloth
NOR-17. Aron Dønnum
NOR-18. Jorgen Strand Larsen
NOR-19. Antonio Nusa
NOR-20. Oscar Bobb

NZL-2. Max Crocombe Payne
NZL-3. Alex Paulsen
NZL-4. Michael Boxall
NZL-5. Liberato Cacace
NZL-6. Tim Payne
NZL-7. Tyler Bindon
NZL-8. Francis de Vries
NZL-9. Finn Surman
NZL-10. Joe Bell
NZL-11. Sarpreet Singh
NZL-12. Ryan Thomas
NZL-14. Matthew Garbett
NZL-15. Marko Stamenić
NZL-16. Ben Old
NZL-17. Chris Wood
NZL-18. Elijah Just
NZL-19. Callum McCowatt
NZL-20. Kosta Barbarouses

PAN-2. Orlando Mosquera
PAN-3. Luis Mejia
PAN-4. Fidel Escobar
PAN-5. Andres Andrade
PAN-6. Michael Amir Murillo
PAN-7. Eric Davis
PAN-8. Jose Cordoba
PAN-9. Cesar Blackman
PAN-10. Cristian Martinez
PAN-11. Aníbal Godoy
PAN-12. Adalberto Carrasquilla
PAN-14. Édgar Bárcenas
PAN-15. Carlos Harvey
PAN-16. Ismael Díaz
PAN-17. Jose Fajardo
PAN-18. Cecilio Waterman
PAN-19. Jose Luiz Rodriguez
PAN-20. Alberto Quintero

PAR-2. Roberto Fernandez
PAR-3. Orlando Gill
PAR-4. Gustavo Gomez
PAR-5. Fabián Balbuena
PAR-6. Juan José Cáceres
PAR-7. Omar Alderete
PAR-8. Junior Alonso
PAR-9. Mathías Villasanti
PAR-10. Diego Gomez
PAR-11. Damián Bobadilla
PAR-12. Andres Cubas
PAR-14. Matias Galarza Fonda
PAR-15. Julio Enciso
PAR-16. Alejandro Romero Gamarra
PAR-17. Miguel Almirón
PAR-18. Ramon Sosa
PAR-19. Angel Romero
PAR-20. Antonio Sanabria

POR-2. Diogo Costa
POR-3. Jose Sa
POR-4. Ruben Dias
POR-5. João Cancelo
POR-6. Diogo Dalot
POR-7. Nuno Mendes
POR-8. Gonçalo Inácio
POR-9. Bernardo Silva
POR-10. Bruno Fernandes
POR-11. Ruben Neves
POR-12. Vitinha
POR-14. João Neves
POR-15. Cristiano Ronaldo
POR-16. Francisco Trincao
POR-17. João Felix
POR-18. Gonçalo Ramos
POR-19. Pedro Neto
POR-20. Rafael Leão

QAT-2. Meshaal Barsham
QAT-3. Sultan Albrake
QAT-4. Lucas Mendes
QAT-5. Homam Ahmed
QAT-6. Boualem Khoukhi
QAT-7. Pedro Miguel
QAT-8. Tarek Salman
QAT-9. Mohamed Al-Mannai
QAT-10. Karim Boudiaf
QAT-11. Assim Madibo
QAT-12. Ahmed Fatehi
QAT-14. Mohammed Waad
QAT-15. Abdulaziz Hatem
QAT-16. Hassan Al-Haydos
QAT-17. Edmilson Junior
QAT-18. Akram Hassan Afif
QAT-19. Ahmed Al Ganehi
QAT-20. Almoez Ali

RSA-2. Ronwen Williams
RSA-3. Sipho Chaine
RSA-4. Aubrey Modiba
RSA-5. Samukele Kabini
RSA-6. Mbekezeli Mbokazi
RSA-7. Khulumani Ndamane
RSA-8. Siyabonga Ngezana
RSA-9. Khuliso Mudau
RSA-10. Nkosinathi Sibisi
RSA-11. Teboho Mokoena
RSA-12. Thalente Mbatha
RSA-14. Bathasi Aubaas
RSA-15. Yaya Sithole
RSA-16. Sipho Mbule
RSA-17. Lyle Foster
RSA-18. Iqraam Rayners
RSA-19. Mohau Nkota
RSA-20. Oswin Appollis

SCO-2. Angus Gunn
SCO-3. Jack Hendry
SCO-4. Kieran Tierney
SCO-5. Aaron Hickey
SCO-6. Andrew Robertson
SCO-7. Scott McKenna
SCO-8. John Souttar
SCO-9. Anthony Ralston
SCO-10. Grant Hanley
SCO-11. Scott McTominay
SCO-12. Billy Gilmour
SCO-14. Lewis Ferguson
SCO-15. Ryan Christie
SCO-16. Kenny McLean
SCO-17. John McGinn
SCO-18. Lyndon Dykes
SCO-19. Che Adams
SCO-20. Ben Gannon-Doak

SEN-2. Eduardo Mendy
SEN-3. Yehvann Diouf
SEN-4. Moussa Niakhaté
SEN-5. Abdoulaye Seck
SEN-6. Ismail Jakobs
SEN-7. El Hadji Malick Diouf
SEN-8. Kalidou Koulibaly
SEN-9. Idrissa Gana Gueye
SEN-10. Pape Matar Sarr
SEN-11. Pape Gueye
SEN-12. Habib Diarra
SEN-14. Lamine Camara
SEN-15. Sadio Mane
SEN-16. Ismaïla Sarr
SEN-17. Boulaye Dia
SEN-18. Iliman Ndiaye
SEN-19. Nicolas Jackson
SEN-20. Krepin Diatta

SUI-2. Gregor Kobel
SUI-3. Yvon Mvogo
SUI-4. Manuel Akanji
SUI-5. Ricardo Rodriguez
SUI-6. Nico Elvedi
SUI-7. Aurèle Amenda
SUI-8. Silvan Widmer
SUI-9. Granit Xhaka
SUI-10. Denis Zakaria
SUI-11. Remo Freuler
SUI-12. Fabian Rieder
SUI-14. Ardon Jashari
SUI-15. Johan Manzambi
SUI-16. Michel Aebischer
SUI-17. Breel Embolo
SUI-18. Ruben Vargas
SUI-19. Dan Ndoye
SUI-20. Zeki Amdouni

SWE-2. Victor Johansson
SWE-3. Isak Hien
SWE-4. Gabriel Gudmundsson
SWE-5. Emil Holm
SWE-6. Victor Nilsson Lindelöf
SWE-7. Gustaf Lagerbielke
SWE-8. Lucas Bergvall
SWE-9. Hugo Larsson
SWE-10. Jesper Karlström
SWE-11. Yasin Ayari
SWE-12. Mattias Svanberg
SWE-14. Daniel Svensson
SWE-15. Ken Sema
SWE-16. Roony Bardghji
SWE-17. Dejan Kulusevski
SWE-18. Anthony Elanga
SWE-19. Alexander Isak
SWE-20. Viktor Gyökeres

TUN-2. Bechir Ben Said
TUN-3. Aymen Dahmen
TUN-4. Van Valery
TUN-5. Montassar Talbi
TUN-6. Yassine Meriah
TUN-7. Ali Abdi
TUN-8. Dylan Bronn
TUN-9. Ellyes Skhiri
TUN-10. Aissa Laidouni
TUN-11. Ferjani Sassi
TUN-12. Mohamed Ali Ben Romdhane
TUN-14. Hannibal Mejbri
TUN-15. Elias Achouri
TUN-16. Elias Saad
TUN-17. Hazem Mastouri
TUN-18. Ismael Gharbi
TUN-19. Sayfallah Ltaief
TUN-20. Naim Sliti

TUR-2. Ugurcan Cakir
TUR-3. Mert Muldur
TUR-4. Zeki Celik
TUR-5. Abdulkerim Bardakci
TUR-6. Caglar Soyunku
TUR-7. Merih Demiral
TUR-8. Ferdi Kadioglu
TUR-9. Kaan Ayhan
TUR-10. Ismail Yuksek
TUR-11. Hakan Calhanoglu
TUR-12. Orkun Kokcu
TUR-14. Arda Guler
TUR-15. Irfan Can Kahvecu
TUR-16. Yunus Akgun
TUR-17. Can Uzun
TUR-18. Baris Alper Yilmaz
TUR-19. Kerem Akturkoglu
TUR-20. Kenan Yildiz

URU-2. Sergio Rochet
URU-3. Santiago Mele
URU-4. Ronald Araujo
URU-5. José María Giménez
URU-6. Sebastian Caceres
URU-7. Mathias Olivera
URU-8. Guillermo Varela
URU-9. Nahitan Nandez
URU-10. Federico Valverde
URU-11. Giorgian De Arrascaeta
URU-12. Rodrigo Bentancur
URU-14. Manuel Ugarte
URU-15. Nicolás de la Cruz
URU-16. Maxi Araujo
URU-17. Darwin Núñez
URU-18. Federico Viñas
URU-19. Rodrigo Aguirre
URU-20. Facundo Pellistri

USA-2. Matt Freese
USA-3. Chris Richards
USA-4. Tim Ream
USA-5. Mark McKenzie
USA-6. Alex Freeman
USA-7. Antonee Robinson
USA-8. Tyler Adams
USA-9. Tanner Tessmann
USA-10. Weston McKennie
USA-11. Christian Roldan
USA-12. Timothy Weah
USA-14. Diego Luna
USA-15. Malim Tillman
USA-16. Christian Pulisic
USA-17. Brenden Aaronson
USA-18. Ricardo Pepi
USA-19. Haji Wright
USA-20. Folarin Balogun

UZB-2. Utkir Yusupov
UZB-3. Farrukh Savfiev
UZB-4. Sherzod Nasrullaev
UZB-5. Umar Eshmurodov
UZB-6. Husniddin Aliqulov
UZB-7. Rustamjon Ashurmatov
UZB-8. Khojiakbar Alijonov
UZB-9. Abdukodir Khusanov
UZB-10. Odiljon Hamrobekov
UZB-11. Otabek Shukurov
UZB-12. Jamshid Iskanderov
UZB-14. Azizbek Turgunboev
UZB-15. Khojimat Erkinov
UZB-16. Eldor Shomurodov
UZB-17. Oston Urunov
UZB-18. Jaloliddin Masharipov
UZB-19. Igor Sergeev
UZB-20. Abbosbek Fayzullaev
"""

# Extra Stickers (jugadores misteriosos, fuera del álbum, 4 variantes cada uno)
EXTRA_STICKER_PLAYERS = [
    ("Lionel Messi",        "ARG"),
    ("Jérémy Doku",         "BEL"),
    ("Vinícius Júnior",     "BRA"),
    ("Alphonso Davies",     "CAN"),
    ("Luis Díaz",           "COL"),
    ("Luka Modrić",         "CRO"),
    ("Moisés Caicedo",      "ECU"),
    ("Mohamed Salah",       "EGY"),
    ("Jude Bellingham",     "ENG"),
    ("Kylian Mbappé",       "FRA"),
    ("Florian Wirtz",       "GER"),
    ("Raúl Jiménez",        "MEX"),
    ("Achraf Hakimi",       "MAR"),
    ("Cody Gakpo",          "NED"),
    ("Erling Haaland",      "NOR"),
    ("Cristiano Ronaldo",   "POR"),
    ("Heung-min Son",       "KOR"),
    ("Lamine Yamal",        "ESP"),
    ("Christian Pulisic",   "USA"),
    ("Federico Valverde",   "URU"),
]

# Coca-Cola Versión 2 (Latinoamérica) — la versión que se vende en Argentina
COCA_COLA_LATAM = [
    ("CC1",  "Lamine Yamal",        "ESP"),
    ("CC2",  "Joshua Kimmich",      "GER"),
    ("CC3",  "Harry Kane",          "ENG"),
    ("CC4",  "Santiago Giménez",    "MEX"),
    ("CC5",  "Josko Gvardiol",      "CRO"),
    ("CC6",  "Federico Valverde",   "URU"),
    ("CC7",  "Jefferson Lerma",     "COL"),
    ("CC8",  "Enner Valencia",      "ECU"),
    ("CC9",  "Gabriel Magalhães",   "BRA"),
    ("CC10", "Virgil van Dijk",     "NED"),
    ("CC11", "Alphonso Davies",     "CAN"),
    ("CC12", "Emiliano Martinez",   "ARG"),
    ("CC13", "Raúl Jiménez",        "MEX"),
    ("CC14", "Lautaro Martínez",    "ARG"),
]

# Historia del Mundial — figuritas FWC-9 a FWC-19 (las "printed in album" se omiten)
FWC_HISTORY = [
    ("FWC-9",  "Team Photo (Italy 1934)"),
    ("FWC-10", "Team Photo (Uruguay 1950)"),
    ("FWC-11", "Team Photo (West Germany 1954)"),
    ("FWC-12", "Team Photo (Brazil 1962)"),
    ("FWC-13", "Team Photo (West Germany 1974)"),
    ("FWC-14", "Team Photo (Argentina 1986)"),
    ("FWC-15", "Team Photo (Brazil 1994)"),
    ("FWC-16", "Team Photo (Brazil 2002)"),
    ("FWC-17", "Team Photo (Italy 2006)"),
    ("FWC-18", "Team Photo (Germany 2014)"),
    ("FWC-19", "Team Photo (Argentina 2022)"),
]


# ─────────────────────────────────────────────────────────────────────────────
# Construcción del catálogo
# ─────────────────────────────────────────────────────────────────────────────

def slug_id(prefix: str, suffix: str) -> str:
    """ID estable: stk_arg_10, stk_fwc_1, stk_cc_lat_5, stk_extra_messi_gold."""
    s = suffix.lower().replace(" ", "_").replace("-", "_").replace(".", "")
    return f"{prefix}_{s}"


def parse_player_line(line: str) -> dict | None:
    """Parsea una línea tipo 'ARG-10. Rodrigo De Paul' → dict."""
    m = re.match(r"^([A-Z]{3})-(\d+)\.\s*(.+)$", line.strip())
    if not m:
        return None
    team_code, num, name = m.group(1), int(m.group(2)), m.group(3).strip()
    return {"team_code": team_code, "number": num, "name": name}


def build_catalog() -> dict:
    stickers: list[dict] = []
    position = 0

    # ── 1. Panini Logo (00) ─────────────────────────────────────────────────
    position += 1
    stickers.append({
        "id": "stk_panini_00",
        "code": "00",
        "album_position": position,
        "label": "Panini Logo",
        "type": "panini_logo",
        "team_id": None,
        "position_in_team": None,
        "is_foil": True,
        "parallel_set": None,
        "parallel_variant": None,
    })

    # ── 2. Intro FWC-1 a FWC-8 ─────────────────────────────────────────────
    intro = [
        ("FWC-1", "Emblema Oficial 1/2", "official_emblem"),
        ("FWC-2", "Emblema Oficial 2/2", "official_emblem"),
        ("FWC-3", "Mascotas Oficiales",  "mascot"),
        ("FWC-4", "Slogan Oficial",      "slogan"),
        ("FWC-5", "Pelota Oficial",      "official_ball"),
        ("FWC-6", "Canadá (Anfitrión)",  "host_country"),
        ("FWC-7", "México (Anfitrión)",  "host_country"),
        ("FWC-8", "USA (Anfitrión)",     "host_country"),
    ]
    for code, label, stype in intro:
        position += 1
        stickers.append({
            "id": slug_id("stk", code),
            "code": code,
            "album_position": position,
            "label": label,
            "type": stype,
            "team_id": None,
            "position_in_team": None,
            "is_foil": True,
            "parallel_set": None,
            "parallel_variant": None,
        })

    # ── 3. Stickers por equipo (48 × 20 = 960) ──────────────────────────────
    # Cargar jugadores parseados
    players_by_team: dict[str, dict[int, str]] = {}
    for raw_line in PLAYERS_RAW.strip().split("\n"):
        if not raw_line.strip():
            continue
        parsed = parse_player_line(raw_line)
        if parsed:
            players_by_team.setdefault(parsed["team_code"], {})[parsed["number"]] = parsed["name"]

    for team in TEAMS:
        code = team["code"]
        team_id = f"team_{code.lower()}"
        for pos_in_team in range(1, 21):
            position += 1
            sticker_code = f"{code}-{pos_in_team}"
            sticker_id = slug_id("stk", sticker_code)

            if pos_in_team == 1:
                label = f"Escudo {team['name_es']}"
                stype = "team_emblem"
                is_foil = True
            elif pos_in_team == 13:
                label = f"Foto Grupal {team['name_es']}"
                stype = "team_photo"
                is_foil = False
            else:
                label = players_by_team.get(code, {}).get(pos_in_team, f"Jugador {pos_in_team}")
                stype = "player"
                is_foil = False

            stickers.append({
                "id": sticker_id,
                "code": sticker_code,
                "album_position": position,
                "label": label,
                "type": stype,
                "team_id": team_id,
                "position_in_team": pos_in_team,
                "is_foil": is_foil,
                "parallel_set": None,
                "parallel_variant": None,
            })

    # ── 4. Historia del Mundial (FWC-9 a FWC-19) ───────────────────────────
    for code, label in FWC_HISTORY:
        position += 1
        stickers.append({
            "id": slug_id("stk", code),
            "code": code,
            "album_position": position,
            "label": label,
            "type": "legend",
            "team_id": None,
            "position_in_team": None,
            "is_foil": False,
            "parallel_set": None,
            "parallel_variant": None,
        })

    main_album_count = position
    print(f"→ Stickers del álbum principal: {main_album_count}")

    # ── 5. Extra Stickers (20 × 4 = 80, FUERA del álbum) ────────────────────
    extra_stickers = []
    variants = [("regular", "Purple"), ("bronze", "Bronze"), ("silver", "Silver"), ("gold", "Gold")]
    for idx, (player, team_code) in enumerate(EXTRA_STICKER_PLAYERS, start=1):
        parallel_set = f"MP-{idx:02d}"  # MP = Mystery Player
        for variant_key, variant_label in variants:
            extra_stickers.append({
                "id": slug_id("stk_extra", f"{idx}_{variant_key}"),
                "code": f"{parallel_set}-{variant_key.upper()}",
                "album_position": None,  # fuera del álbum
                "label": f"{player} ({variant_label})",
                "type": "mystery_player",
                "team_id": f"team_{team_code.lower()}",
                "position_in_team": None,
                "is_foil": variant_key in ("silver", "gold"),
                "parallel_set": parallel_set,
                "parallel_variant": variant_key,
            })

    # ── 6. Coca-Cola Latinoamérica (parte del álbum, página dedicada) ──────
    cocacola_stickers = []
    for code, player, team_code in COCA_COLA_LATAM:
        cocacola_stickers.append({
            "id": slug_id("stk_cc_lat", code.lower()),
            "code": f"CC-LAT-{code[2:]}",  # CC-LAT-1, CC-LAT-2, etc.
            "album_position": None,  # página especial, sin posición numérica fija
            "label": f"{player} (Coca-Cola LATAM)",
            "type": "coca_cola_special",
            "team_id": f"team_{team_code.lower()}",
            "position_in_team": None,
            "is_foil": False,
            "parallel_set": "coca_cola_latam",
            "parallel_variant": None,
        })

    all_stickers = stickers + extra_stickers + cocacola_stickers

    # ── 7. Equipos con IDs ─────────────────────────────────────────────────
    teams_out = [
        {
            "id": f"team_{t['code'].lower()}",
            "code": t["code"],
            "name_en": t["name_en"],
            "name_es": t["name_es"],
            "confederation": t["confederation"],
            "is_host": t.get("is_host", False),
        }
        for t in TEAMS
    ]

    return {
        "version": "0.1",
        "source": "cartophilic-info-exch.blogspot.com (community checklist)",
        "source_url": "https://cartophilic-info-exch.blogspot.com/2026/03/panini-fifa-world-cup-2026-mexusacan-09_030880692.html",
        "license_note": "Datos fácticos (códigos, nombres, posiciones). No incluye imágenes oficiales de Panini.",
        "counts": {
            "teams": len(teams_out),
            "album_stickers": main_album_count,
            "extra_stickers": len(extra_stickers),
            "coca_cola_latam": len(cocacola_stickers),
            "total": len(all_stickers),
        },
        "teams": teams_out,
        "stickers": all_stickers,
    }


if __name__ == "__main__":
    catalog = build_catalog()

    output = Path("/mnt/user-data/outputs/catalog.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✓ Catálogo generado en {output}")
    print(f"\nResumen:")
    for k, v in catalog["counts"].items():
        print(f"  {k}: {v}")

    # Sanity checks
    main_album = [s for s in catalog["stickers"] if s["album_position"] is not None]
    assert len(main_album) == 980, f"Álbum principal: esperaba 980, hay {len(main_album)}"

    # Verificar que no haya posiciones duplicadas
    positions = [s["album_position"] for s in main_album]
    assert len(positions) == len(set(positions)), "Hay posiciones duplicadas"
    assert min(positions) == 1 and max(positions) == 980, "Rango de posiciones inválido"

    # Verificar que cada equipo tenga 20 stickers
    from collections import Counter
    team_counts = Counter(s["team_id"] for s in catalog["stickers"]
                          if s["album_position"] is not None and s["team_id"])
    for team_id, count in team_counts.items():
        assert count == 20, f"{team_id} tiene {count} stickers, esperaba 20"

    print(f"\n✓ Sanity checks pasados:")
    print(f"  - 980 stickers en el álbum principal")
    print(f"  - posiciones únicas 1..980")
    print(f"  - 48 equipos × 20 stickers cada uno")
    print(f"  - {len(catalog['stickers'])} stickers totales (incluyendo extras + Coca-Cola)")
