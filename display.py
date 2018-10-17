
def diplaySessionStatus(sessionSeller):
    return "\n\n-==Session Status==-\n\n--API Credentials--\n{}\n\n--Carrier Accounts Connected--\n{}\n--Session Shipments--\n{}\n--Session Rates--\n{}\n--Session Labels--\n{}".format(displayApiKeyStatus(sessionSeller), displayCarriers(sessionSeller), displayShipments(sessionSeller), displayRates(sessionSeller), displayLabels(sessionSeller))


def displayApiKeyStatus(sessionSeller):
    if sessionSeller.apiKey[0:6] == "R1Kfbr":
        return "Current Key: Demo API key in use."
    return "Current Key: API key starting with {}\nValid Key: {}".format(sessionSeller.apiKey[0:6], str(sessionSeller.validKey))


def displayCarriers(sessionSeller):
    if not sessionSeller.carrierAccounts:
        return "Carriers want to be associated to your account, follow step one to connect an account.\n"

    displayList = ""

    for carrier in sessionSeller.carrierAccounts:
        displayList += "{} - Carrier ID: {} - Nickname: {} - Account: {} - Primary Account: {} - Multi-Package Support: {}\n".format(sessionSeller.carrierAccounts[carrier]["carrier_account"], carrier, sessionSeller.carrierAccounts[carrier]["nickname"], sessionSeller.carrierAccounts[carrier]["account_number"], sessionSeller.carrierAccounts[carrier]["primary_account"], sessionSeller.carrierAccounts[carrier]["multi_package_available"])

    return displayList


def displayShipments(sessionSeller):
    if not sessionSeller.shipmentList:
        return "No shipments created in this session...yet!\n"

    displayList = ""

    for shipment in sessionSeller.shipmentList:
        displayList += "Shipment {} - Ship To: {}, {}, {} - Ship From: {}, {}, {} - Number of Packages: {}\n".format(shipment, sessionSeller.shipmentList[shipment]["ship_to"]["name"], sessionSeller.shipmentList[shipment]["ship_to"]["city"], sessionSeller.shipmentList[shipment]["ship_to"]["state"], sessionSeller.shipmentList[shipment]["ship_from"]["name"], sessionSeller.shipmentList[shipment]["ship_from"]["city"], sessionSeller.shipmentList[shipment]["ship_from"]["state"], sessionSeller.shipmentList[shipment]["number_of_packages"])

    return displayList


def displayRates(sessionSeller):
    if not sessionSeller.rateList:
        return "No saved rates, time to go shopping (for rates)!\n"

    displayList = ""

    sessionRates = sessionSeller.rateList

    for rates in sessionRates:
        displayList += "Request {} rates for shipment {} using carrier {}: {} ({}), quoted on {}.\n".format(rates, sessionRates[rates]["shipment_id"], sessionRates[rates]["carrier_id"], sessionRates[rates]["carrier_code"], sessionRates[rates]["carrier_nickname"], sessionRates[rates]["created_at"])

        rateEntry = ""

        for rate in sessionRates[rates]["returned_rates"]:
            if sessionRates[rates]["returned_rates"][rate]["package_type"] == None:
                rateEntry += "\nRate ID: {} - {}\n  Delivery Days: {} - Estimated Delivery Date: {} - Trackable: {}\n  Shipping Amount: {} {} - Insurance Amount: {} {} - Confirmation Amount: {} {} - Other Amount: {} {}".format(rate, sessionRates[rates]["returned_rates"][rate]["service_type"], sessionRates[rates]["returned_rates"][rate]["delivery_days"], sessionRates[rates]["returned_rates"][rate]["estimated_delivery_date"], sessionRates[rates]["returned_rates"][rate]["trackable"], sessionRates[rates]["returned_rates"][rate]["shipping_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["shipping_amount"]["currency"].upper(), sessionRates[rates]["returned_rates"][rate]["insurance_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["insurance_amount"]["currency"].upper(), sessionRates[rates]["returned_rates"][rate]["confirmation_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["confirmation_amount"]["currency"].upper(), sessionRates[rates]["returned_rates"][rate]["other_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["other_amount"]["currency"].upper())
            else:
                rateEntry += "\nRate ID: {} - {} [{}]\n  Delivery Days: {} - Estimated Delivery Date: {} - Trackable: {}\n  Shipping Amount: {} {} - Insurance Amount: {} {} - Confirmation Amount: {} {} - Other Amount: {} {}".format(rate, sessionRates[rates]["returned_rates"][rate]["service_type"], sessionRates[rates]["returned_rates"][rate]["package_type"], sessionRates[rates]["returned_rates"][rate]["delivery_days"], sessionRates[rates]["returned_rates"][rate]["estimated_delivery_date"], sessionRates[rates]["returned_rates"][rate]["trackable"], sessionRates[rates]["returned_rates"][rate]["shipping_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["shipping_amount"]["currency"].upper(), sessionRates[rates]["returned_rates"][rate]["insurance_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["insurance_amount"]["currency"].upper(), sessionRates[rates]["returned_rates"][rate]["confirmation_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["confirmation_amount"]["currency"].upper(), sessionRates[rates]["returned_rates"][rate]["other_amount"]["amount"], sessionRates[rates]["returned_rates"][rate]["other_amount"]["currency"].upper())

        displayList += rateEntry + "\n"

    return displayList


def displayLabels(sessionSeller):
    if len(sessionSeller.labelList) == 0:
        return "Labels anxiously awaiting generation: create a shipment, select a rate, get to shipping."

    displayList = ""

    for each in sessionSeller.labelList:
        displayList += "Label {0} - Status: {1} - Shipment ID: {2} - Ship Date: {3} - Create Date: {4}\n   Carrier ID: {5} - Service Code: {6} - Package Code: {7} - Shipment Cost {8} {9} - Insurance Cost - {10} {11}\n   Tracking Number: {12} - Return Label: {13} - Label Voided: {14}\n   Label URL: {15}".format(each, sessionSeller.labelList[each]["status"], sessionSeller.labelList[each]["shipment_id"], sessionSeller.labelList[each]["ship_date"], sessionSeller.labelList[each]["created_at"], sessionSeller.labelList[each]["carrier_id"], sessionSeller.labelList[each]["service_code"], sessionSeller.labelList[each]["package_code"], sessionSeller.labelList[each]["shipment_cost"]["amount"], sessionSeller.labelList[each]["shipment_cost"]["currency"].upper(), sessionSeller.labelList[each]["insurance_cost"]["amount"], sessionSeller.labelList[each]["insurance_cost"]["currency"].upper(), sessionSeller.labelList[each]["tracking_number"], str(sessionSeller.labelList[each]["is_return_label"]).title(), str(sessionSeller.labelList[each]["label_voided"]).title(), sessionSeller.labelList[each]["label_url"])

    return displayList
