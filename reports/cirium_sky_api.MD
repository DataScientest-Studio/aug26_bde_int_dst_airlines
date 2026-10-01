# Cirium Sky API

# Airlines API:

## All Airlines:

https://api.sky.cirium.com/v1/airlines/

### Query Parameters:
- onlyAcive: boolean
Filters results to include only active airlines.
Default is true. If this parameter is omitted, all airlines (active and inactive) are returned.

### Header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

### Response:
- Airlines (Array of obects Airline):
Airline object: 
fs: string -> The Cirium code for the carrier, globally unique across time

iata: string -> The IATA code for the carrier

icao: string -> The ICAO code for the carrier

name: string -> The name of the carrier

phoneNumber: string -> The primary customer service phone number for the carrier

active: boolean -> Boolean value indicating if the airline is currently active

category: string
The category of operation of the airline:

    A - Scheduled Passenger Carrier
    B - Non-Scheduled Passenger Carrier
    C - Scheduled Cargo Carrier
    D - Non-Scheduled Cargo Carrier
    E - Railway Company
    F - Ferry Company
    G - Non-airline ULD (Cargo)
    H - Computer Reservation System
    I - Scheduled Passenger/Cargo Carrier
    J - Non-scheduled Passenger/Cargo Carrier
    K - Bus Company
    S - Miscellaneous/Other

## Airlines by Code

https://api.sky.cirium.com/v1/airlines/{code}/

### Path Parameters:
- **REQUIRED** code: string
Airline code value. The format depends on the codeType parameter:

    FS: 2–3 characters; may include letters (A–Z), digits (0–9), or an asterisk (*)
    IATA: 2 characters; letters (A–Z) or digits (0–9)
    ICAO: 3 letters (A–Z)

### Query Parameters:
- **REQUIRED** codeType: string
Enum: "FS" "IATA" "ICAO"
Specifies the type of airline code provided in the {code} path parameter.

### Header Parameters: 
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Delay Index API:

## Delay Indexes by Airport Code:

https://api.sky.cirium.com/v1/airports/delay-index/{airports}

### path Parameters
- **REQUIRED** airports: string
Example: PDX,SEA+BLI

One or more airport codes to retrieve Delay Index data for.
Multiple codes can be separated by punctuation characters such as commas or plus signs.
Accepted formats: IATA, ICAO, or Cirium FS airport codes.

Example: PDX,SEA+BLI

### query Parameters:
- classification: integer <int64> [ 1 .. 5 ]
Example: classification=1

Filters results to include airports up to the specified classification level.
Levels range from 1 (largest airports) to 5 (smallest).
For example, a value of 3 returns classifications 1, 2, and 3.

- score: integer <int64> [ 0 .. 5 ]
Example: score=1

Filters results by the normalized Delay Index score.
Values range from 0 (no delay) to 5 (maximum delay).
Used to identify airports currently experiencing delays.

- codeType: string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS

Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### Header Parameters: 
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

### Response:
delayIndexes: Array of objects DelayIndex

Airport: object airport

rawScore: number <double> -> A raw delay score for the airport based on the number of observations, departure delays, cancellations, and the time of day at the airport (not normalized)

normalizedScore: number <double>
The normalized delay score, from 0 to 5 in increments of .25 (where 5 is maximum delay)

    0 - Minimal disruption (delays and cancellations)
    2.5 - Moderate disruption (delays and cancellations)
    5 Severe disruption (delays and cancellations)

dateStart: string -> The date and time (UTC) of the start of the window for the current delay calculation in ISO-8601 format. yyyy-MM-ddTHH:mm:ss.SSSZ

dateEnd: string -> The date and time (UTC) of the end of the window for the current delay calculation in ISO-8601 format. yyyy-MM-ddTHH:mm:ss.SSSZ

flights: integer <int32> -> The count of all known flights at the airport for the given time window (whether tracked or not)

observations: integer <int32> -> The count of flights at the airport for the given time window that are included in the delay calculation (scheduled/tracked flights)

canceled: integer <int32> -> The count of flights at the airport for the given time window that were canceled

onTime: integer <int32> -> The count of flights at the airport for the given time window that are currently expected to be on-time

delayed15: integer <int32> -> The count of flights at the airport for the given time window that are currently expected to be delayed between 15 and 30 minutes

delayed30: integer <int32> -> The count of flights at the airport for the given time window that are currently expected to be delayed between 30 and 45 minutes

delayed45: integer <int32> -> The count of flights at the airport for the given time window that are currently expected to be delayed more than 45 minutes

delta: number <float> -> The percentage change in normalized score from the last period based on current observations. Positive values indicate worsening conditions, while negative values indicate improving conditions.

## Delay Indexes by Country Code:

https://api.sky.cirium.com/v1/airports/delay-index/country-code-iso/{countryCodeIso}

### path Parameters:
- **REQUIRED** countryCodeIso: string
Example: US
Two-letter ISO country code used to retrieve Delay Index data for all airports in the specified country.

### query Parameters: 
- classification: integer <int64> [ 1 .. 5 ]
Example: classification=1

Filters results to include airports up to the specified classification level.
Levels range from 1 (largest airports) to 5 (smallest).
For example, a value of 3 returns classifications 1, 2, and 3.

- score: integer <int64> [ 0 .. 5 ]
Example: score=1

Filters results by the normalized Delay Index score.
Values range from 0 (no delay) to 5 (maximum delay).
Used to identify airports currently experiencing delays.

