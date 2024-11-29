from django.utils.translation import gettext_lazy as _

# RATING_CHOICES = (
#     (1, "★☆☆☆☆"),
#     (2, "★★☆☆☆"),
#     (3, "★★★☆☆"),
#     (4, "★★★★☆"),
# (5, "★★★★★"),
# )

# ☆☆☆☆☆☆☆ **

# * for ManageAppSettings //

APP_TYPES = (
    (0, _("Select Your Bussiness")),
    (1, _("Single Clinic App.")),
    (2, _("Multi Clinic App.")),
    (3, _("Maintenance App.")),
)


SESSION_STATUS = (
    (0, "--- Session Status ---"),
    (1, "مفتوح"),
    (2, "معلق"),
    (3, "مغلق"),
)
# * for unites of measure

UNITS = (
    ("main", _("الوحدة الاساسية")),
    ("sell", _("وحدة البيع")),
    ("purchase", _("وحدة الشراء")),
    ("main_sell", _("وحدة بيع اساسيه")),
    ("main_purchase", _("وحدة شراء اساسيه")),
    ("default", _("افتراضى")),
)


HOUR = "hour"
DAY = "day"
WEEK = "week"
MONTH = "month"
YEAR = "year"

TIMES = (
    (HOUR, _("ساعة")),
    (DAY, _("يوم")),
    (WEEK, _("اسبوع")),
    (MONTH, _("شهر")),
    (YEAR, _("سنة")),
)

CASH = "نقدى"
DUE = "اجل"

DUE_CASH = "دفعات نقدية"
CASH_MONEY = "كاش"
CHEQUE = "شيك"
TRANSFERE = "تحويل"

VISA = "فيزا"
WALLET = "محفظة"
NEW_WALLET = "  محفظةجديدة"
SAFE = "خزينة"
BANK_ACCOUNT = "حساب بنكى"
STORES = "مخازن"


PAYMENT_METHODS = (
    (0, "--- Payment Methods ---"),
    (1, CASH),
    (2, DUE),
    # (3, VISA),
    # (4, CHEQUE),
    # (5, TRANSFERE),
)

TREASURY_TYPES = (
    (0, "--- Treasury Types ---"),
    (1, SAFE),
    (2, VISA),
    (3, WALLET),
    (4, BANK_ACCOUNT),
)


CASH_PAYMENT_METHODS = (
    (0, "--- Cash Payment Methods ---"),
    (1, SAFE),
    (2, VISA),
    (3, WALLET),
    (4, NEW_WALLET),
)

TYPES = (
    (0, "--- Choose Type ---"),
    (1, SAFE),
    (2, VISA),
    (3, WALLET),
    (4, NEW_WALLET),
    (5, BANK_ACCOUNT),
    (6, STORES),
)

DUE_PAYMENT_METHODS = (
    (1, DUE_CASH),
    (2, CHEQUE),
    (3, TRANSFERE),  # need an account_no
)

OWNER = "owner"
CLIENT = "client"
ADMIN = "admin"
VENDOR = "vendor"
# EDITOR = 'editor'
MANAGER = "manager"
EMPLOYEE = "employee"
REPRESENTATIVE = "rep"
DRIVER = "driver"
GUEST = "guest"

USER_TYPES = (
    (OWNER, "Owner"),
    (MANAGER, "Manager"),
    (ADMIN, "Admin"),
    (EMPLOYEE, "Employee"),
    (VENDOR, "Vendor"),
    (CLIENT, "Client"),
    (REPRESENTATIVE, "Representative"),
    (DRIVER, "Driver"),
    (GUEST, "Guest"),
)

# * In Carts app SellService model
CLIENT_ROLE = (
    (0, "--Select Account Type--"),
    (1, "Client"),
    (2, "Employee"),
    (3, "Vendor"),
)

TRANSACTION_TYPE = (
    (0, "--Select Transaction Type--"),
    (1, _("Debit")),
    (2, _("Credit")),
    (3, _("Debit & Credit")),
)
# EMP_ROLE =(
#     (0, "--Select Employee Role --"),
#     (1, "Supervisor"),
#     (2, "Manager"),
#     (3, "Employee"),
# )

SERVCIE_BILL_TYPE = (
    (0, "--Select Bill Type--"),
    (1, "Services"),
    (2, "Items"),
    (3, "Services & Items"),
)


