import os
import subprocess
from datetime import datetime
from typing import Tuple

import pandas as pd

REGULAR_PORTS = [
    80,
    443,
    2052,
    2053,
    2082,
    2083,
    2086,
    2087,
    2095,
    2096,
    8080,
    8443,
    8880,
]
ROOT_PATH = "D:\FQFQFQFQ\CF-IP\IP库"
UUID = "254ee1c9-62ac-4062-b720-b575fb90d1ea"
HOST = "notls.zjccc.onflashdrive.app"


def csv2vless(input_filename: str, output_filename: str) -> None:
    df = pd.read_csv(input_filename)
    vless_strs = []
    for _, row in df.iterrows():
        ip = row["IP地址"]
        port = row["端口"]
        dc = row["数据中心"]
        city = row["城市"]
        vless = f"vless://{UUID}@{ip}:{port}?encryption=none&security=tls&sni={HOST}&fp=random&type=ws&host={HOST}&path=/?ed=2560#{dc} | {city}"
        vless_strs.append(vless)

    if vless_strs:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(vless_strs))


# csv2vless('./data/ip.csv', "./data/vless.txt")


def ip_test(input_filename: str, output_filename: str) -> None:
    subprocess.run(
        f"./bin/cfiptest.exe -f {input_filename} -st 0 -maxdc 100000 -o {output_filename}",
        check=True,
    )


# ip_test("./data/ip.txt", "./data/output.csv")
def csv2ip(root: str, suffix: str) -> Tuple[str, str]:
    csv_files = [file for file in os.listdir(root) if file.endswith(".csv")]

    df_list = []
    for f in csv_files:
        df = pd.read_csv(os.path.join(root, f))
        df = df[df["TLS"]]
        new_df = df.loc[:, ["IP地址", "端口"]]
        df_list.append(new_df)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.sort_values(by=["IP地址", "端口"], inplace=True)
    combined_df.drop_duplicates(subset=["IP地址", "端口"], keep="first", inplace=True)

    # 区分常规端口和非常规端口
    irregular_port_df = combined_df[~combined_df["端口"].isin(REGULAR_PORTS)]
    combined_df = combined_df[combined_df["端口"].isin(REGULAR_PORTS)]
    irregular_port_df.reset_index(drop=True, inplace=True)
    combined_df.reset_index(drop=True, inplace=True)

    irregular_ports_filename = f"irp_{suffix}.txt"
    regular_ports_filename = f"rp_{suffix}.txt"

    ir_ip_pairs = [
        f'{row["IP地址"]}:{row["端口"]}' for _, row in irregular_port_df.iterrows()
    ]
    ip_pairs = [f'{row["IP地址"]}:{row["端口"]}' for _, row in combined_df.iterrows()]

    with open(
        os.path.join("./data", irregular_ports_filename), "w", encoding="utf-8"
    ) as ir_f:
        ir_f.write("\n".join(ir_ip_pairs))
    with open(
        os.path.join("./data", regular_ports_filename), "w", encoding="utf-8"
    ) as reg_f:
        reg_f.write("\n".join(ip_pairs))

    return irregular_ports_filename, regular_ports_filename


if __name__ == "__main__":
    today = f"{datetime.now():%Y%m%d}"
    ir, r = csv2ip(ROOT_PATH, suffix=today)

    ip_test(f"./data/{ir}", f"./data/ir_{today}.csv")
    ip_test(f"./data/{r}", f"./data/r_{today}.csv")

    csv2vless(f"./data/ir_{today}.csv", f"./data/vless_ir_{today}.txt")
    csv2vless(f"./data/r_{today}.csv", f"./data/vless_r_{today}.txt")
