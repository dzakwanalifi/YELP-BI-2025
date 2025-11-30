import csv
import re
import os

# Data raw strings provided by the user
data_2024 = """
Bogor	50.168,52	59,73	299.675,82
Sukabumi	81.612,30	57,20	466.835,93
Cianjur	105.305,70	59,91	630.847,78
Bandung	51.947,62	64,33	334.188,58
Garut	71.635,66	63,51	454.937,51
Tasikmalaya	66.324,47	53,29	353.415,07
Ciamis	44.307,13	53,32	236.248,23
Kuningan	41.522,97	53,81	223.427,76
Cirebon	84.465,74	60,45	510.632,02
Majalengka	87.220,48	55,50	484.085,66
Sumedang	49.430,79	55,00	271.869,00
Indramayu	212.866,19	65,74	1.399.352,12
Subang	163.881,64	59,12	968.941,45
Purwakarta	30.629,17	58,90	180.397,10
Karawang	183.065,46	56,89	1.041.530,95
Bekasi	84.199,55	49,46	416.476,98
Bandung Barat	27.566,67	53,98	148.802,98
Pangandaran	24.131,55	48,98	118.188,45
Kota Bogor	28,35	53,05	150,39
Kota Sukabumi	2.337,35	58,58	13.693,10
Kota Bandung	940,85	69,59	6.547,70
Kota Cirebon	99,81	63,94	638,23
Kota Bekasi	282,68	42,86	1.211,69
Kota Depok	5,82	56,24	32,73
Kota Cimahi	70,93	61,38	435,34
Kota Tasikmalaya	6.532,64	54,19	35.403,54
Kota Banjar	4.782,04	60,46	28.913,80
"""

data_2023 = """
Bogor	50.999,48	55,54	283.266,58
Sukabumi	93.866,34	54,59	512.391,58
Cianjur	115.749,72	56,17	650.123,11
Bandung	49.366,27	60,80	300.142,89
Garut	74.538,34	60,88	453.787,94
Tasikmalaya	69.685,72	56,16	391.379,69
Ciamis	53.976,46	55,42	299.124,49
Kuningan	44.815,65	58,24	261.023,34
Cirebon	82.797,11	59,89	495.878,20
Majalengka	100.124,09	55,77	558.430,27
Sumedang	53.525,51	53,64	287.112,51
Indramayu	230.456,96	61,80	1.424.303,10
Subang	174.864,99	58,77	1.027.659,54
Purwakarta	31.884,84	58,50	186.533,23
Karawang	189.064,62	59,87	1.131.976,57
Bekasi	93.338,02	53,28	497.339,49
Bandung Barat	26.709,13	53,62	143.212,52
Pangandaran	30.250,90	46,05	139.300,30
Kota Bogor	25,76	47,99	123,61
Kota Sukabumi	2.699,69	59,96	16.187,08
Kota Bandung	901,17	70,19	6.325,63
Kota Cirebon	137,10	56,12	769,39
Kota Bekasi	306,86	42,90	1.316,49
Kota Depok	5,82	52,42	30,51
Kota Cimahi	76,61	57,50	440,48
Kota Tasikmalaya	7.863,88	50,83	39.968,81
Kota Banjar	5.625,24	56,69	31.891,85
"""

data_2022 = """
Bogor	56.002,23	53,55	299.893,80
Sukabumi	95.012,99	53,49	508.220,48
Cianjur	115.877,18	53,33	617.941,03
Bandung	47.537,79	60,84	289.205,70
Garut	75.951,04	58,11	441.316,20
Tasikmalaya	81.310,17	53,00	430.961,73
Ciamis	55.844,25	54,74	305.676,17
Kuningan	48.250,13	57,53	277.583,76
Cirebon	84.892,18	58,27	494.699,98
Majalengka	100.950,53	56,08	566.087,34
Sumedang	56.662,01	52,62	298.163,00
Indramayu	245.329,29	60,42	1.482.255,86
Subang	177.986,35	58,36	1.038.780,58
Purwakarta	34.396,95	54,87	188.731,69
Karawang	204.326,26	60,05	1.226.880,08
Bekasi	103.088,97	53,91	555.747,09
Bandung Barat	29.201,93	52,62	153.648,29
Pangandaran	30.115,90	49,37	148.670,61
Kota Bogor	32,21	54,02	173,99
Kota Sukabumi	2.176,04	60,91	13.254,34
Kota Bandung	995,22	72,21	7.186,11
Kota Cirebon	159,80	53,93	861,82
Kota Bekasi	454,07	41,15	1.868,44
Kota Depok	14,55	49,57	72,13
Kota Cimahi	59,59	56,73	338,03
Kota Tasikmalaya	9.797,97	55,35	54.233,66
Kota Banjar	5.978,36	52,31	31.271,18
"""