# * for gender
MALE = "m"
FEMALE = "f"

GENDER = (
    (MALE, _("Male")),
    (FEMALE, _("Female")),
)

MARITAL_STATUS = (
    (0, "--Select Marital Status--"),
    (1, "Single"),
    (2, "Married"),
    (3, "Divorced"),
    (4, "Widowed"),
)

MILITARY_STATUS = (
    (0, "--Select Military Status--"),
    (1, "Exemption"),
    (2, "Postponed"),
    (3, "Temporary Exemption"),
)

RELIGION = (
    (0, "--Select Religion--"),
    (1, "Muslim"),
    (2, "Christian"),
)

# * for Discount
DISCOUNT_CHOICES = (
    (0, "Disc / Off"),
    (1, "%"),
    (2, "$"),
)

# * for Tax
TAX_CHOICES = (
    (0, "Tax/Off"),
    (1, "%"),
    (2, "$"),
)


# * for Bill
BILL_LINKED = (
    (0, "Bill Off"),
    (1, "Bill On"),
    # (2, 'Off'),
)

BILL_TYPES = (
    (0, "Select Bill Type"),
    (1, "Sales Bill"),
    (2, "Return Sales Bill"),
    (3, "Purchases Bill"),
    (4, "Return Purchases Bill"),
)


# * for store responsibles
STORE_ROLES = (
    (0, "--Select Store Roles--"),
    (1, "Full Access"),
    (2, "Add and Update"),
    (3, "Add Only"),
)

SALES_OFFER = (
    (0, "--Select Sales Offer--"),
    (1, "Sales Offer 1"),
    (2, "Sales Offer 2"),
    (3, "Sales Offer 3"),
)

CLIENT_TYPE = (
    (0, "--Select Cliet Type--"),
    (1, "Cash"),
    (2, "On Line"),
    (3, "Due"),
    (4, "Payments"),
)

#####

EQUIPMENT_TYPE = (
    (0, "--- Equipment Type ---"),
    (1, "Equipment"),
    (2, "Vehicle"),
)

CURRENT_STATUS = (
    (0, "--- Status ---"),
    (1, "In Service"),
    (2, "Out Of Service"),
    (3, "Under Maintenance"),
    (4, "In Storage"),
    (5, "Reserved"),
    (6, "On Assignment"),
    (7, "Damaged"),
    (8, "Sold"),
)

VEHICLE_TYPES = (
    (0, "--- Select Vehicle Type ---"),
    (1, "Car"),
    (2, "Motorcycle"),
    (3, "Truck"),
    (4, "Bus"),
    (5, "Bicycle"),
    (6, "Scooter"),
    (7, "Van"),
    (8, "Tractor"),
    (9, "ATV"),
    (10, "RV"),
)

EGYPT_GOVERNORATES = (
    (0, "--- Select Governorates ---"),
    (1, "Alexandria"),
    (2, "Aswan"),
    (3, "Asyut"),
    (4, "Beheira"),
    (5, "Beni Suef"),
    (6, "Cairo"),
    (7, "Dakahlia"),
    (8, "Damietta"),
    (9, "Faiyum"),
    (10, "Gharbia"),
    (11, "Giza"),
    (12, "Ismailia"),
    (13, "Kafr El Sheikh"),
    (14, "Luxor"),
    (15, "Matruh"),
    (16, "Minya"),
    (17, "Monufia"),
    (18, "New Valley"),
    (19, "North Sinai"),
    (20, "Port Said"),
    (21, "Qalyubia"),
    (22, "Qena"),
    (23, "Red Sea"),
    (24, "Sharqia"),
    (25, "Sohag"),
    (26, "South Sinai"),
    (27, "Suez"),
)


