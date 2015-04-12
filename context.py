#!/usr/bin/python

from tablet import Line
from sys import stdout

class Context:

    # List of common professions in the Ur III corpus.

    professions = [
                "aga'us[soldier]",
                "arad[slave]",
                "aszgab[leatherworker]",
                "azlag[fuller]",
                "bahar[potter]",
                "bisajdubak[archivist]",
                "damgar[merchant]",
                "dikud[judge]",
                "dubsar[scribe]",
                "en[priest]",
                "ereszdijir[priestess]",
                "ensik[ruler]",
                "engar[farmer]",
                "enkud[tax-collector]",
                "gaba'asz[courier]",
                "galamah[singer]",
                "gala[singer]",
                "geme[worker]",
                "gudug[priest]",
                "guzala[official]",
                "idu[doorkeeper]",
                "iszib[priest]",
                "kaguruk[supervisor]",
                "kasz[runner]",
                "kijgia[messenger]",
                "kinkin[miller]",
                "kuruszda[fattener]",        # (of animals)
                "kusz[official]",
                "lu2-mar-sa-me[unknown]",
                "lugal[king]",
                "lukur[priestess]",
                "lungak[brewer]",
                "malah[sailor]",
                "maszkim[administrator]",
                "muhaldim[cook]",
                "muszendu[bird-catcher]",
                "nagada[herdsman]",
                "nagar[carpenter]",
                "nar[musician]",
                "nin[lady]",
                "nubanda[overseer]",
                "nukirik[horticulturalist]",
                "sajDUN[recorder]",
                "sajja[official]",
                "simug[smith]",
                "sipad[shepherd]",
                "sukkal[secretary]",
                "szabra[administrator]",
                "szagia[cup-bearer]",
                "szakkanak[general]",
                "szej[cook]",
                "szesz[brother]",
                "szidim[builder]",
                "szu'i[barber]",
                "szukud[fisherman]",
                "tibira[sculptor]",
                "ugula[overseer]",
                "unud[cowherd]",
                "urin[guard]",
                "ujjaja[porter]",
                "uszbar[weaver]",
                "zabardab[official]",
                "zadim[stone-cutter]"
              ]


    @staticmethod
    def get_left_context(line, index, word, args, offset = 1):

        (leftword, leftlem) = (None, None)
        if (index - offset) >= 0:
            (leftword, leftlem) = line.words[index - offset]

        if args.nogloss:
            leftlem = Context.remove_gloss(leftlem)

        return (leftword, leftlem)


    @staticmethod
    def get_right_context(line, index, word, args, offset = 1):

        (rightword, rightlem) = (None, None)
        if (len(line.words) - 1) >= (index + offset):
            (rightword, rightlem) = line.words[index + offset]

        if args.nogloss:
            rightlem = Context.remove_gloss(rightlem)

        return (rightword, rightlem)


    @staticmethod
    def remove_gloss(lem):
        if lem:
            lem = list( set( [ l if not '[' in l
                               else 'W' 
                               for l in lem ] ))
        return lem


    @staticmethod
    def format_context(lem):
        if not lem:
            return None
        else:
            return ','.join(lem)


    @staticmethod
    def get_liang_induced_context_rules():
        return [ ]


    @staticmethod
    def get_liang_induced_spelling_rules():
        return [ ('ir', 46386),
                 ('lu2', 41752),
                 ('a-a', 39855),
                 ('a-hu', 22940),
                 ('a-ta', 16151),
                 ('a-na', 14518),
                 ('al-la', 14441),
                 ('ub-sar', 13065),
                 ('dub-sar', 13062),
                 ('a-ba', 12624),
                 ('ba-a', 12427),
                 ('a-ti', 11618),
                 ('a-sza', 11529),
                 ('us2-sa', 11305),
                 ('a-sza3', 10887),
                 ('i-ga', 10566),
                 ('a-ga', 9429),
                 ('i3-da', 8835),
                 ('ab-ba', 8628),
                 ('a-ka', 8526),
                 ('a-ni', 8236),
                 ('szu-{d}suen', 7592),
                 ('ub-ba', 7541),
                 ('i-a', 7492),
                 ('szul-gi', 7391),
                 ('ba-ba6', 7389),
                 ('a-da', 7310),
                 ('ARAD2', 7001),
                 ('a-e', 6999),
                 ('a-ra', 6973),
                 ('al-e', 6903),
                 ('a-du', 6851),
                 ('gal-e', 6836),
                 ('u-um', 6822),
                 ('en-lil2', 6780),
                 ('{d}en-lil', 6757),
                 ('sa6-ga', 6618),
                 ('i-da', 6509),
                 ('i-ma', 6490),
                 ('u-DU', 6377),
                 ('mu-DU', 6362),
                 ('lugal-e', 6361),
                 ('zi-ga', 6270),
                 ('u-ba', 6091),
                 ('a2-bi', 6019),
                 ('a-zi', 5903),
                 ('1(disz)-sze', 5682),
                 ('1(disz)-sze3', 5676),
                 ('a-sa6', 5633),
                 ('gub-ba', 5590),
                 ('a-e3', 5400),
                 ('a-mu', 5361),
                 ('i-ta', 5136),
                 ('la2-ia3', 5057),
                 ('an-na', 4962),
                 ('a-bi', 4926),
                 ('il2-la', 4782),
                 ('a-sze', 4676),
                 ('zi-da', 4672),
                 ('e-bi', 4629),
                 ('ba-sa', 4607),
                 ('engar', 4602),
                 ('sze-bi', 4572),
                 ('e2-a', 4531),
                 ('a-sze3', 4525),
                 ('1(disz)-kam', 4437),
                 ('uri5{ki}-ma', 4388),
                 ('i3-li', 4158),
                 ('3(disz)-kam', 4156),
                 ('ru-um', 4125),
                 ('i3-li2', 4101),
                 ('a-lu', 4022),
                 ('ki-ma', 3983),
                 ('nu-ba', 3967),
                 ('u-ta', 3962),
                 ('ur-ni', 3959),
                 ('ki-masz', 3910),
                 ('nu-banda3', 3887),
                 ('mar-{d}suen', 3874),
                 ('a-nu', 3834),
                 ('i-na', 3792),
                 ('sze-KIN', 3781),
                 ('KIN-ku5', 3766),
                 ('ur-e', 3620),
                 ('a-za', 3609),
                 ('za3-ga', 3567),
                 ('un-ga', 3566),
                 ('2(disz)-kam', 3560),
                 ('ur-{d}ba', 3559),
                 ('u-a', 3545),
                 ('ur-sa', 3521),
                 ('i-la', 3513),
                 ('a-gu', 3513),
                 ('in-a', 3506),
                 ('pa-e3', 3497),
                 ('mu-zi', 3441),
                 ('dumu-zi', 3435),
                 ('a-la', 3403),
                 ('e2-ga', 3403),
                 ('u2-a', 3370),
                 ('ur-nigar', 3334),
                 ('e2-gal', 3291),
                 ('ur-{d}ni', 3286),
                 ('a-ru', 3246),
                 ('u-ga', 3205),
                 ('in-gi', 3197),
                 ('u-la', 3189),
                 ('u-nu', 3186),
                 ('nin-a', 3162),
                 ('a-ke4', 3152),
                 ('4(disz)-kam', 3148),
                 ('u-hu', 3125),
                 ('ur-{d}nin', 3102),
                 ('u2-ba', 3097),
                 ('u3-ba', 3071),
                 ('a-zu', 3029),
                 ('mar-tu', 3022),
                 ('al-a', 3021),
                 ('a2-du', 3018),
                 ('ku3-ba', 3009),
                 ('sa2-du11', 2983),
                 ('i-bi', 2957),
                 ('hi-a', 2956),
                 ('ur-me', 2899),
                 ('a-ma', 2882),
                 ('nu-u', 2873),
                 ('a-usz2', 2871),
                 ('ba-usz2', 2862),
                 ('gal-a', 2853),
                 ('hu-u', 2828),
                 ('ur-{d}szu', 2813),
                 ('a-tu', 2763),
                 ('gu-la', 2735),
                 ('mu-ni', 2735),
                 ('n-ta', 2728),
                 ('szesz-ka', 2719),
                 ('szesz-kal', 2716),
                 ('e-ba', 2713),
                 ('u2-ka', 2667),
                 ('e2-ma', 2666),
                 ('du10-ga', 2635),
                 ('i3-gesz', 2632),
                 ('ab-du', 2626),
                 ('en-ki', 2602),
                 ('ezem-{d}szu', 2578),
                 ('gu-za', 2576),
                 ('u2-e', 2575),
                 ('ul-pa', 2569),
                 ('{d}en-ki', 2556),
                 ('szul-pa', 2546),
                 ('{d}szul-pa', 2536),
                 ('li9-si4', 2526),
                 ('{d}li9-si', 2524),
                 ('a2-gu', 2508),
                 ('ur-bi', 2502),
                 ('a2-a', 2500),
                 ('en-na', 2496),
                 ('zu-e', 2479),
                 ('dumu-ni', 2433),
                 ('masz-da', 2429),
                 ('e-e', 2412),
                 ('a-li', 2407),
                 ('szu-gi', 2402),
                 ('{d}nin-gi', 2374),
                 ('nin-szu', 2368),
                 ('si-mu', 2354),
                 ('a-ri', 2351),
                 ('hun-ga2', 2350),
                 ('e3-a', 2342),
                 ('ezem-{d}szul', 2339),
                 ('in-szub', 2331),
                 ('{d}nin-szu', 2326),
                 ('{d}nin-szubur', 2323),
                 ('du11-ga', 2322),
                 ('ur-bi2', 2307),
                 ('sar-ta', 2284),
                 ('mu-ru', 2282),
                 ('a-gi', 2262),
                 ('za3-bi', 2259),
                 ('sza3-bi', 2248),
                 ('bi2-lu', 2244),
                 ('a-di', 2209),
                 ('nin-lil2', 2200),
                 ('e2-mah', 2154),
                 ('mu-hul', 2153),
                 ('nig2-la', 2153),
                 ('su-ga', 2150),
                 ('usz-bar', 2142),
                 ('nu-ri', 2123),
                 ('a2-ga', 2094),
                 ('ur-sag', 2092),
                 ('lugal-i', 2089),
                 ('i3-du', 2078),
                 ('zu-nu', 2071),
                 ('szu-nu', 2059),
                 ('kal-ga', 2039),
                 ('u2-lum', 2032),
                 ('zu2-lum', 2020),
                 ('szu-numun', 1989),
                 ('e-ta', 1988),
                 ('ma-ke', 1974),
                 ('al-ku', 1965),
                 ('ma-ke4', 1959),
                 ('id-gur2', 1948),
                 ('ur-{d}lamma', 1940),
                 ('u-da', 1940),
                 ('lugal-ku', 1931),
                 ('u3-bi', 1906),
                 ('i-ti', 1896),
                 ('sila3-ta', 1891),
                 ('nu-ur', 1890),
                 ('szu-esz', 1873),
                 ('i-me', 1856),
                 ('ub-da', 1852),
                 ('u2-du', 1836),
                 ('i-bi2', 1833),
                 ('limmu2-ba', 1830),
                 ('u3-ga', 1823),
                 ('mu-du', 1813),
                 ('si-ma', 1791),
                 ('ku3-ga', 1784),
                 ('lugal-a', 1780),
                 ('ur-{d}sza', 1767),
                 ('i3-pa', 1763),
                 ('ar-a', 1752),
                 ('in-u', 1742),
                 ('am-ma', 1736),
                 ('a-me', 1723),
                 ('a-dim2', 1665),
                 ('ba-di', 1661),
                 ('un-na', 1656),
                 ('ki-ga', 1654),
                 ('ur-{d}szar', 1651),
                 ('bi2-{d}suen', 1640),
                 ('5(disz)-kam', 1638),
                 ('i-su', 1638),
                 ('asz-ru', 1623),
                 ('e-ki', 1616),
                 ('ezem-ma', 1611),
                 ('ur-{d}suen', 1609),
                 ('aga3-us2', 1608),
                 ('u2-sa', 1605),
                 ('a2-ki', 1600),
                 ('ki-a', 1598),
                 ('nig2-ka', 1579),
                 ('e-ne', 1571),
                 ('a-si', 1566),
                 ('a2-ka', 1554),
                 ('ur-{d}na', 1553),
                 ('du-ni', 1539),
                 ('a-bu', 1538),
                 ('e2-ki', 1532),
                 ('ur-ra', 1530),
                 ('ah-e', 1524),
                 ('a2-n', 1514),
                 ('um-ma', 1512),
                 ('mah-e', 1512),
                 ('ur-a', 1502),
                 ('id2-da', 1485),
                 ('nig2-ka9', 1484),
                 ('lugal-u', 1480),
                 ('i-du', 1479),
                 ('gid2-da', 1476),
                 ('in-ta', 1455),
                 ('{d}ig-alim', 1453),
                 ('{munus}asz2-gar3', 1453),
                 ('er3-ra', 1433),
                 ('du-du', 1429),
                 ('ad-da', 1416),
                 ('ensi2-ka', 1414),
                 ('u3-zu', 1414),
                 ('ur-sa6', 1407),
                 ('u-mu', 1407),
                 ('6(disz)-kam', 1406),
                 ('guz-za', 1405),
                 ('al-ta', 1385),
                 ('gal2-la', 1378),
                 ('in-na', 1375),
                 ('su-su', 1374),
                 ('ur-{d}isz', 1359),
                 ('gal-an', 1354),
                 ('e11-e', 1353),
                 ('si-ga', 1350),
                 ('a2-da', 1348),
                 ('ug3-IL2', 1337),
                 ('ur-i', 1333),
                 ('ur-{d}nu', 1319),
                 ('7(disz)-kam', 1316),
                 ('al-ni', 1315),
                 ('8(disz)-kam', 1314),
                 ('an-ti', 1313),
                 ('im-ma', 1298),
                 ('ur-{d}ig', 1296),
                 ('ab-sza', 1293),
                 ('gal-ni', 1288),
                 ('lugal-ni', 1280),
                 ('i-sze3', 1278),
                 ('lu-lu', 1276),
                 ('esz18-dar', 1273),
                 ('i-ri', 1258),
                 ('bu-u', 1247),
                 ('in-ma', 1238),
                 ('nin-ma', 1229),
                 ('sza3-gu', 1225),
                 ('ki-si', 1222),
                 ('mu-ta', 1221),
                 ('hu-uh', 1220),
                 ('al-sze3', 1220),
                 ('ezem-a', 1219),
                 ('ur-{d}en', 1219),
                 ('u5-bi', 1218),
                 ('an-sza', 1207),
                 ('ezem-an', 1202),
                 ('ezem-{d}nin', 1185),
                 ('ar3-ra', 1177),
                 ('hu-uh2', 1163),
                 ('i-sza', 1150),
                 ('gi4-a', 1149),
                 ('a2-zi', 1148),
                 ('e-sze3', 1136),
                 ('u3-a', 1128),
                 ('uh2-nu', 1126),
                 ('ar-zi', 1116),
                 ('i-ba', 1114),
                 ('ar-szi', 1110),
                 ('i-e', 1105),
                 ('gur8-re', 1104),
                 ('ur-ku', 1101),
                 ('ki-su7', 1096),
                 ('bi2-gu7', 1091),
                 ('ur5-ra', 1088),
                 ('lu-bu', 1088),
                 ('ur-gu', 1082),
                 ('u5-bi2', 1082),
                 ('SIG7-a', 1081),
                 ('bar-ra', 1076),
                 ('me-e', 1074),
                 ('e-la', 1073),
                 ('i-ra', 1062),
                 ('gesz-zi', 1057),
                 ('ur3-ra', 1056),
                 ('kur-illat', 1055),
                 ('ku3-sig17', 1054),
                 ('{d}iszkur-illat', 1053),
                 ('a2-ta', 1052),
                 ('a2-la', 1045),
                 ('kar-zi', 1044),
                 ('{d}nin-gesz', 1042),
                 ('a-ku', 1041),
                 ('e2-ba', 1039),
                 ('ezem-me', 1038),
                 ('asz2-e', 1038),
                 ('i3-nu', 1030),
                 ('u3-nu', 1027),
                 ('ses-da', 1027),
                 ('masz2-e', 1027),
                 ('e-li', 1021),
                 ('lugal-ma', 1020),
                 ('ag-ga', 1015),
                 ('nig2-a', 1015),
                 ('sa6-sa6', 1009),
                 ('en-mah', 1006),
                 ('dam-ga', 998),
                 ('mu-ne', 997),
                 ('esz-a', 995),
                 ('i3-sa', 994),
                 ('nig2-gu', 987),
                 ('u4-e', 986),
                 ('da3-gu7', 985),
                 ('iti-6(disz)', 980),
                 ('ur-{d}li', 974),
                 ('ur4-ra', 973),
                 ('ah-gal', 970),
                 ('u2-ru', 970),
                 ('e-ka', 969),
                 ('ni-i', 969),
                 ('i-in', 958),
                 ('i-zi', 958),
                 ('inim-{d}szara2', 958),
                 ('u-ka', 951),
                 ('u-ku', 950),
                 ('hu-nu', 933),
                 ('gar-ra', 929),
                 ('gu-ni', 928),
                 ('ri-mu', 927),
                 ('2(disz)-sze3', 925),
                 ('sze-i', 924),
                 ('siki-{d}nin', 923),
                 ('i3-ka', 922),
                 ('gar-e', 917),
                 ('dam-gar3', 911),
                 ('in-esz', 909),
                 ('i3-ga', 909),
                 ('gu-nigin', 903),
                 ('gu3-de2', 898),
                 ('ur-tur', 897),
                 ('szu-du', 892),
                 ('hu-wa', 888),
                 ('ur2-ra', 888),
                 ('u4-gu', 879),
                 ('e-si', 878),
                 ('u2-gu', 877),
                 ('sze-il', 876),
                 ('sa6-ta', 872),
                 ('lugal-ma2', 861),
                 ('kam-asz', 858),
                 ('in-ga', 855),
                 ('kar-ra', 855),
                 ('ur-du', 854),
                 ('kiszib3-ba', 853),
                 ('min-esz3', 846),
                 ('lu5-ta', 845),
                 ('e-a', 839),
                 ('ur-szu', 838),
                 ('ur-ba', 829),
                 ('du8-a', 826),
                 ('nam-ha', 823),
                 ('i-ku', 821),
                 ('gi-ra', 817),
                 ('e2-i', 810),
                 ('lil2-ra', 809),
                 ('u-na', 807),
                 ('tu-ra', 807),
                 ('hu-ur', 801),
                 ('lagar-e', 798),
                 ('en-nu', 789),
                 ('ur-{d}isztaran', 788),
                 ('e-esz', 787),
                 ('ke4-ne', 786),
                 ('a-sag', 780),
                 ('an-ne', 774),
                 ('ar-da', 772),
                 ('in-da', 769),
                 ('ga6-ga2', 764),
                 ('sza3-ta', 759),
                 ('am-ta', 756),
                 ('ku4-ra', 755),
                 ('i-im', 754),
                 ('im-gi', 751),
                 ('hu-ur5', 751),
                 ('i-tu', 748),
                 ('sza13-dub', 746),
                 ('ur5-ti', 745),
                 ('szu-i', 740),
                 ('i3-zu', 736),
                 ('si-i', 730),
                 ('mu-szu', 724),
                 ('e3-ta', 721),
                 ('u-sze3', 719),
                 ('ri-i', 718),
                 ('dab5-ba', 717),
                 ('i-ni', 712),
                 ('masz-e', 712),
                 ('in-ka', 712),
                 ('ur-ta', 707),
                 ('nin-e', 706),
                 ('in-su', 695),
                 ('munu4-gu7', 693),
                 ('in-tu', 691),
                 ('esz5-sza', 685),
                 ('lu5-lu5', 681),
                 ('lugal-usz', 681),
                 ('bar-da', 677),
                 ('e-lu', 676),
                 ('szu-du7', 671),
                 ('al-bi', 669),
                 ('a-mi', 663),
                 ('gu-du', 661),
                 ('al-ba', 656),
                 ('ur-{d}dumu', 656),
                 ('ka5-a', 655),
                 ('gal-ka', 655),
                 ('im-sze3', 653),
                 ('a-ki', 652),
                 ('al-me', 651),
                 ('hi-li', 650),
                 ('lugal-ne', 643),
                 ('sa10-a', 641),
                 ('a{ki}-sze3', 636),
                 ('se3-ga', 635),
                 ('esz-sza', 633),
                 ('i-gu', 633),
                 ('an-du', 632),
                 ('at-ta', 630),
                 ('a-pi', 630),
                 ('ezem-{d}ba', 629),
                 ('ku-ra', 628),
                 ('illat-ta', 628),
                 ('ezem-{d}dumu', 627),
                 ('IR', 626),
                 ('1(disz)-a', 623),
                 ('gi-sa', 620),
                 ('1(u)-kam', 617),
                 ('im-e', 616),
                 ('zu-ga', 615),
                 ('a-ha', 613),
                 ('dim-sze3', 611),
                 ('zu-ma', 609),
                 ('al-in', 605),
                 ('hu-ni', 603),
                 ('ur-{d}utu', 599),
                 ('zu-ni', 598),
                 ('u5-a', 597),
                 ('wa-qar', 594),
                 ('usz-mu', 593),
                 ('ar-ga', 588),
                 ('a-hi', 586),
                 ('ia3-a', 581),
                 ('ur-{d}da', 579),
                 ('ar-sza', 568),
                 ('dara3-ab', 567),
                 ('a-szu', 546),
                 ('ah-ta', 540),
                 ('an-ku', 538),
                 ('mah-ta', 528),
                 ('ur-{d}a', 521),
                 ('ku5-ra', 508),
                 ('kiszib3-bi', 508),
                 ('uz-ga', 507),
                 ('de6-a', 506),
                 ('szar-ru', 505),
                 ('du8-du', 503),
                 ('asz-ta', 499),
                 ('za3-ge', 499),
                 ('bar-ta', 497),
                 ('zu-ku', 496),
                 ('nu-tuku', 492),
                 ('nam-e', 489),
                 ('ub-du', 470),
                 ('ri-iq', 462),
                 ('an-ka', 459),
                 ('a-ne', 453),
                 ('zi-ge', 447),
                 ('ba6-ta', 442),
                 ('ti-id', 442),
                 ('ur-su', 440),
                 ('nam-sza', 410),
                 ('iq-ti', 405),
                 ('um-mu', 395),
                 ('e-da', 394),
                 ('ge6-par4', 390),
                 ('ab-ta', 388),
                 ('gu-gu', 386),
                 ('ku-u', 375),
                 ('tak4-a', 371),
                 ('6(disz)-sze3', 363),
                 ('hu-we', 359),
                 ('ur-ge6', 358),
                 ('ar-ba', 356),
                 ('bar-e', 355),
                 ('pa3-da', 353),
                 ('gi4-gi4', 353),
                 ('a-wa', 348),
                 ('al-kal', 340),
                 ('e-na', 340),
                 ('ti-e', 337),
                 ('ah-sze3', 333),
                 ('szeg9-bar', 332),
                 ('esz3-e', 330),
                 ('e-gi', 329),
                 ('u-me', 328),
                 ('an-e', 326),
                 ('e-me', 319),
                 ('a-re', 304),
                 ('ezem-{d}me', 294),
                 ('gi-si', 289),
                 ('dalla', 287),
                 ('i-gi', 287),
                 ('szar-ra', 285),
                 ('ar3-ta', 283),
                 ('an-e3', 282),
                 ('ge6-ba', 279),
                 ('al-pa', 277),
                 ('tum3-du10', 277),
                 ('i-ib', 274),
                 ('uz-tur', 270),
                 ('bi-e', 264),
                 ('NE-NE', 261),
                 ('ar-za', 257),
                 ('esz-sze3', 254),
                 ('ur-sze', 251),
                 ('i-isz', 248),
                 ('szu-u', 247),
                 ('hu-bu', 239),
                 ('lu-usz', 231),
                 ('um-sze', 230),
                 ('e-ge', 229),
                 ('i-ki', 227),
                 ('usz-e', 221),
                 ('{d}isz-bi', 218),
                 ('ur5-sze3', 217),
                 ('e3-e', 215),
                 ('du-sze', 211),
                 ('szesz-szesz', 208),
                 ('bi-sze', 207),
                 ('gu-ul', 205),
                 ('1(u)-sze', 203),
                 ('gi-e', 202),
                 ('1(u)-sze3', 202),
                 ('lu5-ge', 202),
                 ('ku5-sze3', 195),
                 ('zu-gu', 193),
                 ('ur-zu', 193),
                 ('ub-tuku', 192),
                 ('gibil4-le', 188),
                 ('zu-zu', 186),
                 ('KI-AN{ki}', 185),
                 ('ur3-re', 185),
                 ('e-de3', 184),
                 ('mu-zu', 184),
                 ('tuh-hu', 183),
                 ('szer7-ru', 183),
                 ('zu-tum', 174),
                 ('mu-ur', 173),
                 ('szu-tu', 170),
                 ('ur-re', 169),
                 ('ur-ru', 160),
                 ('SI-A', 157),
                 ('ku-bu', 154),
                 ('u4-de3', 152),
                 ('i-re', 150),
                 ('bu-du', 150),
                 ('u4-sze3', 148),
                 ('szu-{d}utu', 146),
                 ('ri-sze', 140),
                 ('ur-{d}ur3', 138),
                 ('ku-ru', 133),
                 ('e-te', 132),
                 ('szu-lu', 132),
                 ('se-ge', 130),
                 ('sze-sze', 130),
                 ('zu-ur', 130),
                 ('NE-e', 128),
                 ('du11-ge', 127),
                 ('si-NE', 126),
                 ('di-de3', 124),
                 ('er3-re', 123),
                 ('si-e', 121),
                 ('hu-du', 121),
                 ('er-gu', 116),
                 ('ul-e', 116),
                 ('ke4-de3', 109),
                 ('ur-{d}gu', 102),
                 ('usz-lu', 101),
                 ('ur4-ru', 101),
                 ('ki-sze', 100) ]


    @staticmethod
    def write_header():
        stdout.write( '\tWord/Lemma (Do not use!)'
                      '\tWord Index'
                      '\tLeft Context Word'
                      # '\tLeft Context Lemma'
                      '\tRight Context Word'
                      # '\tRight Context Lemma'
                      '\tLine Context'
                      '\tIs Word Alone On Line'
                      '\tLeft context is dumu'
                      '\tRight context is dumu'
                      '\tNone ki (word) None'
                      '\tNone igi (word) None'
                      '\tNone igi (word)-sze3 None'
                      '\tPersonnenkeil'
                      '\tNone kiszib3 (word)'
                      '\tNone giri3 (word)'
                      '\tFirst syllable repeated'
                      '\tLast syllable repeated'
                      '\tAny syllable repeated'
                      '\tIs profession'
                      '\tContains profession'
                      '\tLeft Context is profession'
                      '\tLeft Context contains profession'
                      '\tRight Context is profession'
                      '\tRight Context contains profession'
                      '\tStarts with ur-'
                      '\tStarts with lu2-'
                      '\tEnds with -mu'
                      '\tContains {d}'
                      '\tContains {ki}'
                      '\tContains any determinative'
                      '\tContains q sound'
                      '\tContains lugal'
                      '\tContains number'
                      '\tFollowed by sag'
                      '\tFollowed by zarin'
                      '\tPreceded by numeric classifier'
                      '\titi at head of sentence'
                      '\tmu at head of sentence' )

        for (token, frequency) in Context.get_liang_induced_context_rules():
            stdout.write( '\tContext {} ({})'.format(token, frequency) )

        for (token, frequency) in Context.get_liang_induced_spelling_rules():
            stdout.write( '\tContains {} ({})'.format(token, frequency) )

        stdout.write('\n')
                      

    @staticmethod
    def test_all(tests):
        for t in tests:
            if not t:
                Context.test_fail()
                return
        Context.test_pass()


    @staticmethod
    def test_any(tests):
        for t in tests:
            if t:
                Context.test_pass()
                return
        Context.test_fail()

    
    @staticmethod
    def test_pass():
        stdout.write( '\t{}'.format(1) )


    @staticmethod
    def test_fail():
        stdout.write( '\t{}'.format(0) )
        

    @staticmethod
    def write(line, index, word, args):

        # Variables that we may use as part of other features.

        lemmata = line.get_lemmata(word)
        signs = word.split('-')

        (leftcx, leftlem) = \
            Context.get_left_context(line, index, word, args)

        (leftcx2, leftlem2) = \
            Context.get_left_context(line, index, word, args, offset = 2)

        (rightcx, rightlem) = \
            Context.get_right_context(line, index, word, args)

        # Print raw lemma tag.  May include gloss, even when
        # --nogloss switch is provided.  This is for the benefit
        # of human readers with some familiarity with Sumerian.
 
        stdout.write( '\t"{}/{}"'.format( word,
                                          Context.format_context(lemmata) ))

        # Index of word in line.  0-based.

        stdout.write( '\t{}'.format(index) )

        # Left context.

        stdout.write( '\t{}'.format(leftcx) )

        # Right context.

        stdout.write( '\t{}'.format(rightcx) )

        # Print line context.

        stdout.write( '\t"{}"'.format(line.line) )

        # Is word alone on line ?

        Context.test_all([ (leftcx, rightcx) == (None, None) ])
        
        # Left context is dumu.

        Context.test_all([ (leftcx == 'dumu') ])

        # Right context is dumu.

        Context.test_all([ (rightcx == 'dumu') ])

        # ^ ki <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == \
                           (None, 'ki', None) ])
            
        # ^ igi <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == \
                           (None, 'igi', None) ])

        # ^ igi <word>-sze $

        Context.test_all([ (leftcx2, leftcx, rightcx) == (None, 'igi', None),
                           word.endswith('-sze3') ])

        # Personnenkeil: ^ 1(disz) <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == \
                           (None, '1(disz)', None) ])

        # ^ kiszib3 <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == \
                           (None, 'kiszib3', None) ])

        # ^ giri3 <word> $

        Context.test_all([ (leftcx2, leftcx, rightcx) == \
                           (None, 'giri3', None) ])

        # First syllable repeated

        if len(signs) > 1:
            Context.test_all([ signs[0] == signs[1] ])
        else:
            Context.test_fail()

        # Last syllable repeated

        signs = word.split('-')
        if len(signs) > 1:
            Context.test_all([ signs[-2] == signs[-1] ])
        else:
            Context.test_fail()

        # Any syllable repeated

        if len(signs) > 1:
            Context.test_any([ a == b for (a, b)
                               in zip(signs, signs[1:]) ])
        else:
            Context.test_fail()

        # Is profession

        Context.test_any([ pf == lem
                           for pf in Context.professions
                           for lem in lemmata ])

        # Contains profession

        Context.test_any([ pf in lem 
                           for pf in Context.professions
                           for lem in lemmata ])

        # Left context is profession

        if leftlem:
            Context.test_any([ pf == lem
                               for pf in Context.professions
                               for lem in line.get_lemmata(leftcx) ])
        else:
            Context.test_fail()

        # Left context contains profession

        if leftlem:
            Context.test_any([ pf in lem
                               for pf in Context.professions
                               for lem in line.get_lemmata(leftcx) ])
        else:
            Context.test_fail()

        # Right context is profession

        if rightlem:
            Context.test_any([ pf == lem
                               for pf in Context.professions
                               for lem in line.get_lemmata(rightcx) ])
        else:
            Context.test_fail()

        # Right context contains profession

        if rightlem:
            Context.test_any([ pf in lem
                               for pf in Context.professions
                               for lem in line.get_lemmata(rightcx) ])
        else:
            Context.test_fail()

        # Starts with ur-

        Context.test_all([ word.startswith('ur-') ])
        
        # Starts with lu2-

        Context.test_all([ word.startswith('lu2-') ])
        
        # Ends with -mu

        Context.test_all([ word.endswith('-mu') ])
        
        # Contains {d}

        Context.test_all([ '{d}' in word ])

        # Contains {ki}

        Context.test_all([ '{ki}' in word ])

        # Contains any determinative

        Context.test_all([ '{' in word ])

        # Contains q sound

        Context.test_all([ 'q' in word ])

        # Contains lugal

        Context.test_all([ 'lugal' in word ])

        # Contains numeric elements

        Context.test_any([ '(asz)' in word,
                           '(disz)' in word,
                           '(u)' in word ])

        # Followed by sag

        Context.test_all([ rightcx == 'sag' ])

        # Followed by zarin

        Context.test_all([ rightcx == 'zarin' ])

        # Preceded by numeric classifier

        Context.test_all([ leftcx in ( 'ba-an', 'ba-ri2-ga', 'bur3', 'da-na',
                                       'gin2-tur', 'gin2', 'gur-lugal', 
                                       'gur-sag-gal2', 'gur', 'iku', 'GAN2',
                                       'ku-li-mu', 'ku-li-kam', 'kusz3',
                                       'sar', 'sila3' ) ])

        # iti at head of sentence

        Context.test_all([ 'iti' == line.words[0][0] ])

        # mu at head of sentence

        Context.test_all([ 'mu' == line.words[0][0] ])

        # Liang Luo's induced spelling rules

        for (token, frequency) in Context.get_liang_induced_spelling_rules():
            Context.test_all([ token in word ])

        """
        # Print boolean feature, 1 if word is PN, 0 if not.

        if 'PN' in lemmata:
            Context.test_pass()
        else:
            Context.test_fail()

        # Print most common tag for this word.

        # Actually, don't print the most common tag for this word.
        # This is not a good feature for CRF (or any feature-based
        # NLP algorithm) since it's # not immediately calculable
        # from context as a feature should be, but rather requires
        # reference to the index of the entire corpus.

        if word in INDEX:
        (bestlem, _) = INDEX[word].most_common(1)[0]
        else:
        bestlem = 'X'

        stdout.write('\t{}'.format( formatLems([ bestlem ], args) ))
        """
