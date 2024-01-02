import re
from datetime import datetime

class HDFC:
    def __init__(self, txt):
        self.txt = txt
    def getAmount(self):
        pattern = 'Dear Customer, Rs\.([\d.]+) has been debited'
        match = re.search(pattern, self.txt)
        return float(match.group(1))

    def getDetails(self):
        pattern = 'to (.*?) on'
        match = re.search(pattern, self.txt)
        return match.group(1)

    def getDate(self):
        pattern = 'on (.*?)\. Your'
        match = re.search(pattern, self.txt)
        date = match.group(1)
        input_date = datetime.strptime(date, "%d-%m-%y")
        output_date = input_date.strftime("%Y-%m-%d")
        return output_date

class Phonepe:
    def __init__(self, txt):
        self.txt = txt
        self.mailObject = {}
    def getAmount(self):
        pattern = '₹ ([\d.]+) Txn'
        match = re.search(pattern, self.txt)
        return float(match.group(1))
    def getDetails(self):
        pattern = 'Paid to (.*?) ₹'
        match = re.search(pattern, self.txt)
        return match.group(1)
    def getDate(self):
        pattern = 'PhonePe (.*?) Paid to'
        match = re.search(pattern, self.txt)
        date = match.group(1)
        input_date = datetime.strptime(date, "%b %d, %Y")
        output_date = input_date.strftime("%Y-%m-%d")
        return output_date
    def getCategory(self):
        return "uncategorised"
    def getTime(self):
        return "12:00:00"
    def getMailObject(self):
        self.mailObject["amount"] = self.getAmount()
        self.mailObject["details"] = self.getDetails()
        self.mailObject["date"] = self.getDate()
        self.mailObject["time"] = self.getTime()
        self.mailObject["category"] = self.getCategory()
        return self.mailObject