####
CITY = (
    ("alexandria", "ALEXANDRIA"),
    ("aswan", "ASWAN"),
    ("asyut", "ASYUT"),
    ("beheira", "BEHEIRA"),
    ("benisuef", "BENI SUEF"),
    ("cairo", "CAIRO"),
    ("dakahlia", "DAKAHLIA"),
    ("demiatta", "DAMIETTA"),
    ("faiyum", "FAIYUM"),
    ("gharbia", "GHARBIA"),
    ("giza", "GIZA"),
    ("ismailia", "ISMAILIA"),
    ("kafr_el_sheikh", "KAFR EL SHEIKH"),
    ("luxor", "LUXOR"),
    ("matruh", "MATRUH"),
    ("minya", "MINYA"),
    ("monufia", "MONUFIA"),
    ("new_valley", "NEW VALLEY"),
    ("north_sinai", "NORTH SINAI"),
    ("port_said", "PORT SAID"),
    ("qalyubia", "QALYUBIA"),
    ("qena", "QENA"),
    ("red_sea", "RED SEA"),
    ("sharqia", "SHARQIA"),
    ("sohag", "SOHAG"),
    ("south_sinai", "SOUTH SINAI"),
    ("suez", "SUEZ"),
    ("halayb", "HALAYB"),
    ("shalateen", "SHALATEEN"),
)


# EGYPT = "EG"