data_2021 = """
Bogor	57 426,46	49,66	285 154,00
Sukabumi	89 510,44	55,07	492 926,27
Cianjur	113 538,50	53,88	611 773,02
Bandung	50 552,68	61,46	310 715,20
Garut	75 965,56	58,36	443 319,91
Tasikmalaya	82 934,85	53,77	445 909,19
Ciamis	55 013,02	58,23	320 330,73
Kuningan	47 236,30	58,41	275 893,22
Cirebon	84 946,29	54,71	464 730,69
Majalengka	97 515,62	54,79	534 250,18
Sumedang	53 341,28	49,12	262 037,84
Indramayu	227 051,34	58,12	1 319 623,64
Subang	163 946,73	58,52	959 456,43
Purwakarta	32 930,64	50,98	167 865,29
Karawang	197 916,26	62,36	1 234 133,75
Bekasi	100 338,32	58,56	587 586,07
Bandung Barat	27 654,55	52,97	146 494,62
Pangandaran	27 677,79	50,58	140 000,72
Kota Bogor	36,09	47,69	172,10
Kota Sukabumi	2 456,16	61,57	15 123,41
Kota Bandung	1 025,58	69,21	7 097,77
Kota Cirebon	231,68	53,72	1 244,61
Kota Bekasi	477,98	48,21	2 304,54
Kota Depok	45,39	53,83	244,35
Kota Cimahi	76,62	57,78	442,71
Kota Tasikmalaya	8 539,85	57,52	49 118,08
Kota Banjar	5 723,33	62,24	35 624,74
"""

data_2020 = """
Bogor	55 692,05	53,68	298 974,65
Sukabumi	93 371,47	55,85	521 459,25
Cianjur	113 856,46	54,72	622 992,32
Bandung	50 150,32	55,27	277 156,28
Garut	77 873,41	54,56	424 913,90
Tasikmalaya	72 941,41	60,92	444 358,24
Ciamis	52 925,20	53,43	282 791,46
Kuningan	45 785,65	60,57	277 317,90
Cirebon	83 233,39	59,72	497 080,10
Majalengka	98 037,63	57,77	566 334,48
Sumedang	55 892,07	54,96	307 178,00
Indramayu	226 626,09	60,16	1 363 311,87
Subang	169 416,08	57,30	970 759,74
Purwakarta	30 315,68	52,76	159 957,49
Karawang	181 915,22	59,80	1 087 873,90
Bekasi	103 171,69	48,86	504 103,31
Bandung Barat	29 196,89	56,39	164 640,49
Pangandaran	29 313,07	52,87	154 982,57
Kota Bogor	33,32	45,70	152,26
Kota Sukabumi	2 335,74	62,22	14 532,67
Kota Bandung	1 074,49	63,28	6 799,08
Kota Cirebon	225,82	45,67	1 031,24
Kota Bekasi	483,64	56,30	2 723,05
Kota Depok	30,99	61,06	189,23
Kota Cimahi	77,49	56,45	437,44
Kota Tasikmalaya	7 569,30	48,02	36 349,80
Kota Banjar	5 344,06	53,09	28 371,86
"""

def clean_number(num_str):
    """
    Cleans number string:
    - Removes spaces (thousand separators in 2020/2021)
    - Removes dots (thousand separators in 2022-2024)
    - Replaces comma with dot (decimal separator)
    """
    if not num_str:
        return 0.0
    
    # Remove spaces
    num_str = num_str.replace(" ", "")
    # Remove dots (thousand separators)
    num_str = num_str.replace(".", "")
    # Replace comma with dot
    num_str = num_str.replace(",", ".")
    
    try:
        return float(num_str)
    except ValueError:
        return 0.0

def parse_data(year, data_str):
    records = []
    lines = data_str.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Try splitting by tab first
        parts = line.split('\t')
        
        # If not enough parts, try splitting by multiple spaces (2 or more)
        if len(parts) < 4:
            parts = re.split(r'\s{2,}', line)
            
        if len(parts) >= 4:
            city = parts[0].strip()
            luas_panen_str = parts[1].strip()
            produktivitas_str = parts[2].strip()
            produksi_str = parts[3].strip()
            
            # Skip "Jawa Barat" total row
            if city.lower() == "jawa barat":
                continue
                
            record = {
                'year': year,
                'kabupaten_kota': city,
                'luas_panen_ha': clean_number(luas_panen_str),
                'produktivitas_ku_ha': clean_number(produktivitas_str),
                'produksi_ton': clean_number(produksi_str)
            }
            records.append(record)
        else:
            # Fallback regex for lines that might have single spaces as separators but no internal spaces in numbers (unlikely for 2020/2021)
            # Or if the copy-paste lost the tabs.
            # Let's try a regex that looks for the last 3 numbers
            match = re.search(r'^(.*?)\s+([\d\s\.]*,\d+)\s+([\d\s\.]*,\d+)\s+([\d\s\.]*,\d+)$', line)
            if match:
                 city = match.group(1).strip()
                 luas_panen_str = match.group(2).strip()
                 produktivitas_str = match.group(3).strip()
                 produksi_str = match.group(4).strip()
                 
                 if city.lower() == "jawa barat":
                    continue

                 record = {
                    'year': year,
                    'kabupaten_kota': city,
                    'luas_panen_ha': clean_number(luas_panen_str),
                    'produktivitas_ku_ha': clean_number(produktivitas_str),
                    'produksi_ton': clean_number(produksi_str)
                 }
                 records.append(record)
            else:
                print(f"Warning: Could not parse line in {year}: {line}")
            
    return records

all_records = []
all_records.extend(parse_data(2024, data_2024))
all_records.extend(parse_data(2023, data_2023))
all_records.extend(parse_data(2022, data_2022))
all_records.extend(parse_data(2021, data_2021))
all_records.extend(parse_data(2020, data_2020))

# Sort by Year (descending) and then City
all_records.sort(key=lambda x: (-x['year'], x['kabupaten_kota']))

output_dir = "bps-jakarta-data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, "jawa_barat_rice_production_2020_2024.csv")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['year', 'kabupaten_kota', 'luas_panen_ha', 'produktivitas_ku_ha', 'produksi_ton']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for record in all_records:
        writer.writerow(record)

print(f"Successfully created {output_file} with {len(all_records)} records.")
