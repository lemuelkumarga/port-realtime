import globalvars as g
import secretvars as s
import pandas as pd
import time
import math
from datetime import date
import alpaca_trade_api as tradeapi

# API parameters
polygon_api = tradeapi.REST(s.insert_alpaca_api_key_here,
                            s.insert_alpaca_api_secret_here,
                            s.insert_alpaca_api_base_url_here).polygon
dt = str(date.today())


# Returns the latest realtime prices for the ticker
def get_realtime_prices(ticker):
    output = pd.DataFrame()

    loop_counter = 0
    while loop_counter < 5:
            try:
                output = output.append(
                    polygon_api.historic_quotes_v2(symbol=ticker, date=dt, reverse=True, limit=10000).df.reset_index())
                loop_counter = 5
            except Exception as e:
                print(e)
                loop_counter += 1
                # If you face error 5 times, force move to the next date
                if loop_counter == 5:
                    force_move_to_next = True
                else:
                    time.sleep(1)

    output['ts'] = output['sip_timestamp'].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
    output['ts_hour'] = output['sip_timestamp'].apply(lambda x: x.hour)
    output['ts_minute'] = output['sip_timestamp'].apply(lambda x: x.minute)
    output['ts_second'] = output['sip_timestamp'].apply(lambda x: math.floor(x.second / 2) * 2)
    output['px'] = output['ask_price']
    output = output[(output['ts'] >= dt + " " + "09:30:00") & (output['ts'] <= dt + " " + "16:00:00")]

    output = output[['ts', 'ts_hour', 'ts_minute', 'ts_second', 'px']] \
             .drop_duplicates(['ts_hour', 'ts_minute', 'ts_second'])

    # Parse the information into the cache
    for row in output.iterrows():

        # Get values
        d, t = row[1]['ts'].split(' ')
        val = row[1]['px']

        # Set current date in the first iteration
        if g.cur_dt is None:
            g.cur_dt = d
        # We only want to collect prices for current date. 
        # Ignore all previous date prices
        elif g.cur_dt > d:
            break

        # Set time as the keys in cache
        if t not in g.cache.keys():
            g.cache[t] = {}

        g.cache[t][ticker] = float(val)


# Main function to ping stock prices 
def main():
    for i in g.tickers:
        get_realtime_prices(i)