### header Parameters
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

## Delay Indexes by Region: 

https://api.sky.cirium.com/v1/airports/delay-index/region/{region}

### path Parameters:
- **REQUIRED** region: string
Enum: "Africa" "Antarctica" "Asia" "Caribbean" "Central-America" "Europe" "Middle-East" "North-America" "Oceania" "South-America"
Example: North-America

Geographic region used to retrieve Delay Index data.
Must match one of the predefined region names.

### query Parameters: 
- classification: integer <int64> [ 1 .. 5 ]
Example: classification=1

Filters results to include airports up to the specified classification level.
Levels range from 1 (largest airports) to 5 (smallest).
For example, a value of 3 returns classifications 1, 2, and 3.

- score: integer <int64> [ 0 .. 5 ]
Example: score=1

Filters results by the normalized Delay Index score.
Values range from 0 (no delay) to 5 (maximum delay).
Used to identify airports currently experiencing delays.

### header Parameters
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.


## Delay Indexes by State Code: 

https://api.sky.cirium.com/v1/airports/delay-index/region/{state}

### path Parameters:
- **REQUIRED** state: string
 Example: OR

Two-letter U.S. state or Canadian province code used to retrieve Delay Index data for all airports within the specified area.

### query Parameters: 
- classification: integer <int64> [ 1 .. 5 ]
Example: classification=1

Filters results to include airports up to the specified classification level.
Levels range from 1 (largest airports) to 5 (smallest).
For example, a value of 3 returns classifications 1, 2, and 3.

- score: integer <int64> [ 0 .. 5 ]
Example: score=1

Filters results by the normalized Delay Index score.
Values range from 0 (no delay) to 5 (maximum delay).
Used to identify airports currently experiencing delays.

### header Parameters
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Airport API:

https://api.sky.cirium.com/v1/airports/

### query Parameters:
- onlyAcive: boolean
Filters results to include only active airlines.
Default is true. If this parameter is omitted, all airlines (active and inactive) are returned.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.


### Response: 

fs: string -> The Cirium code for the airport, globally unique across time

iata: string -> The IATA code for the airport

icao: string -> The ICAO code for the airport

faa: string -> The FAA code for the airport

name: string -> The name of the airport

street1: string -> The street address of the airport, part 1

street2: string -> The street address of the airport, part 2

city: string -> The city in which the airport resides

cityCode: string -> The code of the city in which the airport resides

stateCode: string -> The State in which the airport resides

postalCode: string -> The postal code in which the airport resides

countryCode: string -> The code for the country in which the airport resides

district: string -> The district of the city in which the airport resides. Returned if specifying includeNewFields in extendedOptions.

countryName: string -> The name of the country in which the Airport resides

regionName: string -> The name of the region in which the Airport resides

timeZoneRegionName: string -> The name of the Time Zone region in which the Airport resides

weatherZone: string -> The NOAA weather zone (US only) in which the Airport resides

localTime: string -> The local time at the Airport in ISO-8601 format. yyyy-MM-dd'T'HH:mm:ss.SSS.

utcOffsetHours: number <float> -> The current UTC offset at the Airport

latitude: number <float> -> The latitude of the airport in decimal degrees

longitude: number <float> -> The longitude of the airport in decimal degrees

elevationFeet: integer <int32> -> The elevation above sea level of the airport in feet

classification: integer <int32> -> The Cirium classification of the size of the airport, 1(max) to 5(min)

active: boolean -> Boolean value indicating if the airport is currently operational

dateFrom: string -> Ignore. These are not returned.

dateTo: string -> Ignore. These are not returned.

weatherUrl: string -> URL for the Weather service with current weather data for the Airport

delayIndexUrl: string -> URL for the DelayIndex service with current delay information computed for the Airport


## Airports by City Code:

https://api.sky.cirium.com/v1/airports/city-code-iata/{cityCodeIata}

### path parameter:
- **REQUIRED** cityCodeIata: string
IATA city code (3 letters).

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

## Airports by Country Code:

https://api.sky.cirium.com/v1/airports/country-code-iso/{countryCodeIso}

## path Parameters: 
- **REQUIRED** countryCodeIso: string
ISO 3166-1 alpha-2 country code (2 uppercase letters).
Examples: US for United States, GB for United Kingdom, FR for France.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

## Airport within radius: 

https://api.sky.cirium.com/v1/airports/latitude/{latitude}/longitude/{longitude}/radius-miles/{radiusMiles}

### path Parameters:
- **REQUIRED** latitude: number<float> [ -90 .. 90 ]
Example: 45.588995
Latitude of the search point center in decimal degrees. Must be between -90 and +90.

- **REQUIRED** longitude: number <float> [ -180 .. 180 ]
Example: -122.592901
Longitude of the search point center in decimal degrees. Must be between -180 and +180.


- **REQUIRED** radiusMiles: integer >= 1
Example: 8
Search radius in miles around the specific latitude and longitude. Defines the circular area used to find airports.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Equipment API:

## All Equipment:

https://api.sky.cirium.com/v1/equipment

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

## Response: 
iata: string -> The IATA code for the equipment type

name: string -> The descriptive name for the equipment type

turboProp: boolean -> Boolean value indicating if the equipment type uses TurboProp propulsion

jet: boolean -> Boolean value indicating if the equipment type uses jet propulsion

