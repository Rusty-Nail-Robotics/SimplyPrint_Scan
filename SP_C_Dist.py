import requests
import json
import os
import time

filament0_id = None
filament1_id = None
urlID = "{Your URL ID Here}"#{Your URL ID Here}
headers = {
			'X-API-KEY': '{Your API KEY Here}', #{Your API KEY Here},
			'accept': 'application/json',
			'content-type': 'application/json'
			}

def main():
	
	while(True):
		
		printerIDs = []
		#request_Filament_UIDs()
		Printers_and_Filaments = []
		#printer_id = 20581
		Printers_and_Filaments = extract_printer_and_filament()
		#print(Printers_and_Filaments)
		printer_dict = {item['printer_id']: item for item in Printers_and_Filaments}
		#print(printer_dict)
		#print(printer_dict.get(20102).get("extruder_0"))
		for i in Printers_and_Filaments:
			#print(f"{i.get('printer_name')} ID {i.get('printer_id')} ")
			#print(f"	Extruder 0 is loaded with {get_filament_uid_by_id(i.get('extruder_0'))}/{i.get('extruder_0')}")
			#print(f"	Extruder 1 is loaded with {get_filament_uid_by_id(i.get('extruder_1'))}/{i.get('extruder_1')}")
			printerIDs.append(int(i.get('printer_id')))
		#print(printerIDs) 
		initial_Input = str(input("Scan Extruder or Task Barcode "))
		if(initial_Input == "DELETE"):
			Delete_Filament()
		elif(initial_Input == "UNASSIGN"):
			print("Unassign Function Not Setup")
			time.sleep(5)
		else:
			Assign_Filament(initial_Input, printerIDs, printer_dict)
		
		os.system('cls')
	
def Delete_Filament():
	global headers
	global urlID
	filamentToDelete = input("Scan Filament to DELETE Barcode")
	if(filamentToDelete == "ABORT" or filamentToDelete == "ASSIGN"):
		return;
	filamentToDelete = filamentToDelete[-4:]
	filamentToDelete = str(get_filament_id_by_uid(filamentToDelete))
	confirm_DELETE = input(f"Confirm Filament {filamentToDelete} Will be PERMENENTLY DELETED. Scan DELETE To confirm or ABORT to Cancel")
	if(confirm_DELETE == "ABORT"):
		return
	elif(confirm_DELETE == "DELETE"):
		deleteFilanemtURL = f'https://api.simplyprint.io/{urlID}/filament/Delete?fid='
		
			
		params = {
			"fid": filament0_id
			}
	
		deleteFilanemtURL = deleteFilanemtURL+filamentToDelete
		response = requests.get(deleteFilanemtURL, headers=headers)
		data = json.loads(response.text)
		

		print(deleteFilanemtURL)
		print(response)
		print(data)
		time.sleep(15)
	else:
		print("Confirmation Scan Unrecognised")
		time.sleep(5)
		
		
			
def Assign_Filament(printerToChange, printerIDs, printer_dict):
			
			if(printerToChange == "ABORT"):
				return;
			printerToChange = printerToChange.split()
			if(len(printerToChange) != 2):
				print("Input must be 2 items.  'printer id' 'extruder'.  ex. '20102 1'")
				time.sleep(2)
			else:
				print(printerToChange[0])
				if int(printerToChange[0]) in printerIDs:
					extruderToChange = printerToChange[1]
					print(f"Extruder {extruderToChange} on {printer_dict.get(int(printerToChange[0])).get("printer_name")} Selected")
					scannedInput = input("Scan Filament Barcode")
					scannedInput = scannedInput[-4:]
					print(scannedInput)
				
					if(extruderToChange == "0"):
						filament0_id = get_filament_id_by_uid(scannedInput.upper())
						print(filament0_id)
						filament1_id = None# 
						result = assign_filament_to_printer(int(printerToChange[0]), filament0_id, filament1_id)
					elif(extruderToChange == "1"):
						filament1_id = get_filament_id_by_uid(scannedInput.upper())
						print(filament1_id)
						filament0_id = None
						result = assign_filament_to_printer(int(printerToChange[0]), filament0_id, filament1_id)
					else:
						print("Extruder Must be a 1 ir 0")
						time.sleep(5)
					print("OK")
					print(result)
				else:
					print("Printer Not Found")
					
		

	
	
