# Canterbury Seismic Instruments (CSI) instructions

## Installation

```bash
scp csi/* pi@ip-address:~/csi-to-ingest
```

## Setup

[Zerotier setup](https://docs.google.com/document/d/1l8SA2pNLpueWjAy0l3gStlXXv-Tw3wwl3vfgqVdrA8s/edit?usp=sharing)

```bash
sudo python3 -m pip install -r requirements.txt --break-system-packages
sudo cp csi-ingest.service /etc/systemd/system/csi-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable csi-ingest.service
sudo systemctl start csi-ingest.service
```

## Debugging

```bash
sudo systemctl restart csi-ingest.service
sudo systemctl status csi-ingest.service
tail -f ~/csi-to-ingest/logs
```