widebody: boolean -> Boolean value indicating if the equipment type is a wide-body airframe

regional: boolean -> Boolean value indicating if the equipment type is a regional airframe

## Equipment By IATA Code:

https://api.sky.cirium.com/v1/equipment/code-iata/{codeIata}

### path Parameters:
- **REQUIRED** codeIata: string
Three-character IATA equipment code used to retrieve aircraft information.
Consists of uppercase letters and/or digits (A–Z, 0–9).
Example: CRV

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Flight Status API:

## Flight Arrivals by Date:

https://api.sky.cirium.com/v1/flights/status/airline/{airline}/flight-number/{flightNumber}/arrival-date/{arrivalDate}

### path Parameters:
- **REQUIRED** airline: string
Code of the airline. Accepted formats:
    IATA – 2-character code, e.g. BA
    ICAO – 3-character code, e.g. BAW
    FS – Cirium unique code (2 or 3 alphanumeric characters)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** flightNumber: string
Flight number, excluding the airline code. Identifies a specific flight operated by the airline on a given day.
The value consists of 1 to 4 digits and may include an optional single uppercase letter as a suffix. Leading zeros are allowed.

For example:
    BA123 → flightNumber is 123
    DL045B → flightNumber is 045B

- **REQUIRED** arrivalDate: string <date>
Example: 2025-08-23
Date of arrival in YYYY-MM-DD format (ISO 8601), for example: 2025-10-01.
The date is interpreted in the local time of the arrival airport unless the utc flag is set to true.

### query Parameters:
- utc: 	boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- airport: string
Optional filter to restrict results to the arrival airport.

Accepted formats:
    IATA – 3-letter airport code, e.g. LAX
    ICAO – 4-letter airport code, e.g. KLAX
    FS - 3-4 alphanumeric characters, Cirium unique airport code

All formats are supported and matched in this order: IATA, ICAO, then FS.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.

Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.


### Response: 
schema: string

flightId: integer <int64> -> The unique identifier for the flight

carrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

carrierFsCode: string -> The Cirium unique code for the operating carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in Extended options)

operatingCarrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

operatingCarrierFsCode: string -> The Cirium unique code for the operating carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in Extended options). Returned if specifying includeNewFields in extendedOptions.

primaryCarrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

primaryCarrierFsCode: string -> The Cirium unique code for the primary carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in Extended options). Returned if specifying includeNewFields in extendedOptions.

flightNumber: string -> The flight identification number and any additional characters

departureAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

departureAirportFsCode: string -> The Cirium unique code for the departure airport to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in Extended options)

arrivalAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

arrivalAirportFsCode: string -> The Cirium unique code for the arrival airport to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in Extended options)

divertedAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

divertedAirportFsCode: string -> The Cirium unique code for the airport to which the flight was diverted, if any, to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in Extended options).

departureDate: object (DateUtcAndLocal)

arrivalDate: object (DateUtcAndLocal)

status: string
The current status of the flight. One of the following values:
    A - Active
    C - Canceled
    D - Diverted
    DN - Data Needed
    L - Landed
    NO - Not Operational
    R - Redirected
    S - Scheduled
    U - Unknown

schedule: object (Schedule)

operationalTimes: object (OperationalTimes)

codeshares: Array of objects (Codeshare) -> Zero or more marketing or operating relationships for this flight

delays: object (Delays) -> Any calculated delays for the flight based on operational times (scheduled, estimated and actual)

flightDurations: object (FlightDurations) -> Calculated flight durations based on operational times (scheduled, estimated and actual)

airportResources: object (AirportResources) -> Information related to the departure and arrival terminal, gate and baggage

flightEquipment: object (FlightEquipment) -> Information about the equipment used for this flight. May contain equipment objects inlined if specifying useInlinedReferences, otherwise the equipment can be looked up in the appendix using the codes provided.

flightStatusUpdates: Array of objects (FlightStatusUpdate) -> Contains a list of all updates that have occurred to this flight status since originally published. Included if the specifying includeDeltas in Extended options.

irregularOperations: Array of objects (IrregularOperation) -> A list of zero or more irregular operations that have occurred for this flight. Returned if specifying includeNewFields in extendedOptions.

confirmedIncident: object (ConfirmedIncident) -> This object contains information about a severe issue with the flight. Cirium manually publishes the message. It rarely is published, and usually is the result of an accident with the aircraft. The message is a textual description of what occurred. Returned if specifying includeNewFields in extendedOptions.

lastDataAcquiredDate: string <date-time> -> The last time the flight status data was acquired


## Flight Departures by Date:

https://api.sky.cirium.com/v1/flights/status/airline/{airline}/flight-number/{flightNumber}/departure-date/{departureDate}

### path Parameters:
- **REQUIRED** airline: string
Example: AS
Code of the airline. Accepted formats:
    IATA – 2-character code, e.g. BA
    ICAO – 3-character code, e.g. BAW
    FS – Cirium unique code (2 or 3 alphanumeric characters)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** flightNumber: string
Flight number, excluding the airline code. Identifies a specific flight operated by the airline on a given day.
The value consists of 1 to 4 digits and may include an optional single uppercase letter as a suffix. Leading zeros are allowed.

For example:
    BA123 → flightNumber is 123
    DL045B → flightNumber is 045B

- **REQUIRED** departureDate: string<date>
Date of departure in YYYY-MM-DD format (ISO 8601), for example: 2025-10-01.
The date is interpreted in the local time of the departure airport unless the utc flag is set to true.

