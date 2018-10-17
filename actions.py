import calls, content, display


def set_auth():
    key = input("Please enter you API Key or hit enter to use a default key: ").strip(" ")

    if key == "":
        defaultKey = content.demoCreds
        auth_test = calls.get_carriers(defaultKey)

        return ("Using default key.", defaultKey, True, auth_test[1])
    else:
        auth_test = calls.get_carriers(key)

        if auth_test[0] == 200:
            return ("API credentials authorized.\nAssociating carrier accounts with this session.", key, True, auth_test[1])
        else:
            return ("Authorization failed, please check the key entered for errors.", "error", False, content.authFailure)


def query_carrier_list(sessionSeller):
    if sessionSeller.validKey == False:
        return "Please make sure you have valid keys before making this call."

    try:
        feed = calls.get_carriers(sessionSeller.apiKey)[1]
    except Exception:
        return "Call failed. Please make sure you have working connection to the internet."

    displayList = ""    

    for carrier in feed["carriers"]:
        displayList += "{} - Carrier ID: {} - Nickname: {} - Account: {} - Primary Account: {} - Multi-Package Support: {}\n".format(carrier["friendly_name"], carrier["carrier_id"], carrier["nickname"], carrier["account_number"], carrier["primary"], carrier["has_multi_package_supporting_services"])
    return displayList


def add_fedex(sessionSeller):
    if sessionSeller.validKey == False:
        return "Please make sure you have valid keys before making this call."

    print("In this example we will be adding a FedEx account that has parcelcast enabled. To add this account we will be providing the following details:")
    print(content.addCarrierCallDisplay + content.fedexDisplayJson)

    input("Press enter to continue.\n")

    addFedexParcelcast = calls.add_fedex_account(sessionSeller.apiKey, content.fedexPayload)

    if addFedexParcelcast[0] != 200:
        return "Looks like the attempt failed because of error: {}.\n".format(str(addFedexParcelcast))

    print("By listing carriers with another call we can check to see if it is on your account.")
    print(query_carrier_list(sessionSeller))
    print("There it is under Carrier ID {}! It's just that easy.".format(addFedexParcelcast[1]["carrier_id"]))

    input("Let's go ahead and remove the account by making a DELETE call. Hit enter to continue.\n")

    removeFedexparcelcast = calls.delete_fedex_account(sessionSeller.apiKey, addFedexParcelcast[1]["carrier_id"])

    if removeFedexparcelcast != 204:
        return "Looks like the attempt failed because of error: {}.\n".format(str(removeFedexparcelcast))

    input("Now let's see if the Parcelcast account is gone. Hit enter to continue.")

    print(query_carrier_list(sessionSeller))

    return "And there we go. Programmatically adding and removing carrier accounts is easy peasy!"


def create_shipment_data(shipment_data):
    data = {"shipment_id": shipment_data["shipments"][0]["shipment_id"], "create_date": shipment_data["shipments"][0]["created_at"], "ship_to": {"name": shipment_data["shipments"][0]["ship_to"]["name"], "city": shipment_data["shipments"][0]["ship_to"]["city_locality"], "state": shipment_data["shipments"][0]["ship_to"]["state_province"]}, "ship_from": {"name": shipment_data["shipments"][0]["ship_from"]["name"], "city": shipment_data["shipments"][0]["ship_from"]["city_locality"], "state": shipment_data["shipments"][0]["ship_from"]["state_province"]}, "number_of_packages": len(shipment_data["shipments"][0]["packages"])}

    return data


def create_shipment(sessionSeller):
    if sessionSeller.validKey == False:
        return "Please make sure you have valid keys before making this call."

    shipmentData = ""
    createShipmentCall = ""

    print("Now let's create shipment that we can use for rate shopping and label creation.\nTo save time we've gone ahead and created a couple of sample shipments.")

    while True:
        shipmentChoice = input("Enter (1) for a single package shipment, enter (2) for a multi-package shipment that requests address validation. ").strip()

        if shipmentChoice == "1":
            print("Single package shipment selected!")
            input("Hit enter to see the call we'll be making.")
            print(content.createShipmentCallDisplay + content.displayExampleShipment1)
            pause = input("Press enter to continue.\n")
            createShipmentCall = calls.create_shipment(sessionSeller.apiKey, content.exampleShipment1)
            break
        elif shipmentChoice == "2":
            print("Multi-Package shipment selected!")
            input("Hit enter to see the call we'll be making.")
            print(content.createShipmentCallDisplay + content.displayExampleShipment2)
            input("Press enter to continue.\n")
            createShipmentCall = calls.create_shipment(sessionSeller.apiKey, content.exampleShipment2)            
            break
        else:
            print("Sorry, I didn't quite get that.")

    while True:
        option = input("Would you like to see the raw JSON response [y\\n]: ").lower().strip(" ")

        if option == "y":
            print("Here's the response JSON of that call:\n")
            print(createShipmentCall[1])
            break
        elif option == "n":
            break
        else:
            print("Sorry, I didn't quite get that.")
    
    print("\nYour shipment now lives within the ShipEngine ecosystem can be applied within a whole bunch of functions just by using its new shipment ID of {}.".format(createShipmentCall[1]["shipments"][0]["shipment_id"]))
    
    shipmentData = create_shipment_data(createShipmentCall[1])

    print("\nNow that we have a shipment created we are ready to move on.")

    return shipmentData


