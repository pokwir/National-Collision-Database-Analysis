# %% [markdown]
# # Data Preprocessing

# %% [markdown]
# mapping data codes to dataset. 

# %%
import csv

def create_csv_from_text(input_text, output_filename):
    data = [line.split(maxsplit=1) for line in input_text.strip().split('\n')[1:]]

    with open(output_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Code", "Description"])
        csv_writer.writerows(data)

# %%
# Create a dictionary with the name of the file as the key and the contents (text fields) of the file as the value
file_dict = {
    "C_MNTH": \
            '''Code Description
            01 January
            02 February
            03 March
            04 April
            05 May
            06 June
            07 July
            08 August
            09 September
            10 October
            11 November
            12 December
            UU Unknown
            XX Jurisdiction does not provide this data element''', 
    "C_WDAY": \
            '''Code Description
            1 Monday
            2 Tuesday
            3 Wednesday
            4 Thursday
            5 Friday
            6 Saturday
            7 Sunday
            UU Unknown
            XX Jurisdiction does not provide this data element''',
    "C_SEV": \
            '''Code Description
            1 Collision producing at least one fatality 
            2 Collision producing non-fatal injury 
            U Unknown''', 
    "C_VEHS": \
    '''Code Description
            01-98 01-98 vehicles involved.
            99 99 or more vehicles involved.
            UU Unknown
            XX Jurisdiction does not provide this data element''',
    "C_CONF": \
            '''Code Description
            01 Hit a moving object
            02 Hit a stationary object
            03 Ran off left shoulder
            04 Ran off right shoulder
            05 Rollover on roadway
            06 Any other single vehicle collision configuration
            21 Rear-end collision
            22 Side swipe
            23 One vehicle passing to the left of the other, or left turn conflict
            24 One vehicle passing to the right of the other, or right turn conflict
            25 Any other two vehicle - same direction of travel configuration
            31 Head-on collision
            32 Approaching side-swipe
            33 Left turn across opposing traffic
            34 Right turn, including turning conflicts
            35 Right angle collision
            36 Any other two-vehicle 
            41 Hit a parked motor vehicle
            QQ Choice is other than the preceding values
            UU Unknown
            XX Jurisdiction does not provide this data element''',
        "C_RCFG": \
            '''Code Description
            01 Non-intersection
            02 At an intersection of at least two public roadways
            03 Intersection with parking lot entrance/exit, private driveway or laneway
            04 Railroad level crossing
            05 Bridge, overpass, viaduct
            06 Tunnel or underpass
            07 Passing or climbing lane
            08 Ramp
            09 Traffic circle
            10 Express lane of a freeway system
            11 Collector lane of a freeway system
            12 Transfer lane of a freeway system
            QQ Choice is other than the preceding values
            UU Unknown
            XX Jurisdiction does not provide this data element''',
    "C_WTHR": \
            '''Code Description
            1 Clear and sunny
            2 Overcast, cloudy but no precipitation
            3 Raining
            4 Snowing, not including drifting snow
            5 Freezing rain, sleet, hail
            6 Visibility limitation e.g. drifting snow, fog, smog, dust, smoke, mist
            7 Strong wind
            Q Choice is other than the preceding values
            U Unknown
            X Jurisdiction does not provide this data element''', 
    "C_RSUR": \
            '''Code Description
            1 Dry, normal
            2 Wet
            3 Snow
            4 Slush, wet snow
            5 Icy
            6 Sand/gravel/dirt
            7 Muddy
            8 Oil
            9 Flooded
            Q Choice is other than the preceding values 
            U Unknown
            X Jurisdiction does not provide data element''',
    "C_RALN": \
            '''Code Description
            1 Straight and level
            2 Straight with gradient
            3 Curved and level
            4 Curved with gradient
            5 Top of hill or gradient
            6 Bottom of hill or gradient
            Q Choice is other than the preceding values
            U Unknown
            X Jurisdiction does not provide this data element''', 
    "C_TRAF": \
        '''Code Description
                01 Traffic signals fully operational 
                02 Traffic signals in flashing mode 
                03 Stop sign
                04 Yield sign
                05 Warning sign
                06 Pedestrian crosswalk
                07 Police officer
                08 School guard, flagman
                09 School crossing
                10 Reduced speed zone
                11 No passing zone sign
                12 Markings on the road
                13 School bus stopped with school bus signal lights flashing 
                14 School bus stopped with school bus signal lights not flashing 
                15 Railway crossing with signals, or signals and gates
                16 Railway crossing with signs only
                17 Control device not specified
                18 No control present
                QQ Choice is other than the preceding values
                UU Unknown
                XX Jurisdiction does not provide this data element''', 
        "V_ID": \
                '''Code Description
                99 Pedestrian''', 
        "V_TYPE": \
                '''Code Description
                01 Light Duty Vehicle
                05 Panel/cargo van
                06 Other trucks and vans
                07 Unit trucks
                08 Road tractor
                09 School bus
                10 Smaller school bus
                11 Urban and Intercity Bus
                14 Motorcycle and moped
                16 Off road vehicles
                17 Bicycle
                18 Purpose-built motorhome
                19 Farm equipment
                20 Construction equipment
                21 Fire engine
                22 Snowmobile
                23 Streetcar
                NN Data element is not applicable
                QQ Choice is other than the preceding values
                UU Unknown
                XX Jurisdiction does not provide this data element''', 
        "V_YEAR": \
                '''Code Description
                UUUU Unknown
                NNNN Data element is not applicable
                XXXX Jurisdiction does not provide this data element''', 
        "P_ID": \
                '''Code Description
                NN Data element is not applicable
                UU Unknown''', 
        "P_SEX": \
                '''Code Description
                M Male
                F Female
                N Not Applicable, 
                UU Unknown''',
        "P_AGE": \
                '''Code Description
                UU Unknown
                NN Data element is not applicable
                XX Jurisdiction does not provide this data element''',
        "P_PSN": \
                '''Code Description
                11 Driver
                12 Front row, center
                13 Front row, right outboard, including motorcycle passenger in sidecar
                21 Second row, left outboard, including motorcycle passenger
                22 Second row, center
                23 Second row, right outboard
                31 Third row, left outboard
                32 Third row, center
                33 Third row, right outboard
                96 Position unknown, but the person was definitely an occupant
                97 Sitting on someone’s lap
                98 Outside passenger compartment
                99 Pedestrian
                NN Data element is not applicable
                QQ Choice is other than the preceding values
                UU Unknown
                XX Jurisdiction does not provide this data element''',
        "P_ISEV": \
                '''Code Description
                1 No Injury
                2 Injury
                3 Fatality
                N Data element is not applicable 
                U Unknown
                X Jurisdiction does not provide this data element''',
        "P_SAFE": \
                '''Code Description
                01 No safety device used, or No child restraint used
                02 Safety device used or child restraint used
                09 Helmet worn
                10 Reflective clothing worn
                11 Both helmet and reflective clothing used
                12 Other safety device used
                13 No safety device equipped
                NN Data element is not applicable
                QQ Choice is other than the preceding values
                UU Unknown
                XX Jurisdiction does not provide this data element''', 
        "P_USER": \
                '''Code Description
                1 Motor Vehicle Driver
                2 Motor Vehicle Passenger
                3 Pedestrian
                4 Bicyclist
                5 Motorcyclist
                U Not stated / Other / Unknown'''
}

# %%
# get the first text in file_dict
file_dict['P_USER']


# %%


# %%

for file in file_dict:
    create_csv_from_text(input_text=file_dict[file], output_filename=file+".csv")


# %%
!pwd

# %%