### query Parameters:
- utc: boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- airport: string
Optional filter to restrict results to the arrival airport.

Accepted formats:
    IATA – 3-letter airport code, e.g. LAX
    ICAO – 4-letter airport code, e.g. KLAX
    FS - 3-4 alphanumeric characters, Cirium unique airport code

All formats are supported and matched in this order: IATA, ICAO, then FS.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.

Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

## Flight by ID:

https://api.sky.cirium.com/v1/flights/status/{flightId}

### path Parameters:
- **REQUIRED** flightId: integer <int64>

Unique flight identifier assigned by Cirium.

This numeric identifier is stable over time and refers to a specific flight instance, including airline, flight number, and operating date. It is especially useful when accessing current flight status or retrieving historical flight status data with precision.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

## by Tail Number: 

https://api.sky.cirium.com/v1/flights/status/tail-number/{tailNumber}/departure-date/{departureDate}

### path Parameters:
- **REQUIRED** tailNumber: string
Aircraft tail number (also known as registration number), used to identify a specific airframe.
Typically includes a country prefix followed by a registration code, e.g. N12345 or G-EZTD.

- **REQUIRED** departureDate: string <date>
Example: 2025-08-23
Date of departure in YYYY-MM-DD format (ISO 8601), for example: 2025-08-23.
The date is interpreted in the local time of the departure airport.

### query Parameters: 
- numDays: 	
integer [ 1 .. 10 ]
Default: 1
Controls how many days of flights are returned, starting from the specified date.
Accepts values from 1 to 10. Default is 1.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Historical Flight Status API:

## Airport Arrivals by Date:

https://api.sky.cirium.com/v1/flights/historical-status/arrival-airport/{arrivalAirport}/arrival-date/{arrivalDate}/arrival-hour/{arrivalHour}

### path Parameters:
- **REQUIRED** arrivalAirport: string
Example: LAX
Code of the arrival airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** arrivalDate: string <date>
Example: 2015-08-23
Date of arrival in YYYY-MM-DD format (ISO 8601), for example: 2015-10-01.
The date is interpreted in the local time of the arrival airport unless the utc flag is set to true.

- **REQUIRED** arrivalHour: string^([0-9]|1[0-9]|2[0-3])$
Example: 4
Hour of arrival in HH format (0–23), with or without a leading zero. For example: 4 for 4 AM or 16 for 4 PM.
The hour is interpreted in the local time of the arrival airport unless the utc flag is set to true.

### query Parameters:
- utc: boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- numHours: integer <int64> [ 1 .. 6 ]
Default: 1
Example: numHours=3
Controls how many hours of arrival or departure flights are returned, starting from the specified hour.
Accepts values from 1 to 6. Default is 1. Used to define the size of the time window.

- carrier: string
Example: carrier=AA
Filters results to include only flights operated by the specified airline.

Accepted formats:
    IATA (2-character), e.g. BA, LH
    ICAO (3-character), e.g. BAW, DLH
    FS (alphanumeric, 2 to 3 characters), e.g. BA

All formats are supported and matched in this order: IATA, ICAO, then FS.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.

Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

- maxFlights: integer <int64> >= 1
Example: maxFlights=20
Limits the number of unique flights returned in the response.
If not specified, all matching flights are returned. A value of 0 is not allowed and will return an error.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.

Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

### Response: 
schema: string

flightId: integer <int64> -> The unique identifier for the flight

carrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

carrierFsCode: string -> The Cirium unique code for the operating carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options)

operatingCarrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

operatingCarrierFsCode: string -> The Cirium unique code for the operating carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options). Returned if specifying includeNewFields in extendedOptions.

primaryCarrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

primaryCarrierFsCode: string -> The Cirium unique code for the primary carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options). Returned if specifying includeNewFields in extendedOptions.

flightNumber: string -> The flight identification number and any additional characters

departureAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

departureAirportFsCode: string -> The Cirium unique code for the departure airport to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options)

arrivalAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

arrivalAirportFsCode: string -> The Cirium unique code for the arrival airport to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options)

divertedAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

divertedAirportFsCode: string -> The Cirium unique code for the airport to which the flight was diverted, if any, to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options).

departureDate: object (DateUtcAndLocal)

arrivalDate: object (DateUtcAndLocal)

status: string 
The current status of the flight. One of the following values:
    A - Active
    C - Canceled
    D - Diverted
    DN - Data Needed
    L - Landed
    NO - Not Operational
    R - Redirected
    S - Scheduled
    U - Unknown

schedule: object (Schedule)

operationalTimes: object (OperationalTimes)

codeshares: Array of objects (Codeshare) -> Zero or more marketing or operating relationships for this flight

delays: object (Delays) -> Any calculated delays for the flight based on operational times (scheduled, estimated and actual)

flightDurations: object (FlightDurations) -> Calculated flight durations based on operational times (scheduled, estimated and actual)

airportResources: object (AirportResources) -> Information related to the departure and arrival terminal, gate and baggage

flightEquipment: object (FlightEquipment) -> Information about the equipment used for this flight. May contain equipment objects inlined if specifying useInlinedReferences, otherwise the equipment can be looked up in the appendix using the codes provided.

flightStatusUpdates: Array of objects (FlightStatusUpdate) -> Contains a list of all updates that have occurred to this flight status since originally published. Included if the specifying includeDeltas in extended options.

