import math
import json

# input = [x for x in range(58)] # input list

# output = { } # output dict k : v => int : list

# block_size = 10
# no_of_blocks = math.ceil(len(input) / block_size)

# block_start = 0
# for key in range( no_of_blocks ):
# 	output[ key ] = input[ block_start : block_start + block_size ]
# 	block_start += block_size
	
# # print(output) # dictionary form

# output_json = json.dumps( output )

# print( output_json ) # { '0' : [ ... ], '1' : [ ... ], ... }

data = [
    {
        "faceId": "c5c24a82-6845-4031-9d5d-978df9175426",
        "candidates": [
            {
                "personId": "25985303-c537-4467-b41d-bdb45cd95ca1",
                "confidence": []
            }
        ]
    },
    {
        "faceId": "65d083d4-9447-47d1-af30-b626144bf0fb",
        "candidates": [
            {
                "personId": "2ae4935b-9659-44c3-977f-61fac20d0538",
                "confidence": 0.89
            }
        ]
    },
	{
        "faceId": "65d083d4-9447-47d1-af30-b626144bf0fb",
        "candidates": [
            {
                "personId": "2ae4935b-9659-44c3-977f-61fac20d0538",
                "confidence": 1
            }
        ]
    }
]

# person_ids = list(map( lambda x: x["candidates"][0]["personId"] if (x["candidates"][0]["confidence"]) else None, data )) 

person_ids = [x["candidates"][0]["personId"] for x in data if x["candidates"][0]["confidence"]]
print(person_ids)	