def shop_for_rates(sessionSeller):
    if sessionSeller.validKey == False:
        return "Please make sure you have valid keys before making this call."

    print("\nWith ShipEngine you can get rates without having a shipment ready but in this example we'll use a shipment's ID and a carrier ID to get back a list of all applicable rates for that carrier.")

    while True:
        option = input("\nIf you don't have your shipment_id or carrier_id enter (l) for a list, otherwise hit enter to proceed: ").lower().strip(" ")

        if len(option) == 0:
            break
        elif option == "l":
            print("\n-Carriers Connected-")
            print(display.displayCarriers(sessionSeller))
            print("-Session Shipments-")
            print(display.displayShipments(sessionSeller))
            break
        else:
            pass

    while True:
        shipmentId = input("Please enter your selected shipment_id: ").lower().strip(" ")
        if shipmentId == "q":
            return "Okay, leaving the rates section."
        elif shipmentId == "l":
            print("\n-Carriers Connected-")
            print(display.displayCarriers(sessionSeller))
            print("-Session Shipments-")
            print(display.displayShipments(sessionSeller))
            shipmentId = input("Please enter your selected shipment_id: ").lower().strip(" ")
        carrierId = input("Please enter your selected carrier_id: ").lower().strip(" ")

        if carrierId == "q":
            return "Okay, leaving the rates section."
        elif carrierId == "l":
            print("\n-Carriers Connected-")
            print(display.displayCarriers(sessionSeller))
            print("-Session Shipments-")
            print(display.displayShipments(sessionSeller))
        elif len(shipmentId) == 0 or len(carrierId) == 0:
            print("It looks like nothing was entered for one of the IDs. Please try again or enter (q) to quit this section.")
        elif shipmentId[0:3] != "se-" or carrierId[0:3] != "se-":
            print("ShipEngine originated IDs will start with 'se-', try entering IDs with that prefix. Enter (l) if you need to see you session carrier and shipment lists again.")
        else:
            break

    print("Here's a look at the call we'll be making:")
    print(content.getRatesCallDisplay + content.displayExampleRatesJson.format("{", "}", shipmentId, carrierId))
    input("Press enter to continue.\n")

    try:
        feed = calls.get_rates_call(sessionSeller.apiKey, shipmentId, carrierId)
    except Exception:
        return "Call failed. Please make sure you have working connection to the internet."

    if feed[0] != 200:
        print("\nResponse code {} returned. Response message:\n{}\n".format(feed[0], feed[1]))
        return "Check your that your IDs are accurate and try again."
    elif len(feed[1]["rate_response"]["errors"]) > 0:
        print("It looks like there were some errors with the rates:\n")
        for each in feed[1]["rate_response"]["errors"]:
            print("• {}\n".format(each["message"]))
        return "Try again with another shipment or carrier."

    sessionSeller.addRates(feed[1])

    print("Here's a consolidated list of the rates that were returned.\n")

    print(display.displayRates(sessionSeller))

    while True:
        option = input("Would you like to see the raw JSON response [y\\n]: ").lower().strip(" ")

        if option == "y":
            print(feed[1])
            break
        elif option == "n":
            break
        else:
            print("Sorry, I didn't quite get that.")

    return "\nNow that you have a rate ID creating a label in ShipEngine will quick and easy."


