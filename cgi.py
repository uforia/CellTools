#!/usr/bin/env python3

"""
Convert Wireshark CGIs to MCC+MNC+LAC+CI

CellGlobalIdOrServiceAreaIdFixedLength ::= OCTET STRING (SIZE (7))
   -- Refers to Cell Global Identification or Service Are Identification
   -- defined in 3GPP TS 23.003.
   -- The internal structure is defined as follows:
   -- octet 1 bits 4321               Mobile Country Code 1st digit
   --            bits 8765               Mobile Country Code 2nd digit
   -- octet 2 bits 4321               Mobile Country Code 3rd digit
   --            bits 8765               Mobile Network Code 3rd digit
   --                                         or filler (1111) for 2 digit MNCs
   -- octet 3 bits 4321               Mobile Network Code 1st digit
   --            bits 8765               Mobile Network Code 2nd digit
   -- octets 4 and 5                  Location Area Code according to 3GPP TS 24.008
   -- octets 6 and 7                  Cell Identity (CI) value or
   --                                         Service Area Code (SAC) value
   --                                         according to 3GPP TS 23.003

E.g.: "22 F8 10 09 DD DB 46" becomes: MCC=0d228, MNC=0d01, LAC=0x09DD, CI=0xDB46
"""

import sys
import traceback

def hex_to_dec(hex_str):
    return int(hex_str, 16)

def split_cgi(cgi):
    mcc = (cgi[:3][::-1] + cgi[3:4][::-1])[1:]
    mnc = cgi[4:6][::-1] if cgi[2].lower() == "f" else (cgi[4:6][::-1]+cgi[2])
    lac = hex_to_dec(cgi[6:10])
    cellid = hex_to_dec(cgi[10:])
    return mcc, mnc, lac, cellid

try:
    cgi = ''.join(sys.argv[1:]).lower().replace(' ','')
    mcc, mnc, lac, cellid = split_cgi(cgi)
    print("MCC:", mcc)
    print("MNC:", mnc)
    print("LAC:", lac)
    print("Cell ID:", cellid)
except:
    if not cgi:
        print(f"You need to specify a Wireshark CGI to run this script.")
    else:
        print(f"Could not convert Wireshark CGI {cgi} to MCC+MNC+LAC+CI!\n")
        print(traceback.format_exc())
