Get USB ports

```bash
ls /dev/tty.*
ls /dev/cu.*
```

Install service

```bash
sudo python3 -m pip install -r requirements.txt --break-system-packages
sudo cp crisislab-ingest.service /etc/systemd/system/crisislab-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable crisislab-ingest.service
sudo systemctl start crisislab-ingest.service
```

```bash
# Service management
sudo systemctl restart crisislab-ingest.service
sudo systemctl status crisislab-ingest.service
# get logs
tail -f ~/crisislab-to-ingest/logs
```

[Zerotier setup](https://docs.google.com/document/d/1l8SA2pNLpueWjAy0l3gStlXXv-Tw3wwl3vfgqVdrA8s/edit?usp=sharing)
