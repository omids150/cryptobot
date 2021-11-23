CREATE TABLE results.forecast (
    modification_time TIMESTAMPTZ DEFAULT now(),
    symbol text,
    corr_btc JSON,
    corr_eth JSON,
    variance real,
    complite boolean
);