def generate_label(sessionSeller):
    if sessionSeller.validKey == False:
        return "Please make sure you have valid keys before making this call."

    print("\nShipEngine allows for the generation of shipping labels without having a shipment or rates already present but for this example we are going to take one of your existing rate IDs and use it to create a label.")

    while True:
        option = input("\nIf you don't have your rate_id enter (l) for a list, otherwise hit enter to proceed: ").lower().strip(" ")

        if len(option) == 0:
            break
        elif option == "l":
            print("-Session Rates-")
            print(display.displayRates(sessionSeller))
            break
        else:
            pass

    while True:
        rateId = input("Please enter your selected rate_id: ").lower().strip(" ")

        if rateId == "q":
            return "Okay, leaving the label section."
        elif len(rateId) == 0:
            print("It looks like nothing was entered for the rate ID. Please try again or enter (q) to quit this section.")
        elif option == "l":
            print("-Session Rates-")
            print(display.displayRates(sessionSeller))
        elif rateId[0:3] != "se-":
            print("ShipEngine originated IDs will start with 'se-', try entering IDs with that prefix. Enter (l) if you need to see you session list again.")
        else:
            break

    isTest = False

    if rateId not in sessionSeller.testLabelChecker:
        print("\nRate ID not found in current session, check ID or proceed with caution: USPS-based labels will be charged upon creation unless test_label specified.\n")

        while True:
            restart = input("Would you like to quit and restart this section? [y\\n]: ").lower().strip(" ")
            if restart == "y":
                return "Returning to menu."
            elif restart == "n":
                break
            else:
                pass
    elif sessionSeller.testLabelChecker[rateId] == "stamps_com" or sessionSeller.testLabelChecker[rateId] == "endicia":
            isTest = True

    print("\nHere's a look at the call we'll be making:")
    print(content.createLabelCallDisplay.format(rateId) + content.displayExampleLabelJson.format("{", "}", str(isTest).lower()))

    input("Press enter to continue.\n")

    print("Making request. . .\n")
    
    try:
        feed = calls.create_label_from_rate(sessionSeller.apiKey, rateId, isTest)
    except Exception:
        return "Call failed. Please make sure you have working connection to the internet."

    if feed[0] != 200:
        print("Response code {} returned.".format(feed[0]))
        if feed[1]["errors"][0]["message"]:
            print("Response message: {}".format(feed[1]["errors"][0]["message"]))
        return "Check your that your rate ID is accurate and try again."

    sessionSeller.addLabel(feed[1])

    while True:
        option = input("Would you like to see the raw JSON response [y\\n]: ").lower().strip(" ")

        if option == "y":
            print(feed[1])
            break
        elif option == "n":
            break
        else:
            print("Sorry, I didn't quite get that.")
    
    return "\nYour label has been generated and is ready for retrieval! Copy and paste the URL below into a web browser to begin the download:\n\n{}\n".format(sessionSeller.labelList[feed[1]["label_id"]]["label_url"])

def void_label(sessionSeller):
    if sessionSeller.validKey == False:
        return "Please make sure you have valid keys before making this call."

    print("Feel free to void a label created during this session or any other ShipEngine originated label.")

    while True:
        choice = input("Would you like a list of the labels created in this session? [y\\n]: ")

        if choice == "y":
            print("\n{}".format(display.displayLabels(sessionSeller)))
            break
        elif choice == "n":
            break
        elif choice == "q":
            return "Exiting label voiding section.\n"
        else:
            print("Sorry, I didn't quite get that. If you'd like to quit this section enter (q).")

    labelToVoid = input("Enter the label ID to be voided: ").lower().strip(" ")

    try:
        intoTheVoid = calls.void_label_call(sessionSeller.apiKey, labelToVoid)
    except Exception:
        return "Call failed. Please make sure you have working connection to the internet."

    if intoTheVoid[0] == 200 and intoTheVoid[1]["approved"] == True:
        if labelToVoid in sessionSeller.labelList:
            sessionSeller.labelList[labelToVoid]["label_voided"] = True
        return "Label {} voided.".format(labelToVoid)
    elif intoTheVoid[0] == 200 and intoTheVoid[1]["approved"] == False:
        return "Label void request not approved. {}".format(intoTheVoid[1]["message"])
    else:
        response = "Call unsuccessful. Response status code {}.".format(intoTheVoid[0])

        try:
            response += " Response message:\n{}\n".format(intoTheVoid[1])
        except IndexError:
            pass

        return response


def testo(key, labelToVoid):
    intoTheVoid = calls.void_label_call(key, labelToVoid)

    response = "Call unsuccessful. Response status code {}.".format(intoTheVoid[0])

    try:
        response += " Response message:\n{}\n".format(intoTheVoid[1])
    except IndexError:
        pass

    return response
    