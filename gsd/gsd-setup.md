```bash
sudo python3 -m pip install -r requirements.txt
sudo cp gsd-ingest.service /etc/systemd/system/gsd-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable gsd-ingest.service
sudo systemctl start gsd-ingest.service
```

```bash
sudo systemctl restart gsd-ingest.service
sudo systemctl status gsd-ingest.service
tail -f ~/gsd-to-ingest/logs
```

[Zerotier setup](https://docs.google.com/document/d/1l8SA2pNLpueWjAy0l3gStlXXv-Tw3wwl3vfgqVdrA8s/edit?usp=sharing)
