import json
import urllib.request
from bs4 import BeautifulSoup

def api():
    #https: // stackoverflow.com / questions / 44239822 / urllib - request - urlopenurl -with-authentication / 44239906
    #logged_user = request.user
    #role_class = UserProfile.objects.filter(user=logged_user)

    #if role_class.get().role == 'gestorsala':
        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        top_level_url = "https://ourfarms.herokuapp.com/apiRest/REF/?format=json"
        password_mgr.add_password(None, top_level_url, "GR2", "gr2134567890")

        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        # create "opener" (OpenerDirector instance)
        opener = urllib.request.build_opener(handler)

        # use the opener to fetch a URL
        products = opener.open("https://ourfarms.herokuapp.com/apiRest/REF/?format=json")

        soup = BeautifulSoup(products.read(), 'html.parser')
        data = json.loads(soup.decode("utf-8")) #items -> type list data is a list of the manifests


        num_manifest = 0

        for manifest in data: #manifest -> type dict
            print(" ")
            print("I'm manifest: ", num_manifest)
            #print("len: ", len(manifest.items()))
            for key, value in manifest.items():
                #print(key, value)
                if key == "Products":
                    print("I have ", len(value), "products")  # value is a list
                    for x in range(len(value)):
                        print("Product: ", x,"-->", value[x])
            num_manifest += 1


if __name__ == "__main__":
    api()
