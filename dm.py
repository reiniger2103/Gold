# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby
# granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOFTWARE.

# Usage: python3 dmfilmchecker.py <mode> <timeinterval>
#
# Available modes: 1. g200 - Checks only for Kodak Gold 200 3 Pack 36exp
#                  2. cp200 - Checks only for Kodak ColorPlus 200 24exp
#                  3. um400 - Checks only for Ultramax 400 24exp
#                  4. all - All of above
#                  5. If empty, same function as all.
#
# Time interval in seconds, default is 600 (10 min)
# example: python3 dmfilmchecker.py um400 360

# !IMPORTANT!: Make sure to change the store list before running the script!
# Step 1: go to https://www.dm.de/store.
# Step2: Enter location or ZIP code
# Step 3:  Find your local store and click more details.
# Step 4: Store ID should be in link.
# Example: #https://www.dm.de/store/de-2861/braunschweig/platz-am-ritterbrunnen-1 -> store number is 2861.

import requests
import sys
import time



# storeCounter, set through appropriate method
storeCount: int
# dictionary which contains the store numbers. Syntax: ['123', '1245', '1242'], set it manually
stores = {'storeNumbers': ['1628', '2077']}


def setStoreCount():
    global storeCount
    for key, value in stores.items():
        storeCount = len([item for item in value if item])


def checkKodakGold200():
    r = requests.get(
        'https://products.dm.de/store-availability/DE/availability?dans=405075', params=stores).json()
    print("\n\nChecking Kodak Gold 200 3 Pack availability")
    for i in range(0, storeCount):
        if r['storeAvailabilities']['405075'][i]['inStock']:
            street, city = getStoreDetails(int(r['storeAvailabilities']['405075'][i]['store']['storeNumber']))
            units = int(r['storeAvailabilities']['405075'][i]['stockLevel'])
            str1 = 'Available at ' + street + ' in ' + city + ' with ' + str(units) + 'units available'
            print(str1)
        else:
            street, city = getStoreDetails(int(r['storeAvailabilities']['405075'][i]['store']['storeNumber']))
            str2 = 'Unavailable at ' + street + ' in ' + city
            print(str2)
    print("Finished checking")


def checkOnlineKodakGold200():
    r = requests.get(
        'https://products.dm.de/product/de/search?productQuery=%3Arelevance%3Adan%3A405075&purchasableOnly=false'
        '&hideFacets=false&hideSorts=false&pageSize=5').json()
    print("Checking online availability")
    if r['products'][0]['purchasable']:
        str3 = 'Kodak Gold 200 available online!'
        print(str3)
    else:
        print("Kodak Gold 200 unavailable online!")



def getStoreDetails(storeid):
    r = requests.get('https://store-data-service.services.dmtech.com/stores/item/de/%2d' % storeid).json()
    street = r['address']['street']
    city = r['address']['city']
    return street, city


if __name__ == '__main__':
    counter = 1
    setStoreCount()
    TIME = 600
    if len(sys.argv) == 3:
        TIME = int(sys.argv[2])

    if sys.argv[1] == 'cp200':
        while True:
            checkKodakCP200()
            print("")
            checkOnlineKodakCP200()
            print("")
            print("Finished round %4d" % counter)
            counter = counter + 1
            time.sleep(TIME)

    elif sys.argv[1] == 'g200':
        while True:
            checkKodakGold200()
            print("")
            checkOnlineKodakGold200()
            print("")
            print("Finished round %4d" % counter)
            counter = counter + 1
            time.sleep(TIME)

    elif sys.argv[1] == 'um400':
        while True:
            checkKodakUltraMax400()
            print("")
            checkOnlineKodakUM400()
            print("")
            print("Finished round %4d" % counter)
            counter = counter + 1
            time.sleep(TIME)

    elif sys.argv[1] == 'all' or len(sys.argv) == 1:
        while True:
            checkKodakCP200()
            print("")
            checkKodakGold200()
            print("")
            checkOnlineKodakGold200()
            print("")
            checkKodakUltraMax400()
            print("")
            checkOnlineKodakCP200()
            print("")
            checkOnlineKodakUM400()
            print("")
            print("Finished round %4d" % counter)
            counter = counter + 1
            time.sleep(TIME)
