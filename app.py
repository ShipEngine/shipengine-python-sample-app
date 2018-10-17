import calls, classy, actions, content, display


print(content.introMessage)

setKey = content.demoCreds

sessionSeller = classy.Seller(setKey, True)


while True:
    choice = input("\nEnter command number or (m) for menu: ").lower().strip(" ")

    if choice == "q":
        break
    elif choice == "m":
        print(content.menu)
    elif choice == "s":
        print(display.diplaySessionStatus(sessionSeller))
    elif choice == "1":
        resetKey = actions.set_auth()
        sessionSeller.apiKey, sessionSeller.validKey = resetKey[1], resetKey[2]
        sessionSeller.setSellerCarriers(resetKey[3])
        print(resetKey[0])
    elif choice == "2":
        print(actions.add_fedex(sessionSeller))
    elif choice == "3":
        newShipment = actions.create_shipment(sessionSeller)
        sessionSeller.addShipment(newShipment)
    elif choice == "4":
        print(actions.shop_for_rates(sessionSeller))
    elif choice == "5":
        print(actions.generate_label(sessionSeller))
    elif choice == "v":
        print(actions.void_label(sessionSeller))
    elif choice == "t":
        # menu option to test methods/functions
        print(actions.testo("Rc62TSSygDf3bTARBLeRunyVM3yeTA60WcEMkdnCWCg", "se-15269871"))


print("\nThanks for take this time to check out a small portion of ShipEngine's API capabilities. Head over to https://docs.shipengine.com/docs for a more detailed look at our API library.\n\nShipEngine: You Can Call on Us.")
