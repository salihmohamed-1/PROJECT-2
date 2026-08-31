# AtmoSync Data Dictionary

## 1. RAW Schema (`ATMOSYNC.RAW`)

### Table: `RAW_TELEMETRY`
| Column Name | Data Type | Constraint | Description |
|---|---|---|---|
| `EVENT_ID` | VARCHAR(64) | PRIMARY KEY | Unique UUID for telemetry event |
| `CONTAINER_ID` | VARCHAR(32) | NOT NULL | Container identifier |
| `EVENT_TIMESTAMP` | TIMESTAMP_NTZ | NOT NULL | UTC timestamp recorded by IoT sensor |
| `TEMPERATURE` | NUMBER(5,2) | | Internal container temperature in °C |
| `HUMIDITY` | NUMBER(5,2) | | Relative humidity percentage (0-100%) |
| `VIBRATION` | NUMBER(5,3) | | Vibration shock metric G-force |
| `LATITUDE` | NUMBER(9,6) | | GPS latitude coordinate |
| `LONGITUDE` | NUMBER(9,6) | | GPS longitude coordinate |
| `ORIGIN` | VARCHAR(64) | | Cargo origin port/city |
| `DESTINATION` | VARCHAR(64) | | Planned destination market |
| `COMMODITY` | VARCHAR(64) | | Cargo commodity type |
| `INGESTED_AT` | TIMESTAMP_NTZ | DEFAULT CURRENT | System load timestamp |

### Table: `COMMODITY_PRICING`
| Column Name | Data Type | Constraint | Description |
|---|---|---|---|
| `PRICE_ID` | VARCHAR(64) | PRIMARY KEY | Price record identifier |
| `COMMODITY` | VARCHAR(64) | NOT NULL | Cargo commodity name |
| `MARKET` | VARCHAR(64) | NOT NULL | Regional spot market name |
| `PRICE_PER_UNIT_INR` | NUMBER(10,2) | NOT NULL | Spot price per unit in INR (₹) |
| `EFFECTIVE_TIMESTAMP` | TIMESTAMP_NTZ | | Effective price timestamp |

---

## 2. ANALYTICS Schema (`ATMOSYNC.ANALYTICS`)

### Fact Model: `FCT_SPOILAGE_ARBITRAGE`
| Column Name | Data Type | Description |
|---|---|---|
| `CONTAINER_ID` | VARCHAR(32) | Container ID |
| `COMMODITY` | VARCHAR(64) | Commodity type |
| `RECOMMENDED_MARKET` | VARCHAR(64) | Financially optimal target reroute market |
| `RISK_LEVEL` | VARCHAR(16) | Environmental risk classification (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) |
| `SPOILAGE_PROBABILITY` | FLOAT | Estimated probability of product degradation (0.0 to 1.0) |
| `ESTIMATED_TIME_TO_SPOILAGE_HOURS` | FLOAT | Calculated remaining safe shelf life in hours |
| `DISTANCE_TO_RECOMMENDED_MARKET_KM` | FLOAT | Haversine distance in km to recommended market |
| `TRANSIT_HOURS_TO_RECOMMENDED_MARKET` | FLOAT | Estimated transit travel hours to recommended market |
| `CARGO_BASE_VALUE_INR` | FLOAT | Total baseline cargo value in INR |
| `ESTIMATED_SPOILAGE_LOSS_INR` | FLOAT | Expected financial loss if spoilage occurs on current route |
| `REROUTE_COST_INR` | FLOAT | Calculated transport cost to reroute shipment (₹45/km) |
| `NET_ARBITRAGE_PROFIT_INR` | FLOAT | Net recovered cargo value minus reroute cost |
| `ARBITRAGE_SCORE` | FLOAT | Weighted score (0 to 100) indicating reroute urgency & profitability |
| `ARBITRAGE_OPPORTUNITY_FLAG` | BOOLEAN | `TRUE` if rerouting is reachable and yields positive net profit |
| `ACTION_RECOMMENDATION` | VARCHAR(128) | Actionable text recommendation for traders |