irregularOperations: Array of objects (IrregularOperation) -> A list of zero or more irregular operations that have occurred for this flight. Returned if specifying includeNewFields in extendedOptions.

confirmedIncident: object (ConfirmedIncident) -> This object contains information about a severe issue with the flight. Cirium manually publishes the message. It rarely is published, and usually is the result of an accident with the aircraft. The message is a textual description of what occurred. Returned if specifying includeNewFields in extendedOptions.

lastDataAcquiredDate: string <date-time> -> The last time the flight status data was acquired

## Airport Depatures by Date:

https://api.sky.cirium.com/v1/flights/historical-status/departure-airport/{departureAirport}/departure-date/{departureDate}/departure-hour/{departureHour}

### path Parameters:
- **REQUIRED** departureAirport: string
Example: LHR
Code of the departure airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** departureDate: string <date>
Example: 2017-08-23
Date of departure in YYYY-MM-DD format (ISO 8601), for example: 2017-08-23.
The date is interpreted in the local time of the departure airport unless the utc flag is set to true.


- **REQUIRED** departureHour: string^([0-9]|1[0-9]|2[0-3])$
Example: 4
Hour of departure in HH format (0–23), with or without a leading zero. For example: 4 for 4 AM or 16 for 4 PM.
The hour is interpreted in the local time of the departure airport unless the utc flag is set to true.

### query Parameters:
- utc: 	
boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- numHours: integer <int64> [ 1 .. 6 ]
Default: 1
Example: numHours=3
Controls how many hours of arrival or departure flights are returned, starting from the specified hour.
Accepts values from 1 to 6. Default is 1. Used to define the size of the time window.

- carrier: string
Example: carrier=AA
Filters results to include only flights operated by the specified airline.

Accepted formats:
    IATA (2-character), e.g. BA, LH
    ICAO (3-character), e.g. BAW, DLH
    FS (alphanumeric, 2 to 3 characters), e.g. BA

All formats are supported and matched in this order: IATA, ICAO, then FS.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.

Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

- maxFlights: integer <int64> >= 1
Example: maxFlights=20
Limits the number of unique flights returned in the response.
If not specified, all matching flights are returned. A value of 0 is not allowed and will return an error.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:

    application/json – standard JSON format
    application/xml – XML format

If the header is missing or the value is not supported, the API will return an error.

## By Flight - Arrivals by Date: 

https://api.sky.cirium.com/v1/flights/historical-status/airline/{airline}/flight-number/{flightNumber}/arrival-date/{arrivalDate}

### path Parameters:
- **REQUIRED** airline: string
Example: AS
Code of the airline. Accepted formats:
    IATA – 2-character code, e.g. BA
    ICAO – 3-character code, e.g. BAW
    FS – Cirium unique code (2 or 3 alphanumeric characters)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** flightNumber: string^\d{1,4}[A-Z]?$
Example: 100
Flight number, excluding the airline code. Identifies a specific flight operated by the airline on a given day.
The value consists of 1 to 4 digits and may include an optional single uppercase letter as a suffix. Leading zeros are allowed.
For example:
    BA123 → flightNumber is 123
    DL045B → flightNumber is 045B

- **REQUIRED** arrivalDate: string <date>
Example: 2015-08-23
Date of arrival in YYYY-MM-DD format (ISO 8601), for example: 2015-10-01.
The date is interpreted in the local time of the arrival airport unless the utc flag is set to true.

### query Parameters: 
- utc: 	boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- airport: string
Optional filter to restrict results to the arrival airport.
Accepted formats:
    IATA – 3-letter airport code, e.g. LAX
    ICAO – 4-letter airport code, e.g. KLAX
    FS - 3-4 alphanumeric characters, Cirium unique airport code

All formats are supported and matched in this order: IATA, ICAO, then FS.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.
Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

### Response: 
schema: string

flightId: integer <int64> -> The unique identifier for the flight

carrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

carrierFsCode: string -> The Cirium unique code for the operating carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options)

operatingCarrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

operatingCarrierFsCode: string -> The Cirium unique code for the operating carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options). Returned if specifying includeNewFields in extendedOptions.

primaryCarrier: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

primaryCarrierFsCode: string -> The Cirium unique code for the primary carrier to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options). Returned if specifying includeNewFields in extendedOptions.

flightNumber: string -> The flight identification number and any additional characters

departureAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

departureAirportFsCode: string -> The Cirium unique code for the departure airport to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options)

arrivalAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

arrivalAirportFsCode: string -> The Cirium unique code for the arrival airport to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options)

divertedAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

divertedAirportFsCode: string -> The Cirium unique code for the airport to which the flight was diverted, if any, to use as a reference for finding the entry in the appendix (unless specifying useInlinedReferences in extended options).

departureDate: object (DateUtcAndLocal)

arrivalDate: object (DateUtcAndLocal)

status: string
The current status of the flight. One of the following values:
    A - Active
    C - Canceled
    D - Diverted
    DN - Data Needed
    L - Landed
    NO - Not Operational
    R - Redirected
    S - Scheduled
    U - Unknown

schedule: object (Schedule)

operationalTimes: object (OperationalTimes)

codeshares: Array of objects (Codeshare) -> Zero or more marketing or operating relationships for this flight

delays: object (Delays) -> Any calculated delays for the flight based on operational times (scheduled, estimated and actual)