def extract_printer_and_filament():
	global headers
	global urlID
	getFilanemtURL = f'https://api.simplyprint.io/{urlID}/printers/Get/'
	response = requests.get(getFilanemtURL, headers=headers)
	data = json.loads(response.text)
	result = []
	
	if data["status"]:
		printers = data["data"]
	for printer_info in printers:
		#print(printer_info)
		#printer_data = printer_info("printer")
		printer_id = printer_info.get('id')
		
		printer_name = printer_info.get('printer').get('name')
		#print(printer_name)
		filament_data = printer_info.get('filament', {})
		#print(f"Printer ID {printer_id}")
		#print(filament_data)
        # Extract only the 'id' for extruder 0
		if(filament_data != None):
			extruder_0 = filament_data.get('0', {})
			extruder_0_info = extruder_0.get('id')
			#print(f"Extruder 0 filament ID is: {extruder_0_info}")
		

			# Extract only the 'id' for extruder 1
			extruder_1 = filament_data.get('1', {})
			extruder_1_info = extruder_1.get('id')
			#print(f"Extruder 1 filament ID is: {extruder_1_info}")
		else:
			extruder_0_info = None
			extruder_1_info = None

        # Create an array containing printer id and the filament data for extruders 0 and 1
		result.append({
			'printer_name': printer_name,
            'printer_id': printer_id,
            'extruder_0': extruder_0_info,
            'extruder_1': extruder_1_info
        })

	return result	
	
def request_Filament_UIDs():
	global filament0_id
	global filament1_id
	while(filament1_id == None):
		filament0UID = input("Extruder 0 Filament UID ").upper()
		filament0_id = get_filament_id_by_uid(filament0UID)	
		print(filament0_id)
		
	while(filament1_id == None):	
		filament1UID = input("Extruder 1 Filament UID ").upper()
		filament1_id = get_filament_id_by_uid(filament1UID)
		print(filament1_id)

def get_filament_uid_by_id(fid):
	global headers
	global urlID
	getFilanemtURL = f'https://api.simplyprint.io/{urlID}/filament/GetFilament/'
	response = requests.get(getFilanemtURL, headers=headers)
	json_data = json.loads(response.text)
	filament_info = []
	
	for key, filament in json_data["filament"].items():
		filament_info.append([filament["id"], filament["uid"]])
		
    # Iterate over the filament data
	for filament in json_data["filament"].values():
        # Check if the uid matches
		if filament["id"] == fid:
			return filament["uid"]
    # Return None if no match is found
	return None
	
def get_filament_id_by_uid(uid):
	global headers
	global urlID
	getFilanemtURL = f'https://api.simplyprint.io/{urlID}/filament/GetFilament/'
	
	response = requests.get(getFilanemtURL, headers=headers)
	json_data = json.loads(response.text)
	filament_info = []
	
	for key, filament in json_data["filament"].items():
		filament_info.append([filament["id"], filament["uid"]])
		
    # Iterate over the filament data
	for filament in json_data["filament"].values():
        # Check if the uid matches
		if filament["uid"] == uid:
			return filament["id"]
    # Return None if no match is found
	return None

def assign_filament_to_printer(printer_id, filament0_id, filament1_id):
	global headers
	global urlID
	url = f"https://api.simplyprint.io/{urlID}/filament/Assign"

	print(filament0_id)
	print(filament1_id)
	if(filament0_id == None):
		params = {
        "pid": printer_id,
        "fid": filament1_id
		}
		data = {
			"extruder": {
			filament1_id: 1
			}
			}
	elif(filament1_id == None):
			params = {
        "pid": printer_id,
		"fid": filament0_id
	}
			data = {
			"extruder": {
			filament0_id: 0
			}
			}
	else:
			params = {
        "pid": printer_id,
        "fid": f"{filament0_id},{filament1_id}"
	}
			data = {
			"extruder": {
				filament0_id: 0,
				filament1_id: 1
			}
			}

    # Make the POST request
	response = requests.post(url, params=params, headers=headers, json=data)
	print(data)
    # Check the response
	if response.status_code == 200:
		return response.json()  # Success: return the response JSON
	else:
		return {"error": response.status_code, "message": response.text}  # Error: return the error details

if __name__ == '__main__':
    main()


