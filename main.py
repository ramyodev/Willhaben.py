import requests
from bs4 import BeautifulSoup
from timeit import timeit


base_url = "https://www.willhaben.at/iad/kaufen-und-verkaufen/marktplatz"
possible_url_inputs = {'marketplace_category': {'antiquitäten / kunst': '/antiquitaeten-kunst-6941',
                                                'baby / kind': '/baby-kind-3928',
                                                'beauty / gesundheit / wellness': '/beauty-gesundheit-wellness-3076',
                                                'boote / yachten / jetskis': '/boote-yachten-jetskis-5007823',
                                                'bücher / filme / musik': '/buecher-filme-musik-387',
                                                'computer / software': '/computer-software-5824',
                                                'dienstleistungen': '/dienstleistungen-537',
                                                'freizeit / instrumente / kulinarik': '/freizeit-instrumente-kulinarik-6462',
                                                'games / konsolen': '/games-konsolen-2785',
                                                'haus / garten / werkstatt': '/haus-garten-werkstatt-3541',
                                                'kameras / tv / multimedia': '/kameras-tv-multimedia-6808',
                                                'kfz-zubehör / motorradteile': '/kfz-zubehoer-motorradteile-6142',
                                                'mode / accessoires': '/mode-accessoires-3275',
                                                'smartphones / telefonie': '/smartphones-telefonie-2691',
                                                'spielen / spielzeug': '/spielen-spielzeug-5136',
                                                'sport / sportgeräte': '/sport-sportgeraete-4390',
                                                'tiere / tierbedarf': '/tiere-tierbedarf-4915',
                                                'uhren / schmuck': '/uhren-schmuck-2409',
                                                'wohnen / haushalt / gastronomie': '/wohnen-haushalt-gastronomie-5387',
                                                'zu verschenken': '/zu-verschenken'},
                       'sort_by': {'aktualität': 'sort=1', "preis aufsteigend": 'sort=3',
                                   'preis absteigend': 'sort=4'},
                       'federal_state': {'burgenland': 'areaId=1',
                                         'kärnten': 'areaId=2',
                                         'niederösterreich': 'areaId=3',
                                         'oberösterreich': 'areaId=4',
                                         'salzburg': 'areaId=5',
                                         'steiermark': 'areaId=6',
                                         'tirol': 'areaId=7',
                                         'vorarlberg': 'areaId=8',
                                         'wien': 'areaId=900',
                                         'andere Länder': 'areaId=22000'},
                       'vendor_type': {"privat": "ISPRIVATE=1", "händler": "ISPRIVATE=0"}
                       }


class ArgumentError(Exception):
    """Exception raised for errors in the input Category.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, arg):
        self.message = f"\nInvalid value for {arg}. Avalible Options:\n" + '\n'.join(possible_url_inputs[arg])
        super().__init__(self.message)


def search_products(title: str = '', PRICE_FROM: str = '', PRICE_TO: str = '', count: str = '',
                    marketplace_category: str = '', sort_by: str = '', federal_state: str = '',
                    vendor_type: str = ''):
    # Verify User Arguments
    args = locals()
    for argument in args:
        if args[argument] and argument in possible_url_inputs and args[argument] not in possible_url_inputs[argument]:
            raise ArgumentError(argument)

    url = build_url(title, PRICE_FROM, PRICE_TO, marketplace_category, sort_by, federal_state, vendor_type)
    response = requests.get(url)
print(2)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(3)
    must_in = "/iad/kaufen-und-verkaufen/d/"
    must_not_in = "counterId="

    print("soup")
    print(len(soup.find_all('article', attrs={'itemtype': 'http://schema.org/Product'})))


def build_url(keyword: str = "", PRICE_FROM: str = "", PRICE_TO: str = "", marketplace_category: str = "",
              sort_by: str = "", federal_state: str = "", vendor_type: str = ""):
    """
    Returns a Willhaben.at url created based on the parameters.
    Please make sure to specify exact parameters, for example marketplace_category= "books / movies / music".
    You can look up all the necessary parameters on Willhaben.at

            Parameters:
                    keyword (str): Terms that specify your search
                    PRICE_FROM (str): A minimum price for the products sought
                    PRICE_TO (str): A maximum price for the products sought
                    marketplace_category (str): The category from which products are searched
                    sort_by (str): Order in which the products should be listed
                    federal_state (str): Federal state from which the seller should come
                    vendor_type (str): Type of Vendor
            Returns:
                    url (str): Url created based on the parameters
    """

    # Verify User Arguments
    args = locals()
    for argument in args:
        if args[argument] and argument in possible_url_inputs and args[argument] not in possible_url_inputs[argument]:
            raise ArgumentError(argument)

    # Build URL String
    if marketplace_category:
        url = base_url + possible_url_inputs["marketplace_category"][marketplace_category] + '?' + '&'.join(
            [possible_url_inputs[x][args[x]] if x in possible_url_inputs else x + '=' + args[x] for x in args if
             args[x]]) + "&rows=100"
    else:
        url = base_url + '?' + '&'.join(
            [possible_url_inputs[x][args[x]] if x in possible_url_inputs else x + '=' + args[x] for x in args if
             args[x]]) + "&rows=100"

    return url


print(search_products())
