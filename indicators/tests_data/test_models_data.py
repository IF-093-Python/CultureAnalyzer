from indicators.models import CountryIndicator

__all__ = ['INDICATORS_DATA']

INDICATORS_DATA = (
    (
        CountryIndicator(iso_code='UKR',
                         name='Ukraine',
                         pdi=10,
                         idv=2,
                         mas=30,
                         uai=4,
                         lto=50,
                         ivr=6),
        [10, 2, 30, 4, 50, 6],
        "Ukraine - UKR",
    ),
    (
        CountryIndicator(iso_code='GER',
                         name='Germany',
                         pdi=98,
                         idv=12,
                         mas=76,
                         uai=0,
                         lto=50,
                         ivr=6),
        [98, 12, 76, 0, 50, 6],
        'Germany - GER',
    ),
    (
        CountryIndicator(iso_code='LON',
                         name='It is a very long name, very long name,',
                         pdi=0,
                         idv=0,
                         mas=32,
                         uai=0,
                         lto=89,
                         ivr=43),
        [0, 0, 32, 0, 89, 43],
        "It is a very long na - LON",
    ),
)