flightDurations: object (FlightDurations) -> Calculated flight durations based on operational times (scheduled, estimated and actual)

airportResources: object (AirportResources) -> Information related to the departure and arrival terminal, gate and baggage

flightEquipment: object (FlightEquipment) -> Information about the equipment used for this flight. May contain equipment objects inlined if specifying useInlinedReferences, otherwise the equipment can be looked up in the appendix using the codes provided.

flightStatusUpdates: Array of objects (FlightStatusUpdate) -> Contains a list of all updates that have occurred to this flight status since originally published. Included if the specifying includeDeltas in extended options.

irregularOperations: Array of objects (IrregularOperation) -> A list of zero or more irregular operations that have occurred for this flight. Returned if specifying includeNewFields in extendedOptions.

confirmedIncident: object (ConfirmedIncident) -> This object contains information about a severe issue with the flight. Cirium manually publishes the message. It rarely is published, and usually is the result of an accident with the aircraft. The message is a textual description of what occurred. Returned if specifying includeNewFields in extendedOptions.

lastDataAcquiredDate: string <date-time> -> The last time the flight status data was acquired

## By Flight - Departures by Date: 

https://api.sky.cirium.com/v1/flights/historical-status/airline/{airline}/flight-number/{flightNumber}/departure-date/{departureDate}

### path Parameters:
- **REQUIRED** airline: string
Example: AS
Code of the airline. Accepted formats:
    IATA – 2-character code, e.g. BA
    ICAO – 3-character code, e.g. BAW
    FS – Cirium unique code (2 or 3 alphanumeric characters)

All formats are supported and matched in this order: IATA, ICAO, then FS.

### query Parameters: 
- **REQUIRED** flightNumber: string^\d{1,4}[A-Z]?$
Example: 100
Flight number, excluding the airline code. Identifies a specific flight operated by the airline on a given day.
The value consists of 1 to 4 digits and may include an optional single uppercase letter as a suffix. Leading zeros are allowed.
For example:
    BA123 → flightNumber is 123
    DL045B → flightNumber is 045B

- **REQUIRED** departureDate: string <date>
Example: 2012-05-02
Date of departure in YYYY-MM-DD format (ISO 8601), for example: 2012-05-02.
The date is interpreted in the local time of the departure airport unless the utc flag is set to true.

- utc: 	boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- airport: string
Optional filter to restrict results to the arrival airport.
Accepted formats:
    IATA – 3-letter airport code, e.g. LAX
    ICAO – 4-letter airport code, e.g. KLAX
    FS - 3-4 alphanumeric characters, Cirium unique airport code

All formats are supported and matched in this order: IATA, ICAO, then FS.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.
Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

## By Flight - By Flight ID:

https://api.sky.cirium.com/v1/flights/historical-status/{flightId}

### path Parameters:
- **REQUIRED** flightId: integer <int64>
Example: 1333667573
Unique flight identifier assigned by Cirium.
This numeric identifier is stable over time and refers to a specific flight instance, including airline, flight number, and operating date. It is especially useful when accessing current flight status or retrieving historical flight status data with precision.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

## By Flight - By Tail Number:

https://api.sky.cirium.com/v1/flights/historical-status/tail-number/{tailNumber}/departure-date/{departureDate}

### path Parameters:
- **REQUIRED** tailNumber: string
Aircraft tail number (also known as registration number), used to identify a specific airframe.
Typically includes a country prefix followed by a registration code, e.g. N12345 or G-EZTD.

- **REQUIRED** departureDate: string <date>
Example: 2025-08-23
Date of departure in YYYY-MM-DD format (ISO 8601), for example: 2025-08-23.
The date is interpreted in the local time of the departure airport.

### query Params: 
- numDays:	integer [ 1 .. 10 ]
Default: 1
Controls how many days of flights are returned, starting from the specified date.
Accepts values from 1 to 10. Default is 1.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

## By Route - Route by Arrival Date: 

https://api.sky.cirium.com/v1/flights/historical-status/departure-airport/{departureAirport}/arrival-airport/{arrivalAirport}/arrival-date/{arrivalDate}

### path Parameters:
- **REQUIRED** departureAirport: string
Example: LHR
Code of the departure airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** arrivalAirport: string
Example: LAX
Code of the arrival airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.


- **REQUIRED** arrivalDate: string <date>
Example: 2025-08-23
Date of arrival in YYYY-MM-DD format (ISO 8601), for example: 2025-10-01.
The date is interpreted in the local time of the arrival airport unless the utc flag is set to true.

### query Parameters:

- hourOfDay: string^([0-9]|1[0-9]|2[0-3])$
Example: hourOfDay=9
Sets the starting hour of the time window for flights returned, based on scheduled departure or arrival time.
Accepts values from 0 to 23, with or without a leading zero. For example: 9 for 9 AM, 18 for 6 PM.
The hour is interpreted in local time unless the utc flag is set to true.

- numHours: integer <int64> [ 1 .. 24 ]
Default: 1
Example: numHours=3
Controls how many hours of arrival or departure flights are returned, starting from the specified hour.
Accepts values from 1 to 24. Default is 24. Used to define the size of the time window.

- utc: 	boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.
Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

- maxFlights: integer <int64> >= 1
Example: maxFlights=20
Limits the number of unique flights returned in the response.
If not specified, all matching flights are returned. A value of 0 is not allowed and will return an error.

nonstopOnly: boolean
Default: true
Filters results to include only nonstop flights between the specified departure and arrival airports.
Default is true.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

