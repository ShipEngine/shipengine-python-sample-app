
class Seller:
    def __init__(self, apiKey, validKey):
        self.apiKey = apiKey
        self.validKey = validKey
        self.carrierAccounts = {}
        self.shipmentList = {}
        self.rateList = {}
        self.testLabelChecker = {}
        self.labelList = {}


    def setSellerCarriers(self, carrierJson):
        self.carrierAccounts = {}

        for carrier in carrierJson["carriers"]:
            self.carrierAccounts[carrier["carrier_id"]] = {"carrier_account": carrier["friendly_name"],"nickname": carrier["nickname"],"account_number": carrier["account_number"],"primary_account": carrier["primary"],"multi_package_available": carrier["has_multi_package_supporting_services"]}


    def addShipment(self, shipment):
        self.shipmentList[shipment["shipment_id"]] = {"create_date": shipment["create_date"], "ship_to": {"name": shipment["ship_to"]["name"], "city": shipment["ship_to"]["city"], "state": shipment["ship_to"]["state"]}, "ship_from": {"name": shipment["ship_from"]["name"], "city": shipment["ship_from"]["city"], "state": shipment["ship_from"]["state"]}, "number_of_packages": shipment["number_of_packages"]}


    def addRates(self, rateFeed):
        newEntry = {}
        newEntry["shipment_id"] = rateFeed["shipment_id"]
        newEntry["created_at"] = rateFeed["created_at"]
        newEntry["carrier_id"] = rateFeed["rate_response"]["rates"][0]["carrier_id"]
        newEntry["carrier_code"] = rateFeed["rate_response"]["rates"][0]["carrier_code"]
        newEntry["carrier_nickname"] = rateFeed["rate_response"]["rates"][0]["carrier_nickname"]
        newEntry["returned_rates"] = {}


        for rate in rateFeed["rate_response"]["rates"]:
            newEntry["returned_rates"][rate["rate_id"]] = {}
            newEntry["returned_rates"][rate["rate_id"]]["service_type"] = rate["service_type"]
            newEntry["returned_rates"][rate["rate_id"]]["service_code"] = rate["service_code"]
            newEntry["returned_rates"][rate["rate_id"]]["package_type"] = rate["package_type"]
            newEntry["returned_rates"][rate["rate_id"]]["shipping_amount"] = rate["shipping_amount"]
            newEntry["returned_rates"][rate["rate_id"]]["insurance_amount"] = rate["insurance_amount"]
            newEntry["returned_rates"][rate["rate_id"]]["confirmation_amount"] = rate["confirmation_amount"]
            newEntry["returned_rates"][rate["rate_id"]]["other_amount"] = rate["other_amount"]
            newEntry["returned_rates"][rate["rate_id"]]["trackable"] = rate["trackable"]
            newEntry["returned_rates"][rate["rate_id"]]["delivery_days"] = rate["delivery_days"]
            newEntry["returned_rates"][rate["rate_id"]]["estimated_delivery_date"] = rate["estimated_delivery_date"]
            newEntry["returned_rates"][rate["rate_id"]]["warning_messages"] = rate["warning_messages"]
            newEntry["returned_rates"][rate["rate_id"]]["error_messages"] = rate["error_messages"]

            self.testLabelChecker[rate["rate_id"]] = rate["carrier_code"]

        self.rateList[rateFeed["rate_response"]["rate_request_id"]] = newEntry


    def addLabel(self, labelFeed):
        self.labelList[labelFeed["label_id"]] = {}
        self.labelList[labelFeed["label_id"]]["status"] = labelFeed["status"]
        self.labelList[labelFeed["label_id"]]["shipment_id"] = labelFeed["shipment_id"]
        self.labelList[labelFeed["label_id"]]["ship_date"] = labelFeed["ship_date"]
        self.labelList[labelFeed["label_id"]]["created_at"] = labelFeed["created_at"]
        self.labelList[labelFeed["label_id"]]["shipment_cost"] = {"currency": labelFeed["shipment_cost"]["currency"], "amount": labelFeed["shipment_cost"]["amount"]}
        self.labelList[labelFeed["label_id"]]["insurance_cost"] = {"currency": labelFeed["insurance_cost"]["currency"], "amount": labelFeed["insurance_cost"]["amount"]}
        self.labelList[labelFeed["label_id"]]["tracking_number"] = labelFeed["tracking_number"]
        self.labelList[labelFeed["label_id"]]["is_return_label"] = labelFeed["is_return_label"]
        self.labelList[labelFeed["label_id"]]["carrier_id"] = labelFeed["carrier_id"]
        self.labelList[labelFeed["label_id"]]["service_code"] = labelFeed["service_code"]
        self.labelList[labelFeed["label_id"]]["package_code"] = labelFeed["package_code"]
        self.labelList[labelFeed["label_id"]]["label_voided"] = labelFeed["voided"]
        self.labelList[labelFeed["label_id"]]["label_url"] = labelFeed["label_download"]["href"]
        self.labelList[labelFeed["label_id"]]["packages"] = 0

        for each in labelFeed["packages"]:
            self.labelList[labelFeed["label_id"]]["packages"] += 1

    def voidLabel(self, labelId):
        pass
