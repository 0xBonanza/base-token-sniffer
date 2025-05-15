r"""
  ___       ____
 / _ \__  _| __ )  ___  _ __   __ _ _ __  ______ _
| | | \ \/ /  _ \ / _ \| '_ \ / _` | '_ \|_  / _` |
| |_| |>  <| |_) | (_) | | | | (_| | | | |/ / (_| |
 \___//_/\_\____/ \___/|_| |_|\__,_|_| |_/___\__,_|

Any question? 0xbonanza@gmail.com
"""

import time
import requests
import json
import winsound
import os
from dotenv import load_dotenv

load_dotenv()

BASE_API_KEY = os.getenv("BASE_API_KEY")
RPM = 6
SNIFFED_ADDRESSES = [
    "0x73ecef8f514c92481990bec889bf8225771a2b9f",
    "0xeda91183dc672e1a62f5442d08e72b04be08000e",
    "0xb302d6ffb51ed526d6ecff4241c5ee12f3eb2e94",
    "0xB4E4D8472C80CfDDe38536d247F3647cE82520c2",
    "0x0517AA178311D28A553A3183d80C97f9dd288C03",
    "0x3810Fb0D9E216e8A2d9138be36328caD7E16183a",
    "0x60b760E37E2FFD46E8707f285020C5D5e5A561E5",
    "0x381Bf860FE9A97e5d59505AFf24C72B4777bB796",
    "0x6b71751A54259F3B222Cc85b0533652231157F1b",
    "0x61e2bE0Eb76084F19cd8e3066093a2f3709EFA67",
    "0xCEE282BE901945645C1f7Cc7ca149a780b0C144A"
]


def sniff():
    """loop sniff a base wallet for new token creation"""
    last_searched_block = 0  # restarts at block 0 at every run
    while True:
        for sniffed_address in SNIFFED_ADDRESSES:
            # use basescan to find new token creation
            query = (f"https://api.basescan.org/api"
                     f"?module=account"
                     f"&action=tokentx"
                     f"&address={sniffed_address}"
                     f"&sort=desc"
                     f"&startblock={last_searched_block}"
                     f"&apikey={BASE_API_KEY}"
                     )
            response = requests.get(query)
            response_json = json.loads(response.text)
            data = response_json["result"]
            print(f"Sniffing https://basescan.org/address/{sniffed_address}")
            # if any token transaction
            if len(data) > 0:
                with open('data.json', 'r+', encoding='utf-8') as f:
                    sniffed = json.load(f)
                    # go back sufficiently in the past to not miss any token creation
                    last_searched_block = int(data[0]["blockNumber"]) - 500  # TODO: could be improved
                    token_addresses = set([item["contractAddress"] for item in data]) - sniffed.keys()
                    for token_address in token_addresses:
                        print(f"--> New token found! Please check here: https://basescan.org/token/{token_address}")
                        # emit 3 beep sound to alert user of new token found
                        for i in range(3):
                            winsound.Beep(200, 100)
                        sniffed[token_address] = {"first found": time.time()}
                # save token found
                with open('data.json', 'w+', encoding='utf-8') as f:
                    json.dump(sniffed, f)
            time.sleep(60 / RPM)


if __name__ == '__main__':
    sniff()