## By Route - Route by Departure Date:

https://api.sky.cirium.com/v1/flights/historical-status/departure-airport/{departureAirport}/arrival-airport/{arrivalAirport}/departure-date/{departureDate}

### path Parameters:
- **REQUIRED** departureAirport: string
Example: LHR
Code of the departure airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** arrivalAirport: string
Example: LAX
Code of the arrival airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** departureDate: string <date>
Example: 2025-08-23
Date of departure in YYYY-MM-DD format (ISO 8601), for example: 2025-10-01.
The date is interpreted in the local time of the arrival airport unless the utc flag is set to true.

### query Parameters:

- hourOfDay: string^([0-9]|1[0-9]|2[0-3])$
Example: hourOfDay=9
Sets the starting hour of the time window for flights returned, based on scheduled departure or arrival time.
Accepts values from 0 to 23, with or without a leading zero. For example: 9 for 9 AM, 18 for 6 PM.
The hour is interpreted in local time unless the utc flag is set to true.

- numHours: integer <int64> [ 1 .. 24 ]
Default: 1
Example: numHours=3
Controls how many hours of arrival or departure flights are returned, starting from the specified hour.
Accepts values from 1 to 24. Default is 24. Used to define the size of the time window.

- utc: 	boolean
Default: false
Enum: true false
Possible values are true or false. When true, the arrival or departure date and hour are interpreted in UTC. When false (default), they are interpreted in the local time of the specified airport.
This affects which flights are included in the time window, especially when querying around midnight or across time zones.

- codeType:	string
Enum: "IATA" "ICAO" "FS"
Defines what type of airline code is used in the request.
Possible values are:
    IATA – 2-character airline code, e.g. BA
    ICAO – 3-character airline code, e.g. BAW
    FS – Cirium’s unique 2 or 3-character alphanumeric airline code

If not specified, the API will try all formats in this order: IATA, ICAO, then FS.

- maxFlights: integer <int64> >= 1
Example: maxFlights=20
Limits the number of unique flights returned in the response.
If not specified, all matching flights are returned. A value of 0 is not allowed and will return an error.

nonstopOnly: boolean
Default: true
Filters results to include only nonstop flights between the specified departure and arrival airports.
Default is true.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Ratings API: 

## by Flight:

https://api.sky.cirium.com/v1/ratings/airline/{airline}/flight-number/{flightNumber}

### path Parameters:
- **REQUIRED** airline: string
Example: AS
Code of the airline. Accepted formats:
    IATA – 2-character code, e.g. BA
    ICAO – 3-character code, e.g. BAW
    FS – Cirium unique code (2 or 3 alphanumeric characters)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- **REQUIRED** flightNumber: string^\d{1,4}[A-Z]?$
Example: 100
Flight number, excluding the airline code. Identifies a specific flight operated by the airline on a given day.
The value consists of 1 to 4 digits and may include an optional single uppercase letter as a suffix. Leading zeros are allowed.
For example:
    BA123 → flightNumber is 123
    DL045B → flightNumber is 045B

### query Parameters:
- departureAirport: string
Example: departureAirport=PDX
Departure airport code used to filter results.
If provided, only flights departing from the specified airport are included.
Accepted formats:
    IATA: 3-letter airport code (e.g. LHR)
    ICAO: 4-letter airport code (e.g. EGLL)
    FS: 3–4 alphanumeric Cirium code (e.g. LAX)
    If omitted, results are not restricted by departure airport.

- codeType: string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS
Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

### Response:
airlineFsCode: string -> The Cirium unique code for the airline to use as a reference for finding the entry in the appendix (unless the extended option to include inlined references is used)

flightNumber: string -> The flight identifier of the flight, typically a number

departureAirportFsCode: string -> The Cirium unique code for the departure airport to use as a reference for finding the entry in the appendix (unless the extended option to include inlined references is used)

arrivalAirportFsCode: string -> The Cirium unique code for the arrival airport to use as a reference for finding the entry in the appendix (unless the extended option to include inlined references is used).

departureAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

airline: object or null (Airline) -> The airline object contains the unique codes and name that identify a unique airline or carrier

arrivalAirport: object or null (Airport) -> The airport object contains the unique codes and name that identify a unique airport

codeshares: integer <int32> -> The number of codeshare observations in the rating

directs: integer <int32> -> The number of direct flights in the rating

observations: integer <int32> -> The number of observations in the sample for ontime performance

ontime: integer <int32> -> The number of observations classified as "ontime" (<15 minutes late)

late15: integer <int32> -> The number of observations classified as "late" (15 - 29 minutes)

late30: integer <int32> -> The number of observations classified as "very late" (30 - 44 minutes)

late45: integer <int32> -> The number of observations classified as "excessively late" (45 + minutes)

cancelled: integer <int32> -> The number of observations cancelled

diverted: integer <int32> -> The number of observations diverted

ontimePercent: number <double> -> The percent of ontime observations

delayObservations: integer <int32> -> The number of observations that arrived later than scheduled time (> 1 minute late)

delayMean: number <double> -> The mean delay

delayStandardDeviation: number <double> -> The standard deviation of the delay

delayMin: integer <int32> -> The minimum delay value observed

delayMax: integer <int32> -> The maximum delay value observed

allOntimeCumulative: number <double> -> How the flight ranks relative to peers on ontime performance (better than %)

