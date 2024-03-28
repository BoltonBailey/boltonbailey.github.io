import csv
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
from scipy.stats import chisquare

hourly_block_counts = np.zeros(24)
hourly_fee_totals = np.zeros(24)
hourly_generation_totals = np.zeros(24)
deltas = []
fees = []

daily_fee_market_quintile_bins = []

# data from https://loyce.club/blockdata/, (I only use later dates)
with open('./data/blockdata.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
    prev_time = parser.parse("2009-01-03 18:15:05")
    for row in spamreader:
        time = parser.parse(row["time"])
        time_delta = time - prev_time
        prev_time = time
        year = time.year
        hour = time.hour
        fee = float(row["fee_total_usd"])
        print(row["time"], time_delta.total_seconds()/60, fee)
        if 2021 == year:
            hourly_block_counts[hour] += 1
            hourly_fee_totals[hour] += fee
            hourly_generation_totals[hour] += float(row["generation_usd"])
            deltas.append(time_delta.total_seconds()/60)
            fees.append(fee)
            if len(fees) >= 4000:
                break


normalized_fees = [144 * fees[i] / sum(fees[i:i+144]) for i in range(len(fees)-144)]

# First Plot

plt.title("Fees Collected Total by Hour in 2021")
plt.ylabel("Total (Millions USD)")
plt.xlabel("Hour (UTC)")
plt.bar(range(24), np.array(hourly_fee_totals)/1e6)
plt.savefig("img/fees-by-hour.png")

print("fees over total", np.sum(hourly_fee_totals)/np.sum(hourly_fee_totals + hourly_generation_totals))

plt.clf()

# Second Plot

plt.title("# Blocks by Hour in 2021")
plt.ylabel("Count of Blocks")
plt.xlabel("Hour (UTC)")
plt.bar(range(24), hourly_block_counts)
plt.savefig("img/blocks-by-hour.png")

print("Chisquare hourly block totals", chisquare(hourly_block_counts))

plt.clf()

# Third Plot

# plt.title("Time to mine block vs. Fee")
# plt.ylabel("Block Fee / Avg Block Fee of subsequent blocks")
# plt.xlabel("Time to mine (minutes)")
# plt.scatter(deltas[:-144], normalized_fees, s=1)
# plt.savefig("img/fees-by-time.png")

# plt.clf()

# Fourth Plot

plt.title("Time to mine block vs. Fee")
plt.ylabel("Block Fee / Avg Block Fee of subsequent blocks")
plt.xlabel("Time to mine (minutes)")
plt.xlim(0, 20)
plt.ylim(0, 5)
plt.scatter(deltas[:-144], normalized_fees, s=1)
plt.savefig("img/fees-by-time.png")

plt.clf()