COUNTRY = (
    # "AF":"Afghanistan",
    # "AX":"Aland Islands",
    # "AL":"Albania",
    ("DZ", "Algeria"),  # index=0
    # "AS":"American Samoa",
    # "AD":"Andorra",
    # "AO":"Angola",
    # "AI":"Anguilla",
    # "AQ":"Antarctica",
    # "AG":"Antigua and Barbuda",
    # "AR":"Argentina",
    # "AM":"Armenia",
    # "AW":"Aruba",
    ("AU", "Australia"),
    # "AT":"Austria",
    # "AZ":"Azerbaijan",
    # "BS":"Bahamas",
    ("BH", "Bahrain"),
    # "BD":"Bangladesh",
    # "BB":"Barbados",
    # "BY":"Belarus",
    ("BE", "Belgium"),
    # "BZ":"Belize",
    # "BJ":"Benin",
    # "BM":"Bermuda",
    # "BT":"Bhutan",
    # "BO":"Bolivia, Plurinational State of",
    # "BQ":"Bonaire, Sint Eustatius and Saba",
    # "BA":"Bosnia and Herzegovina",
    # "BW":"Botswana",
    # "BV":"Bouvet Island",
    ("BR", "Brazil"),
    # "IO":"British Indian Ocean Territory",
    # "BN":"Brunei Darussalam",
    # "BG":"Bulgaria",
    # "BF":"Burkina Faso",
    # "BI":"Burundi",
    # "KH":"Cambodia",
    # "CM":"Cameroon",
    ("CA", "Canada"),
    # "CV":"Cape Verde",
    # "KY":"Cayman Islands",
    # "CF":"Central African Republic",
    # "TD":"Chad",
    # "CL":"Chile",
    ("CN", "China"),
    # "CX":"Christmas Island",
    # "CC":"Cocos (Keeling) Islands",
    # "CO":"Colombia",
    # "KM":"Comoros",
    # "CG":"Congo",
    # "CD":"Congo, The Democratic Republic of the",
    # "CK":"Cook Islands",
    # "CR":"Costa Rica",
    # "CI":"Côte d'Ivoire",
    # "HR":"Croatia",
    # "CU":"Cuba",
    # "CW":"Curaçao",
    # "CY":"Cyprus",
    # "CZ":"Czech Republic",
    ("DK", "Denmark"),
    # "DJ":"Djibouti",
    # "DM":"Dominica",
    # "DO":"Dominican Republic",
    # "EC":"Ecuador",
    ("EG", "Egypt"),  # index=8
    # "SV":"El Salvador",
    # "GQ":"Equatorial Guinea",
    # "ER":"Eritrea",
    # "EE":"Estonia",
    # "ET":"Ethiopia",
    # "FK":"Falkland Islands (Malvinas)",
    # "FO":"Faroe Islands",
    # "FJ":"Fiji",
    ("FI", "Finland"),
    ("FR", "France"),
    # "GF":"French Guiana",
    # "PF":"French Polynesia",
    # "TF":"French Southern Territories",
    # "GA":"Gabon",
    # "GM":"Gambia",
    # "GE":"Georgia",
    ("DE", "Germany"),
    # "GH":"Ghana",
    # "GI":"Gibraltar",
    ("GR", "Greece"),
    # "GL":"Greenland",
    # "GD":"Grenada",
    # "GP":"Guadeloupe",
    # "GU":"Guam",
    # "GT":"Guatemala",
    # "GG":"Guernsey",
    # "GN":"Guinea",
    # "GW":"Guinea-Bissau",
    # "GY":"Guyana",
    # "HT":"Haiti",
    # "HM":"Heard Island and McDonald Islands",
    # "VA":"Holy See (Vatican City State)",
    # "HN":"Honduras",
    # "HK":"Hong Kong",
    # "HU":"Hungary",
    # "IS":"Iceland",
    ("IN", "India"),
    ("ID", "Indonesia"),
    # "IR":"Iran, Islamic Republic of",
    ("IQ", "Iraq"),
    # "IE":"Ireland",
    # "IM":"Isle of Man",
    # "IL":"Israel",
    ("IT", "Italy"),
    # "JM":"Jamaica",
    ("JP", "Japan"),
    # "JE":"Jersey",
    ("JO", "Jordan"),
    # "KZ":"Kazakhstan",
    # "KE":"Kenya",
    # "KI":"Kiribati",
    # "KP":"Korea, Democratic People's Republic of",
    # "KR":"Korea, Republic of",
    ("KW", "Kuwait"),
    # "KG":"Kyrgyzstan",
    # "LA":"Lao People's Democratic Republic",
    # "LV":"Latvia",
    ("LB", "Lebanon"),
    # "LS":"Lesotho",
    # "LR":"Liberia",
    ("LY", "Libya"),
    # "LI":"Liechtenstein",
    # "LT":"Lithuania",
    ("LU", "Luxembourg"),
    # "MO":"Macao",
    # "MK":"Macedonia, Republic of",
    # "MG":"Madagascar",
    # "MW":"Malawi",
    # "MY":"Malaysia",
    # "MV":"Maldives",
    # "ML":"Mali",
    # "MT":"Malta",
    # "MH":"Marshall Islands",
    # "MQ":"Martinique",
    # "MR":"Mauritania",
    # "MU":"Mauritius",
    # "YT":"Mayotte",
    # "MX":"Mexico",
    # "FM":"Micronesia, Federated States of",
    # "MD":"Moldova, Republic of",
    # "MC":"Monaco",
    # "MN":"Mongolia",
    # "ME":"Montenegro",
    # "MS":"Montserrat",
    ("MA", "Morocco"),
    # "MZ":"Mozambique",
    # "MM":"Myanmar",
    # "NA":"Namibia",
    # "NR":"Nauru",
    # "NP":"Nepal",
    ("NL", "Netherlands"),
    # "NC":"New Caledonia",
    # "NZ":"New Zealand",
    # "NI":"Nicaragua",
    # "NE":"Niger",
    # "NG":"Nigeria",
    # "NU":"Niue",
    # "NF":"Norfolk Island",
    # "MP":"Northern Mariana Islands",
    # "NO":"Norway",
    ("OM", "Oman"),
    ("PK", "Pakistan"),
    # "PW":"Palau",
    ("PS", "Palestinian Territory, Occupied"),
    # "PA":"Panama",
    # "PG":"Papua New Guinea",
    # "PY":"Paraguay",
    # "PE":"Peru",
    # "PH":"Philippines",
    # "PN":"Pitcairn",
    # "PL":"Poland",
    # "PT":"Portugal",
    # "PR":"Puerto Rico",
    ("QA", "Qatar"),
    # "RE":"Réunion",
    # "RO":"Romania",
    # "RU":"Russian Federation",
    # "RW":"Rwanda",
    # "BL":"Saint Barthélemy",
    # "SH":"Saint Helena, Ascension and Tristan da Cunha",
    # "KN":"Saint Kitts and Nevis",
    # "LC":"Saint Lucia",
    # "MF":"Saint Martin (French part)",
    # "PM":"Saint Pierre and Miquelon",
    # "VC":"Saint Vincent and the Grenadines",
    # "WS":"Samoa",
    # "SM":"San Marino",
    # "ST":"Sao Tome and Principe",
    ("SA", "Saudi Arabia"),
    # "SN":"Senegal",
    # "RS":"Serbia",
    # "SC":"Seychelles",
    # "SL":"Sierra Leone",
    # "SG":"Singapore",
    # "SX":"Sint Maarten (Dutch part)",
    # "SK":"Slovakia",
    # "SI":"Slovenia",
    # "SB":"Solomon Islands",
    # "SO":"Somalia",
    ("ZA", "South Africa"),
    # "GS":"South Georgia and the South Sandwich Islands",
    ("ES", "Spain"),
    # "LK":"Sri Lanka",
    ("SD", "Sudan"),
    # "SR":"Suriname",
    ("SS", "South Sudan"),
    # "SJ":"Svalbard and Jan Mayen",
    # "SZ":"Swaziland",
    # "SE":"Sweden",
    # "CH":"Switzerland",
    ("SY", "Syrian Arab Republic"),
    # "TW":"Taiwan, Province of China",
    # "TJ":"Tajikistan",
    # "TZ":"Tanzania, United Republic of",
    # "TH":"Thailand",
    # "TL":"Timor-Leste",
    # "TG":"Togo",
    # "TK":"Tokelau",
    # "TO":"Tonga",
    # "TT":"Trinidad and Tobago",
    ("TN", "Tunisia"),
    ("TR", "Turkey"),
    ("TM", "Turkmenistan"),
    # "TC":"Turks and Caicos Islands",
    # "TV":"Tuvalu",
    # "UG":"Uganda",
    # "UA":"Ukraine",
    ("AE", "United Arab Emirates"),
    ("GB", "United Kingdom"),
    ("US", "United States"),
    # "UM":"United States Minor Outlying Islands",
    # "UY":"Uruguay",
    ("UZ", "Uzbekistan"),
    # "VU":"Vanuatu",
    # "VE":"Venezuela, Bolivarian Republic of",
    # "VN":"Viet Nam",
    # "VG":"Virgin Islands, British",
    # "VI":"Virgin Islands, U.S.",
    # "WF":"Wallis and Futuna",
    ("YE", "Yemen"),
    ("ZM", "Zambia"),
    ("ZW", "Zimbabwe"),
)