allOntimeStars: number <double> -> The rating for this flight's ontime performance (0-5 scale) compared to all flights

allDelayCumulative: number <double> -> How the flight ranks relative to peers on delay performance (better than %)

allDelayStars: number <double> -> The rating for this flight's delay performance (0-5 scale) compared to all flights

allStars: number <double> -> The avg of All_ontime_stars and All_delay_stars yielding the overall performance measure of this flight compared to all flights

## by Route: 

https://api.sky.cirium.com/v1/ratings/departure-airport/{departureAirport}/arrival-airport/{arrivalAirport}

### path Parameters: 
- **REQUIRED** departureAirport: string
Example: PDX
Code of the departure airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

- arrivalAirport: string
Example: SEA
Code of the arrival airport. Accepted formats:
    IATA (3-letter)
    ICAO (4-letter)
    FS (3-4 alphanumeric characters, Cirium unique airport code)

All formats are supported and matched in this order: IATA, ICAO, then FS.

### query Parameters:
- codeType: string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS
Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

# ----------------------------------------------------------------------------------------
# Wheather API:

## by Airport Code:

https://api.sky.cirium.com/v1/weather/airport/{airport}

### path Parameters:
- **REQUIRED** airport: string
Example: PDX
Airport code used to retrieve weather data.
Supports IATA (3-letter), ICAO (4-letter), or Cirium FS (3–4 alphanumeric) codes.

### query Parameters: 
- codeType: 	
string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS
Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

### Response:
#### metar:
reportTime: string -> Time the report was issued by the weather station (UTC)

report: string -> Original METAR report text

tags: Array of objects (Tag) -> Additional key/value annotations that provide summary information for the Metar report

weatherStationIcao: string -> ICAO code of the weather station issuing the report. This is not the same as the ICAO code of the nearest airport.

reportModifier: string -> Modifier string for this report. Could be 'Amendment' or 'Correction'.

conditions: object (Conditions) -> The primary set of weather conditions are grouped into a "Conditions" model object including wind, visibility, weather phenomena, cloud coverage, and barometric pressure. "Conditions" sections occur in both METAR reports and TAF forecast sections.

runwayVisualRanges: Array of objects (RunwayVisualRange) -> List of runway visual ranges described by the report

obscurations: Array of objects (Obscuration) -> List of obscurations described by the report

noSignificantChange: boolean -> Boolean value indicating that no significant change is expected to the reported conditions within the next 2 hours

temperatureCelsius: string -> Temperature (degrees celsius/centigrade)

dewPointCelsius: string -> Dew point temperature (degrees celsius/centigrade)

#### taf: 
report: string -> Original TAF report text

reportTime: string -> Time the report was issued by the weather station (UTC)

weatherStationIcao: string -> ICAO code of the weather station issuing the report. This is not the same as the ICAO code of the nearest airport.

observationTime: string -> Timestamp of the observations the report is based on (UTC)

forecasts: Array of objects (Forecast) -> List of forecasts contained in the report

reportType: string or null -> Type of report: 'Normal', 'Amendment', or 'Correction'

#### zoneForecast:
general: string -> General section of the original forecast, providing various kinds of top-level data.

header: string -> Header section of the original forecast, listing zone names, cities, time, and sometimes other information such as advisories.

cities: Array of strings unique -> List of cities within the zone

zoneNames: Array of strings unique -> List of zone names, for zones included in this report

dayForecasts: Array of objects (DayForecast) -> List of day forecasts contained in the report.

reportTime: string -> Timestamp for when the forecast was produced (UTC)

zones: Array of strings unique -> List of zones the forecast applies to

## METAR by Airport Code: 

https://api.sky.cirium.com/v1/weather/airport/{airport}/metar

### path Parameters:
- **REQUIRED** airport: string
Example: PDX
Airport code used to retrieve weather data.
Supports IATA (3-letter), ICAO (4-letter), or Cirium FS (3–4 alphanumeric) codes.

### query Parameters: 
- codeType: 	
string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS
Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

## TAF by Airport Code: 

https://api.sky.cirium.com/v1/weather/airport/{airport}/taf

### path Parameters:
- **REQUIRED** airport: string
Example: PDX
Airport code used to retrieve weather data.
Supports IATA (3-letter), ICAO (4-letter), or Cirium FS (3–4 alphanumeric) codes.

### query Parameters: 
- codeType: 	
string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS
Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.

## Zone Forecast by Airport Code:

https://api.sky.cirium.com/v1/weather/airport/{airport}/zone-forecast

### path Parameters:
- **REQUIRED** airport: string
Example: PDX
Airport code used to retrieve weather data.
Supports IATA (3-letter), ICAO (4-letter), or Cirium FS (3–4 alphanumeric) codes.

### query Parameters: 
- codeType: 	
string
Enum: "IATA" "ICAO" "FS"
Example: codeType=FS
Defines what type of airport code is being used in the request.
Options:
    IATA – 3-letter airport code, e.g. LHR
    ICAO – 4-letter airport code, e.g. EGLL
    FS - 3-4 alphanumeric characters, Cirium unique airport code

If not set, the API will try all formats in this order: IATA, ICAO, then FS.

### header Parameters:
- **REQUIRED** Accept: string 
Enum: "application/json", "application/xml"
Required header that defines the response format.
Supported values:
    application/json – standard JSON format
    application/xml – XML format
If the header is missing or the value is not supported, the API will return an error.