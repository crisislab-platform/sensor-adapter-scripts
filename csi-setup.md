```bash
pip install -r requirements.txt
sudo cp csi-ingest.service /etc/systemd/system/csi-ingest.service
sudo systemctl daemon-reload
sudo systemctl enable csi-ingest.service
sudo systemctl start csi-ingest.service
```

```bash
sudo systemctl restart csi-ingest.service
sudo systemctl status csi-ingest.service
tail -f ~/csi-to-ingest/logs
```