NATIONALITIES = (
    ("AF", _("Afghan")),
    ("AL", _("Albanian")),
    ("DZ", _("Algerian")),
    ("AD", _("Andorran")),
    ("AO", _("Angolan")),
    ("AR", _("Argentinian")),
    ("AM", _("Armenian")),
    ("AU", _("Australian")),
    ("AT", _("Austrian")),
    ("AZ", _("Azerbaijani")),
    ("BS", _("Bahamian")),
    ("BH", _("Bahraini")),
    ("BD", _("Bangladeshi")),
    ("BB", _("Barbadian")),
    ("BY", _("Belorussian")),
    ("BE", _("Belgian")),
    ("BZ", _("Belizian")),
    ("BJ", _("Beninese")),
    ("BT", _("Bhutanese")),
    ("BO", _("Bolivian")),
    ("BA", _("Bosnian")),
    ("BW", _("Botswanan")),
    ("BR", _("Brazilian")),
    ("GB", _("British")),
    ("BN", _("Bruneian")),
    ("BG", _("Bulgarian")),
    ("BF", _("Burkinese")),
    ("MM", _("Burmese")),
    ("BF", _("Burundian")),
    ("BI", _("Cambodian")),
    ("CM", _("Cameroonian")),
    ("CA", _("Canadian")),
    ("CV", _("Cape Verdean")),
    ("TD", _("Chadian")),
    ("CL", _("Chilean")),
    ("CN", _("Chinese")),
    ("CO", _("Colombian")),
    ("CG", _("Congolese")),
    ("CR", _("Costa Rican")),
    ("HR", _("Croatian")),
    ("CU", _("Cuban")),
    ("CY", _("Cypriot")),
    ("CZ", _("Czech")),
    ("DK", _("Danish")),
    ("DJ", _("Djiboutian")),
    ("DM", _("Dominican")),
    ("DO", _("Dominican")),
    ("EC", _("Ecuadorean")),
    ("EG", _("Egyptian")),  # index=48
    ("SV", _("Salvadorean")),
    ("GB", _("English")),
    ("ER", _("Eritrean")),
    ("EE", _("Estonian")),
    ("ET", _("Ethiopian")),
    ("FJ", _("Fijian")),
    ("FI", _("Finnish")),
    ("FR", _("French")),
    ("GA", _("Gabonese")),
    ("GM", _("Gambian")),
    ("GE", _("Georgian")),
    ("DE", _("German")),
    ("GH", _("Ghanaian")),
    ("GR", _("Greek")),
    ("GD", _("Grenadian")),
    ("GT", _("Guatemalan")),
    ("GQ", _("Guinean")),
    ("GY", _("Guyanese")),
    ("HT", _("Haitian")),
    ("NL", _("Dutch")),
    ("HN", _("Honduran")),
    ("HU", _("Hungarian")),
    ("IS", _("Icelandic")),
    ("IO", _("Indian")),
    ("ID", _("Indonesian")),
    ("IR", _("Iranian")),
    ("IQ", _("Iraqi")),
    ("IE", _("Irish")),
    ("IL", _("Israeli")),
    ("IT", _("Italian")),
    ("JM", _("Jamaican")),
    ("JP", _("Japanese")),
    ("JO", _("Jordanian")),
    ("KZ", _("Kazakh")),
    ("KE", _("Kenyan")),
    ("KW", _("Kuwaiti")),
    ("LA", _("Laotian")),
    ("LV", _("Latvian")),
    ("LB", _("Lebanese")),
    ("LR", _("Liberian")),
    ("LY", _("Libyan")),
    ("LT", _("Lithuanian")),
    ("MK", _("Macedonian")),
    ("MG", _("Malagasay")),
    ("MW", _("Malawian")),
    ("MY", _("Malaysian")),
    ("MV", _("Maldivian")),
    ("ML", _("Malian")),
    ("MT", _("Maltese")),
    ("MR", _("Mauritanian")),
    ("MU", _("Mauritian")),
    ("MX", _("Mexican")),
    ("MD", _("Moldovan")),
    ("MC", _("Monacan")),
    ("MN", _("Mongolian")),
    ("ME", _("Montenegrin")),
    ("MA", _("Moroccan")),
    ("MZ", _("Mozambican")),
    ("NA", _("Namibian")),
    ("NP", _("Nepalese")),
    ("NI", _("Nicaraguan")),
    ("NE", _("Nigerien")),
    ("NG", _("Nigerian")),
    ("KP", _("North Korean")),
    ("NO", _("Norwegian")),
    ("OM", _("Omani")),
    ("PK", _("Pakistani")),
    ("PA", _("Panamanian")),
    ("PG", _("Guinean")),
    ("PY", _("Paraguayan")),
    ("PE", _("Peruvian")),
    ("PH", _("Philippine")),
    ("PL", _("Polish")),
    ("PT", _("Portuguese")),
    ("QA", _("Qatari")),
    ("RO", _("Romanian")),
    ("RU", _("Russian")),
    ("RW", _("Rwandan")),
    ("SA", _("Saudi")),
    ("AE", _("Scottish")),
    ("SN", _("Senegalese")),
    ("RS", _("Serbian")),
    ("SC", _("Seychellois")),
    ("SL", _("Sierra Leonian")),
    ("SG", _("Singaporean")),
    ("SK", _("Slovak")),
    ("SI", _("Slovenian")),
    ("SO", _("Somali")),
    ("ZA", _("South African")),
    ("KR", _("South Korean")),
    ("ES", _("Spanish")),
    ("LK", _("Sri Lankan")),
    ("SD", _("Sudanese")),
    ("SR", _("Surinamese")),
    ("SZ", _("Swazi")),
    ("SE", _("Swedish")),
    ("CH", _("Swiss")),
    ("SY", _("Syrian")),
    ("TW", _("Taiwanese")),
    ("TJ", _("Tadjik")),
    ("TZ", _("Tanzanian")),
    ("TH", _("Thai")),
    ("TG", _("Togolese")),
    ("TT", _("Trinidadian")),
    ("TN", _("Tunisian")),
    ("TR", _("Turkish")),
    ("TM", _("Turkmen")),
    ("TV", _("Tuvaluan")),
    ("UG", _("Ugandan")),
    ("UA", _("Ukrainian")),
    ("UY", _("Uruguayan")),
    ("UZ", _("Uzbek")),
    ("VU", _("Vanuatuan")),
    ("VE", _("Venezuelan")),
    ("VN", _("Vietnamese")),
    ("GB", _("Welsh")),
    ("YE", _("Yemeni")),
    ("ZM", _("Zambian")),
    ("ZW", _("Zimbabwean")),
)
